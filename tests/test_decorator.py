import unittest
import inspect
from dataclasses import dataclass, is_dataclass


def val_dataclass(count=0):
  def wrapper(cls):
    for _ in range(count):
      print('test')

    return dataclass()(cls)
  
  return wrapper


class TestDecorator(unittest.TestCase):
  def test_wrapped_dataclass(self):
    @val_dataclass(2)
    class TestClass:
      i: int
      b: str
    
    test_obj = TestClass(i=1, b='bla')
    self.assertTrue(is_dataclass(test_obj))

    pass

  def test_instanciated_dataclass(self):
    class TestClass:
      i: int
      b: str
    
    test_dataclass = dataclass()(TestClass)
    test_obj = test_dataclass(10, 'a')
    self.assertTrue(is_dataclass(test_obj))
  
  def test_subclass_dataclass(self):
    def val_dataclass_wrap(count=0):
      def wrapper(cls):
        for _ in range(count):
          print('test')

        @dataclass
        class WrapDC(cls):
          pass
        return WrapDC
      
      return wrapper

    @val_dataclass_wrap
    class TestClass:
      '''
      Test Doc
      '''
      i: int
      b: str

    test_obj = TestClass()
    # self.assertTrue(is_dataclass(test_obj))


if __name__=='__main__':
  unittest.main()
