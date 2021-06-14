from typing import Any, Union, Optional
import unittest
from rutyva import validation

PRINT_EXCEPTION = True

class TestBasic(unittest.TestCase):
  def test_str(self):
    value = 'a string'
    ann = str
    validation.validate_var(value, ann)

  def test_str_att_int(self):
    value = 1
    ann = str

    expected_error_message = '(1) is (int), but should be (str)'
    assertRaisesTypeErrorAndExceptionMessage(self, (value, ann), expected_error_message)


class TestList(unittest.TestCase):
  def test_list_li_str(self):
    value = ['a', 'b', 'c', 'd']
    ann = list[str]
    validation.validate_var(value, ann)

  def test_list_li_str_one_item_int(self):
    value = ['a', 'b', 'c', 1]
    ann = list[str]
    a = tuple[Union[str, int], list[tuple[str, str, float]], Optional[dict[str, Any]]]
    expected_error_message = 'error in position (3): (1) is (int), but should be (str)'
    assertRaisesTypeErrorAndExceptionMessage(self, (value, ann), expected_error_message)

  def test_list_not_list(self):
    value = 'not a list, just a string'
    ann = list

    expected_error_message = '(not a list, just a string) is (str), but should be (list)'
    assertRaisesTypeErrorAndExceptionMessage(self, (value, ann), expected_error_message)

  def test_list_li_Any(self):
    value = ['str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla')]
    ann = list[Any]

    validation.validate_var(value, ann)

class TestTuple(unittest.TestCase):
  def test_tuple(self):
    value = ('str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla'))
    ann = tuple

    validation.validate_var(value, ann)

  def test_tuple_Any(self):
    value = ('str', 1, {'a': (1, 2)}, [1, 2, 3], Exception('blabla'))
    ann = tuple[Any, Any, Any, Any, Any]

    validation.validate_var(value, ann)

def print_exception(string):
  if PRINT_EXCEPTION:
    print(string)

def assertRaisesTypeErrorAndExceptionMessage(self, args, expected_error_message):
    with self.assertRaises(TypeError) as cm:
      validation.validate_var(*args)

    e_message = cm.exception.args[0]
    
    print_exception(e_message)
    self.assertEqual(e_message, expected_error_message)

a = tuple[Union[str, int], list[tuple[str, str, float]], Optional[dict[str, Any]]]


if __name__=="__main":
  unittest.main()