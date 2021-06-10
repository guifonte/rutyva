from copy import deepcopy
from dataclasses import dataclass, asdict
from typing import Any, Literal, Union, get_args, get_origin
from .validation import validate_any

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

  def validate_attributes(self, raise_error=True, return_error_message=False):
    dc_fields = self.__dataclass_fields__
    for dc_field_key in dc_fields:
      ann = dc_fields[dc_field_key].type
      att = self.__getattribute__(dc_field_key)
      try:
        validate_any(dc_field_key, att, ann)
      except Exception as e:
        error_message = f'({self.__class__.__name__}) attribute ' + e.args[0]
        if raise_error: raise TypeError(error_message)
        if return_error_message: return error_message
        return False
    
    if not raise_error: return True

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
