from copy import deepcopy
from dataclasses import dataclass, asdict
from .validation import validate_any
from .from_dict_generator import gen_from_any

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

      d_copy[key] = gen_from_any(d_copy[key], dc_fields[key].type)
      
    return cls(**d_copy) # type: ignore

    #list -> get_list=None, get_args=()
    #list[Any] -> get_origin=list, get_args=(Any,)
    #list[T] -> get_origin=list, get_args=(T,)
    #list[X, Y] -> Considerar só X
