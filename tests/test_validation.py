from typing import Any, Union, Optional
import unittest
from rutyva import validation

PRINT_EXCEPTION = True

class TestBasic(unittest.TestCase):
  def test_str(self):
    key = 'test_str'
    value = 'a string'
    ann = str
    validation.validate_any(key, value, ann)

  def test_str_att_int(self):
    key = 'test_att'
    value = 1
    ann = str

    expected_error_message = '(test_att) of value (1) expected to have type (str) but have type (int)'
    assertRaisesTypeErrorAndExceptionMessage(self, (key, value, ann), expected_error_message)


class TestList(unittest.TestCase):
  def test_list_li_str(self):
    key = 'test_list_of_str'
    value = ['a', 'b', 'c', 'd']
    ann = list[str]
    validation.validate_any(key, value, ann)

  def test_list_li_str_one_item_int(self):
    key = 'test_list_of_str'
    value = ['a', 'b', 'c', 1]
    ann = list[str]
    a = tuple[Union[str, int], list[tuple[str, str, float]], Optional[dict[str, Any]]]
    expected_error_message = '(test_list_of_str) list in position (3) of value (1) expected to have type (str) but have type (int)'
    assertRaisesTypeErrorAndExceptionMessage(self, (key, value, ann), expected_error_message)

  def test_list_not_list(self):
    key = 'test_list'
    value = 'not a list, just a string'
    ann = list

    expected_error_message = '(test_list) of value (not a list, just a string) expected to have type (list) but have type (str)'
    assertRaisesTypeErrorAndExceptionMessage(self, (key, value, ann), expected_error_message)

  def test_list_li_Any(self):
    key = 'test_list_of_any'
    value = ['str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla')]
    ann = Any

    validation.validate_list(key, value, ann)

class TestTuple(unittest.TestCase):
  def test_tuple(self):
    key = 'test_tuple'
    value = ('str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla'))
    ann = Any

    validation.validate_any(key, value, ann)

  def test_tuple_Any(self):
    key = 'test_tuple'
    value = ('str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla'))
    ann = Any

    validation.validate_tuple(key, value, ann)

def print_exception(string):
  if PRINT_EXCEPTION:
    print(string)

def assertRaisesTypeErrorAndExceptionMessage(self, args, expected_error_message):
    with self.assertRaises(TypeError) as cm:
      validation.validate_any(*args)

    e_message = cm.exception.args[0]
    
    print_exception(e_message)
    self.assertEqual(e_message, expected_error_message)

a = tuple[Union[str, int], list[tuple[str, str, float]], Optional[dict[str, Any]]]


if __name__=="__main":
  unittest.main()