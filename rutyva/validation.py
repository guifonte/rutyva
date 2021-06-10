from typing import Any, Literal, Union, get_args, get_origin


def validate_any(att_key, att, ann):
  origin = get_origin(ann)
  if origin is not None:
    validate_with_origin(origin, att_key, att, get_args(ann))
  else:
    ann_to_test = ann if ann != float else (int, float)

    if ann_to_test == Any: return

    if not isinstance(att, ann_to_test):
      raise TypeError(format_type_error(att_key, att, ann))

def validate_with_origin(origin, att_key, att, args):
    if origin == Union:
      return validate_union(att_key, att, args)
    if origin == Literal:
      return validate_literal(att_key, att, args)
    if origin == list:
      return validate_list(att_key, att, args[0])
    if origin == tuple:
      return validate_tuple(att_key, att, args)
    if origin == dict:
      return validate_dict(att_key, att, args)

    print('VALIDATION WITH ORIGIN NOT IMPLEMENTED:', att_key, att, args, origin)

def validate_dict(att_key, att, anns):
  if not isinstance(att, dict):
    raise TypeError(format_type_error(att_key, att, dict))

  key_class = anns[0]
  val_class = anns[1]
  for key in att:
    try:
      validate_any('', key, key_class)
    except Exception as e:
      raise TypeError(f'({att_key}) dict key ' + e.args[0])

    try:
      validate_any('', att[key], val_class)
    except Exception as e:
      raise TypeError(f'({att_key}) dict key ({key}) value ' + e.args[0])

def validate_literal(att_key, att, options):
  if att not in options:
    raise TypeError(f'({att_key}) of value ({att}) is not one of the valid options: ({options})')

def validate_union(att_key, att, anns):
  for ann in anns:
    try:
      validate_any(att_key, att, ann)
      return
    except:
      pass
  
  error_message = f'({att_key}) of value ({att}) expected to have one of the types ({anns}) but have type ({type(att).__name__})'
  raise TypeError(error_message)

def validate_tuple(att_key, att, ann):
  if not isinstance(att, tuple):
    raise TypeError(format_type_error(att_key, att, tuple))
  
  if ann == Any: return

  att_len = len(att)
  ann_len = len(ann)
  if att_len != ann_len:
    raise TypeError(f'{att_key} ({att}) tuple has length of {att_len} and should be {ann_len}')

  for i in range(ann_len):
    try:
      validate_any(i, att[i], ann[i])
    except Exception as e:
      raise(TypeError(f'({att_key}) tuple in position ' + e.args[0]))

def validate_list(att_key, att_list, list_item_type):
  if not isinstance(att_list, list):
    raise TypeError(format_type_error(att_key, att_list, list))
  
  for i in range(len(att_list)):
    try:
      validate_any(i, att_list[i], list_item_type)
    except Exception as e:
      raise TypeError(f'({att_key}) list in position '+e.args[0])

def format_type_error(att_key, att, ann) -> str:
  if att_key == '':
    return f'({att}) expected to have type ({ann.__name__}) but have type ({type(att).__name__})'
  return f'({att_key}) of value ({att}) expected to have type ({ann.__name__}) but have type ({type(att).__name__})'
