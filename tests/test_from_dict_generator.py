from typing import Optional
import unittest
from rutyva import BaseModel
from dataclasses import dataclass
from rutyva.from_dict_generator import gen_from_any

class TestFromDictGen(unittest.TestCase):
  def test_inner_BaseModel(self):
    @dataclass
    class TestInnerClass(BaseModel):
      a: int
    
    @dataclass
    class TestOuterClass(BaseModel):
      i: TestInnerClass

    d_val = {'i': {'a' : 1}}
    result = TestOuterClass.from_dict(d_val)

  def test_inner_Optional_BaseModel(self):
    @dataclass
    class TestInnerClass(BaseModel):
      a: int
    
    @dataclass
    class TestOuterClass(BaseModel):
      i: Optional[TestInnerClass]=None

    d_val = {'i': {'a' : 1}}
    result = TestOuterClass.from_dict(d_val)

  def test_inner_Optional_BaseModel_None(self):
    @dataclass
    class TestInnerClass(BaseModel):
      a: int
    
    @dataclass
    class TestOuterClass(BaseModel):
      i: Optional[TestInnerClass]=None

    d_val = {}
    result = TestOuterClass.from_dict(d_val)
 
if __name__=="__main":
  unittest.main()
 