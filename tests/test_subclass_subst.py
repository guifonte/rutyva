import unittest
from dataclasses import dataclass
from rutyva import BaseModel

@dataclass
class A(BaseModel):
  a_str: str
  a_int: int

@dataclass
class B(BaseModel):
  a: A

@dataclass
class ASub(A):
  a_float: float

@dataclass
class C(BaseModel):
  pass

class TestSubclassSubst(unittest.TestCase):
  def test_subclass_subst_none(self):
    d = {
      'a': {
        'a_str': 'lorem ipslum',
        'a_int': 13213
      }
    }
    b = B.from_dict(d)
  
  def test_subclass_subst_ASub(self):
    d = {
      'a': {
        'a_str': 'lorem ipslum',
        'a_int': 13213,
        'a_float': 1.23421
      }
    }
    b = B.from_dict(d, subclass_subst=[(A, ASub)])
    self.assertEqual(b.a.a_float, 1.23421)

  def test_subclass_subst_C(self):
    d = {
      'a': {
        'a_str': 'lorem ipslum',
        'a_int': 13213,
        'a_float': 1.23421
      }
    }
    with self.assertRaises(TypeError) as cm:
      b = B.from_dict(d, subclass_subst=[(C, ASub)])
      self.assertEqual(cm.exception.args[0], 'ASub is not a subclass of C')

  def test_subclass_subst_ASubdict_none_list(self):
    d = {
      'a': {
        'a_str': 'lorem ipslum',
        'a_int': 13213,
        'a_float': 1.23421
      }
    }
    b = B.from_dict(d, subclass_subst=None)
    with self.assertRaises(Exception):
      print(b.a.a_float)
