import unittest
from rutyva import BaseModel
from dataclasses import dataclass
from rutyva.from_dict_generator import gen_from_any

class TestFromDictGen(unittest.TestCase):
  def test_inner_BaseModel(self):
    @dataclass
    class TestClass(BaseModel):
      a: int

    d_val = {'a' : 1}
    result = gen_from_any(d_val, TestClass)

 
if __name__=="__main":
  unittest.main()
 