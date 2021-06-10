from typing import get_origin, get_args, Union, Literal, Any
from copy import deepcopy


def from_dict(cls, d: dict):
  if not isinstance(d, dict): raise TypeError('Input is not a dict!')
  d_copy = deepcopy(d)

  dc_fields = cls.__dataclass_fields__  # type: ignore
  for key in d_copy:
    if key not in dc_fields:
      raise TypeError(f'{key} is not an attribute of {cls.__name__}')

    d_copy[key] = gen_from_any(d_copy[key], dc_fields[key].type)
    
  return cls(**d_copy) # type: ignore

def gen_from_any(d_val, ann):
  origin = get_origin(ann)
  if origin is not None:
    if origin == list:
      return gen_from_list(d_val, get_args(ann)[0])
    if origin == Union:
      return gen_from_union(d_val, get_args(ann))
    if origin == Literal: #(int, bool, str, bytes, None)
      return d_val
    if origin == tuple:
      return gen_from_tuple(d_val, get_args(ann))
    if origin == dict:
      return gen_from_dict(d_val, get_args(ann))

    print('GENERATION WITH ORIGIN NOT IMPLEMENTED:', ann, origin, d_val)
    return d_val
  else:
    if isinstance(d_val, ann):
      return d_val
    if ann == Any:
      return d_val

    # check if has from_dict class method
    from_dict_method = getattr(ann, 'from_dict', None)
    if from_dict_method is not None:
      return from_dict_method(d_val)
    
    try:
      return ann(**d_val)
    except:
      return d_val

def gen_from_list(d_val, ann):
  if not isinstance(d_val, list): return d_val

  gen_list = []
  for obj in d_val:
    gen_list.append(gen_from_any(obj, ann))
  
  return gen_list

def gen_from_tuple(d_val, anns):
  if not isinstance(d_val, (tuple, list)): return d_val

  anns_len = len(anns)
  d_val_len = len(d_val)

  if anns_len != d_val_len: return d_val

  gen_lis = []
  for i in range(len(anns)):
    gen_lis.append(gen_from_any(d_val[i], anns[i]))

  return tuple(gen_lis)

def gen_from_union(d_val, anns):
  for ann in anns:
    try:
      new_val = gen_from_any(d_val, ann)
    except:
      new_val = d_val
    
    if d_val != new_val:
      return new_val
  
  return d_val

def gen_from_dict(d_val, amns):
  if not isinstance(d_val, dict): return d_val
  new_dict = {}
  key_class = amns[0]
  val_class = amns[1]

  for val in d_val:
    new_key = gen_from_any(val, key_class) #needs to be hashable (int, bool, str, tuple)
    new_val = gen_from_any(d_val[val], val_class)
    try:
      new_dict[new_key] = new_val
    except:
      return d_val

  return new_dict