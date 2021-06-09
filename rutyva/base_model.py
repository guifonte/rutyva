from copy import deepcopy
from dataclasses import dataclass, asdict
from typing import Any, Literal, Union, get_args, get_origin

@dataclass
class BaseModel:
  def __post_init__(self):
    self.__pre_validation__()
    self.validate_attributes()
    self.__post_validation__()
  
  def __pre_validation__(self): pass

  def __post_validation__(self): pass

  def to_dict(self):
    return asdict(self)

  def validate_attributes(self):
    dc_fields = self.__dataclass_fields__
    for dc_field_key in dc_fields:
      ann = dc_fields[dc_field_key].type
      att = self.__getattribute__(dc_field_key)
      self._validate_any(dc_field_key, att, ann)

  def _validate_any(self, att_key, att, ann):
    origin = get_origin(ann)
    if origin is not None:
      self._validate_with_origin(origin, att_key, att, get_args(ann))
    else:
      ann_to_test = ann if ann != float else (int, float)

      if not isinstance(att, ann_to_test):
        raise TypeError(self._format_type_error(att_key, att, ann))
  
  def _validate_with_origin(self, origin, att_key, att, args):
      if origin == Union:
        return self._validate_union(att_key, att, args)
      if origin == Literal:
        return self._validate_literal(att_key, att, args)
      if origin == list:
        return self._validate_list(att_key, att, args)
      if origin == tuple:
        return self._validate_tuple(att_key, att, args)
      if origin == dict:
        return self._validate_dict(att_key, att, args)

      print('VALIDATION WITH ORIGIN NOT IMPLEMENTED:', att_key, att, args, origin)

  def _validate_dict(self, att_key, att, anns):
    if not isinstance(att, dict):
      raise TypeError(self._format_type_error(att_key, att, dict))

    key_class = anns[0]
    val_class = anns[1]
    for key in att:
      self._validate_any(att_key, key, key_class)
      self._validate_any(att_key, att[key], val_class)

  def _validate_literal(self, att_key, att, options):
    if att not in options:
      raise TypeError(f'{self.__class__.__name__} attribute {att_key} value {att} is not one of the valid options: {options}')

  def _validate_union(self, att_key, att, anns):
    for ann in anns:
      try:
        self._validate_any(att_key, att, ann)
        return
      except:
        pass
    
    raise TypeError(self._format_type_error(att_key, att, anns))
  
  def _validate_tuple(self, att_key, att, ann):
    if not isinstance(att, tuple):
      raise TypeError(self._format_type_error(att_key, att, tuple))
    
    att_len = len(att)
    ann_len = len(ann)
    if att_len != ann_len:
      raise TypeError(f'{self.__class__.__name__} tuple {att_key} ({att_key}) has length of {att_len} and should be {ann_len}')

    for i in range(ann_len):
      self._validate_any(att_key, att[i], ann[i])

  def _validate_list(self, att_key, att_list, ann):
    if not isinstance(att_list, list):
      raise TypeError(self._format_type_error(att_key, att_list, list))
    
    for item in att_list:
      self._validate_any(att_key, item, ann)

  def _format_type_error(self, att_key, att, ann) -> str:
    return f'{self.__class__.__name__} arguments types are not valid: "{att_key}" ({att}) is "{type(att).__name__}" and should be "{ann.__name__}"'

  @classmethod
  def from_dict(cls, d: dict):
    if not isinstance(d, dict): raise TypeError('Input is not a dict!')
    d_copy = deepcopy(d)

    dc_fields = cls.__dataclass_fields__  # type: ignore
    for key in d_copy:
      if key not in dc_fields:
        raise TypeError(f'{key} is not an attribute of {cls.__name__}')

      d_copy[key] = cls._gen_from_any(d_copy[key], dc_fields[key].type)
      
    return cls(**d_copy) # type: ignore

  @staticmethod
  def _gen_from_any(d_val, ann):
    origin = get_origin(ann)
    if origin is not None:
      if origin == list:
        return BaseModel._gen_from_list(d_val, get_args(ann)[0])
      if origin == Union:
        return BaseModel._gen_from_union(d_val, get_args(ann))
      if origin == Literal: #(int, bool, str, bytes, None)
        return d_val
      if origin == tuple:
        return BaseModel._gen_from_tuple(d_val, get_args(ann))
      if origin == dict:
        return BaseModel._gen_from_dict(d_val, get_args(ann))

      print('GENERATION WITH ORIGIN NOT IMPLEMENTED:', ann, origin, d_val)
      return d_val
    else:
      if isinstance(d_val, ann):
        return d_val
      if issubclass(ann, BaseModel):
        return ann.from_dict(d_val) 
      if ann == Any:
        return d_val
      
      try:
        return ann(**d_val)
      except:
        return d_val

      # print('GENERATION NOT IMPLEMENTED:', ann, d_val)
  
  @staticmethod
  def _gen_from_list(d_val, ann):
    if not isinstance(d_val, list): return d_val

    gen_list = []
    for obj in d_val:
      gen_list.append(BaseModel._gen_from_any(obj, ann))
    
    return gen_list

  @staticmethod
  def _gen_from_tuple(d_val, anns):
    if not isinstance(d_val, (tuple, list)): return d_val

    anns_len = len(anns)
    d_val_len = len(d_val)

    if anns_len != d_val_len: return d_val

    gen_lis = []
    for i in range(len(anns)):
      gen_lis.append(BaseModel._gen_from_any(d_val[i], anns[i]))

    return tuple(gen_lis)

  @staticmethod
  def _gen_from_union(d_val, anns):
    for ann in anns:
      try:
        new_val = BaseModel._gen_from_any(d_val, ann)
      except:
        new_val = d_val
      
      if d_val != new_val:
        return new_val
    
    return d_val
  
  @staticmethod
  def _gen_from_dict(d_val, amns):
    if not isinstance(d_val, dict): return d_val
    new_dict = {}
    key_class = amns[0]
    val_class = amns[1]

    for val in d_val:
      new_key = BaseModel._gen_from_any(val, key_class) #needs to be hashable (int, bool, str, tuple)
      new_val = BaseModel._gen_from_any(d_val[val], val_class)
      try:
        new_dict[new_key] = new_val
      except:
        return d_val

    return new_dict

    #list -> get_list=None, get_args=()
    #list[Any] -> get_origin=list, get_args=(Any,)
    #list[T] -> get_origin=list, get_args=(T,)
    #list[X, Y] -> Considerar só X
