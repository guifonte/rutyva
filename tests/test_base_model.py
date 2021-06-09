from copy import deepcopy 
from dataclasses import dataclass
from typing import Union
import unittest
from xuriprafunction.domain.models.base_model import BaseModel

a_int = 5
a_float = 5.454234
a_str = 'lorem'
a_bool = True
a_dict_str_str = {'key': 'value'}
a_tuple_int_str_bool = (a_int, a_str, a_bool)
a_list = [a_int, a_int, a_str, a_dict_str_str]

test_simple_att_params = {
  'a_int': a_int,
  'a_float': a_float,
  'a_str': a_str,
  'a_bool': a_bool,
  'a_tuple': a_tuple_int_str_bool,
  'a_list': a_list
}

@dataclass
class BMSimpleAtt(BaseModel):
  a_int: int
  a_float: float
  a_str: str
  a_bool: bool
  a_tuple: tuple
  a_list: list

class TestBMSimpleAtt(unittest.TestCase):
  def setUp(self) -> None:
    self.test_simple_att_params = deepcopy(test_simple_att_params)

  def test_right(self):
    '''
    Should not raise Exception if all parameters have the right type
    '''
    test = BMSimpleAtt(**self.test_simple_att_params)
  
  def test_wrong_not_mutable(self):
    '''
    Should raise TypeError if a not mutable parameter is wrong
    '''
    self.test_simple_att_params['a_str'] = a_int
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params)
  
  def test_missing_params(self):
    '''
    Should raise TypeError if a parameter is missing
    '''
    self.test_simple_att_params.pop('a_str')
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params)

  def test_extra_params(self):
    '''
    Should raise TypeError if there is any extra parameter
    '''
    self.test_simple_att_params['extra_str'] = a_int
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params)

  def test_wrong_mutable(self):
    '''
    Should raise TypeError if a mutable parameter is of wrong type
    '''
    self.test_simple_att_params['a_list'] = a_tuple_int_str_bool
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params)
  
  def test_float_is_int(self):
    '''
    Should not raise error if a int value is used in a float parameter
    '''
    self.test_simple_att_params['a_float'] = a_int
    test = BMSimpleAtt(**self.test_simple_att_params)

  def test_int_is_bool(self):
    '''
    Should not raise error if a bool value is used in a int parameter
    '''
    self.test_simple_att_params['a_int'] = a_bool
    test = BMSimpleAtt(**self.test_simple_att_params)
  
  def test_bool_is_int(self):
    '''
    Should raise error if a bool value is used in a int parameter
    '''
    self.test_simple_att_params['a_bool'] = a_int
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params) 

  def test_int_is_float(self):
    '''
    Should raise TypeError if a float value is used in an int parameter
    '''
    self.test_simple_att_params['a_int'] = a_float
    with self.assertRaises(TypeError):
      test = BMSimpleAtt(**self.test_simple_att_params)


class TestBMSimpleAttFromDict(unittest.TestCase):
  def setUp(self) -> None:
    self.test_simple_att_params = deepcopy(test_simple_att_params)

  def test_right(self):
    '''
    Should not raise TypeError if dict is right and be equal to input when transformed to dict
    '''
    test = BMSimpleAtt.from_dict(self.test_simple_att_params)
    test_dict = test.to_dict()
    self.assertDictEqual(self.test_simple_att_params, test_dict)

  def test_wrong_not_mutable(self):
    '''
    Should raise error if created from dict with a wrong not mutable paramete
    '''
    self.test_simple_att_params['a_int'] = a_dict_str_str
    with self.assertRaises(TypeError):
      test = BMSimpleAtt.from_dict(self.test_simple_att_params)

  def test_wrong_mutable(self):
    '''
    Should raise TypeError if created from dict with a wrong mutable parameter
    '''
    self.test_simple_att_params['a_tuple'] = a_dict_str_str
    with self.assertRaises(TypeError):
      test = BMSimpleAtt.from_dict(self.test_simple_att_params)

  def test_missing_params(self):
    '''
    Should raise TypeError if created from dict with a missing parameter
    '''
    self.test_simple_att_params.pop('a_tuple')
    with self.assertRaises(TypeError):
      test = BMSimpleAtt.from_dict(self.test_simple_att_params)

  def test_extra_params(self):
    '''
    Should raise TypeError if created from dict with extra parameters
    '''
    self.test_simple_att_params['extra_tuple'] = a_tuple_int_str_bool
    with self.assertRaises(TypeError):
      test = BMSimpleAtt.from_dict(self.test_simple_att_params)
      
  def test_float_is_int(self):
    '''
    Should not raise error if a int parameter is used in a float attribute
    '''
    self.test_simple_att_params['a_float'] = a_int
    test = BMSimpleAtt.from_dict(self.test_simple_att_params)
    test_dict = test.to_dict()
    self.assertDictEqual(self.test_simple_att_params, test_dict)

  def test_int_is_float(self):
    '''
    Should raise TypeError if a float parameter is used in a int attribute
    '''
    self.test_simple_att_params['a_int'] = a_float
    with self.assertRaises(TypeError) as cm:
      test = BMSimpleAtt.from_dict(self.test_simple_att_params)

    # e = cm.exception
    # print(e)


normal_class_params = {
  'a_int': a_int,
  'a_str': a_str
}

bm_normal_class_att_params = {
  'a_int': a_int,
  'a_normal_class_obj': None
}

class NormalClass:
  def __init__(self, a_int: int, a_str: str) -> None:
    self.a_int = a_int
    self.a_str = a_str

@dataclass
class BMNormalClassAtt(BaseModel):
  a_int: int
  a_normal_class_obj: NormalClass

class TestBMNormalClassAtt(unittest.TestCase):
  def setUp(self) -> None:
    self.bm_normal_class_att_params = deepcopy(bm_normal_class_att_params)
    self.normal_class_params = deepcopy(normal_class_params)

  def test_right(self):
    '''
    Should not raise error if the the parameters are right
    '''
    self.bm_normal_class_att_params['a_normal_class_obj'] = NormalClass(**self.normal_class_params)
    test = BMNormalClassAtt(**self.bm_normal_class_att_params)

  def test_wrong_in_normal_class(self):
    '''
    Should not raise TypeError if a parameter is wrong in the normal class
    '''
    self.normal_class_params['a_int']=a_str
    self.bm_normal_class_att_params['a_normal_class_obj'] = NormalClass(**self.normal_class_params)
    test = BMNormalClassAtt(**self.bm_normal_class_att_params)
  
  def test_wrong(self):
    '''
    Should raise TypeError if a parameter is wrong in the BM class
    '''
    self.bm_normal_class_att_params['a_int'] = NormalClass(**self.normal_class_params)
    self.bm_normal_class_att_params['a_normal_class_obj'] = NormalClass(**self.normal_class_params)
    with self.assertRaises(TypeError):
      test = BMNormalClassAtt(**self.bm_normal_class_att_params)
  
  def test_wrong_normal_class(self):
    '''
    Should raise TypeError if the normal class parameter is wrong in the BM class
    '''
    self.bm_normal_class_att_params['a_normal_class_obj'] = a_int
    with self.assertRaises(TypeError):
      test = BMNormalClassAtt(**self.bm_normal_class_att_params)

  def test_right_from_dict(self):
    '''
    Should not raise error if created from dict with right parameters
    '''
    self.bm_normal_class_att_params['a_normal_class_obj'] = self.normal_class_params
    test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)

  def test_right_from_dict_with_object(self):
    '''
    Should not raise error if created from dict with right parameters and class object
    '''
    self.bm_normal_class_att_params['a_normal_class_obj'] = NormalClass(**self.normal_class_params)
    test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)

  def test_wrong_in_normal_class_from_dict(self):
    '''
    Should not raise TypeError if created from dict with a parameter with wrong type in the normal class
    '''
    self.normal_class_params['a_int']=a_str
    self.bm_normal_class_att_params['a_normal_class_obj'] = self.normal_class_params
    test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)
  
  def test_wrong_from_dict(self):
    '''
    Should raise TypeError if created from dict with a parameter with wrong type in the BM class
    '''
    self.bm_normal_class_att_params['a_int'] = NormalClass(**self.normal_class_params)
    self.bm_normal_class_att_params['a_normal_class_obj'] = self.normal_class_params
    with self.assertRaises(TypeError):
      test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)
  
  def test_wrong_normal_class_from_dict(self):
    '''
    Should raise TypeError if created from dict with the normal class parameter of the wrong type in the BM class
    '''
    self.bm_normal_class_att_params['a_normal_class_obj'] = a_int
    with self.assertRaises(TypeError):
      test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)

  def test_wrong_normal_class_with_extra_params_from_dict(self):
    '''
    Should raise TypeError if created from dict with the normal class parameter of the wrong type(extra parameters) in the BM class
    '''
    self.normal_class_params['extra_int'] = a_int
    self.bm_normal_class_att_params['a_normal_class_obj'] = self.normal_class_params
    with self.assertRaises(TypeError):
      test = BMNormalClassAtt.from_dict(self.bm_normal_class_att_params)


normal_dataclass_params = {
  'a_int': a_int,
  'a_str': a_str
}

bm_normal_dataclass_att_params = {
  'a_int': a_int,
  'a_normal_dataclass_obj': None
}
@dataclass
class NormalDataClass:
  a_int: int
  a_str: str

@dataclass
class BMNormalDataClassAtt(BaseModel):
  a_int: int
  a_normal_dataclass_obj: NormalDataClass

class TestBMNormalDataClassAtt(unittest.TestCase):
  def setUp(self) -> None:
    self.bm_normal_dataclass_att_params = deepcopy(bm_normal_dataclass_att_params)
    self.normal_dataclass_params = deepcopy(normal_dataclass_params)

  def test_right(self):
    '''
    Should not raise error if the the parameters are right
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalDataClass(**self.normal_dataclass_params)
    test = BMNormalDataClassAtt(**self.bm_normal_dataclass_att_params)

  def test_wrong_in_normal_class(self):
    '''
    Should not raise TypeError if a parameter is wrong in the normal class
    '''
    self.normal_dataclass_params['a_int']=a_str
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalDataClass(**self.normal_dataclass_params)
    test = BMNormalDataClassAtt(**self.bm_normal_dataclass_att_params)
  
  def test_wrong(self):
    '''
    Should raise TypeError if a parameter is wrong in the BM class
    '''
    self.bm_normal_dataclass_att_params['a_int'] = NormalDataClass(**self.normal_dataclass_params)
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalDataClass(**self.normal_dataclass_params)
    with self.assertRaises(TypeError):
      test = BMNormalDataClassAtt(**self.bm_normal_dataclass_att_params)
  
  def test_wrong_normal_class(self):
    '''
    Should raise TypeError if the normal class parameter is wrong in the BM class
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalClass(**self.normal_dataclass_params)
    with self.assertRaises(TypeError):
      test = BMNormalDataClassAtt(**self.bm_normal_dataclass_att_params)

  def test_right_from_dict(self):
    '''
    Should not raise error if created from dict with right parameters
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = self.normal_dataclass_params
    test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)
  
  def test_right_from_dict_with_object(self):
    '''
    Should not raise error if created from dict with right parameters and dataclass object
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalDataClass(**self.normal_dataclass_params)
    test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)

  def test_wrong_in_normal_dataclass_from_dict(self):
    '''
    Should not raise TypeError if created from dict with a parameter with wrong type in the normal class
    '''
    self.normal_dataclass_params['a_int']=a_str
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = self.normal_dataclass_params
    test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)
  
  def test_wrong_from_dict(self):
    '''
    Should raise TypeError if created from dict with a parameter with wrong type in the BM class
    '''
    self.bm_normal_dataclass_att_params['a_int'] = NormalDataClass(**self.normal_dataclass_params)
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = self.normal_dataclass_params
    with self.assertRaises(TypeError):
      test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)
  
  def test_wrong_normal_dataclass_from_dict(self):
    '''
    Should raise TypeError if created from dict with the normal dataclass parameter of the wrong type in the BM class
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = a_int
    with self.assertRaises(TypeError):
      test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)

  def test_right_from_dict_with_object(self):
    '''
    Should not raise error if created from dict with right parameters and dataclass object
    '''
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = NormalDataClass(**self.normal_dataclass_params)
    test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)

  def test_wrong_normal_class_with_extra_params_from_dict(self):
    '''
    Should raise TypeError if created from dict with the normal class parameter of the wrong type(extra parameters) in the BM class
    '''
    self.normal_dataclass_params['extra_int'] = a_int
    self.bm_normal_dataclass_att_params['a_normal_dataclass_obj'] = self.normal_dataclass_params
    with self.assertRaises(TypeError):
      test = BMNormalDataClassAtt.from_dict(self.bm_normal_dataclass_att_params)


bm_bmclass_att_params = {
  'a_int': a_int,
  'a_bm_simple_att_obj': None
}

@dataclass
class BMBMClassAtt(BaseModel):
  a_int: int
  a_bm_simple_att_obj: BMSimpleAtt

class TestBMBMClassAtt(unittest.TestCase):
  def setUp(self) -> None:
    self.bm_bmclass_att_params = deepcopy(bm_bmclass_att_params)
    self.bm_simple_att_obj = deepcopy(test_simple_att_params)

  def test_right(self):
    '''
    Should not raise error if the parameters are right
    '''
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = BMSimpleAtt(**self.bm_simple_att_obj)
    test = BMBMClassAtt(**self.bm_bmclass_att_params)

  def test_right_subclass(self):
    '''
    Should not raise error if the parameters are subclass
    '''
    @dataclass
    class BMSimpleAttSubclass(BMSimpleAtt):
      b_int: int

    self.bm_simple_att_obj['b_int'] = a_int
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = BMSimpleAttSubclass(**self.bm_simple_att_obj)
    test = BMBMClassAtt(**self.bm_bmclass_att_params)

  def test_subclass_dict_from_dict(self):
    '''
    Should raise TypeError if created from dict and a parameter is a dict of subclass
    '''
    @dataclass
    class BMSimpleAttSubclass(BMSimpleAtt):
      b_int: int

    self.bm_simple_att_obj['b_int'] = a_int
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = self.bm_simple_att_obj
    with self.assertRaises(TypeError):
      test = BMBMClassAtt.from_dict(self.bm_bmclass_att_params)

  def test_subclass_object_from_dict(self):
    '''
    Should not raise TypeError if created from dict and a parameter is a object of subclass
    '''
    @dataclass
    class BMSimpleAttSubclass(BMSimpleAtt):
      b_int: int

    self.bm_simple_att_obj['b_int'] = a_int
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = BMSimpleAttSubclass.from_dict(self.bm_simple_att_obj)
    
    test = BMBMClassAtt.from_dict(self.bm_bmclass_att_params)

  def test_wrong_value_in_bmclass_att_dict_from_dict(self):
    '''
    Should raise TypeError if created from dict and a parameter from the inner BMSimple class is wrong
    '''
    self.bm_simple_att_obj['a_list'] = a_tuple_int_str_bool
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = self.bm_simple_att_obj
    with self.assertRaises(TypeError):
      test = BMBMClassAtt.from_dict(self.bm_bmclass_att_params)

  def test_bmclass_dict_from_dict(self):
    '''
    Should not raise TypeError if created from dict with the parameter of type BMSimple is dict
    '''
    self.bm_bmclass_att_params['a_bm_simple_att_obj'] = self.bm_simple_att_obj
    test = BMBMClassAtt.from_dict(self.bm_bmclass_att_params)

class TestBMWithOriginTypes(unittest.TestCase):
  def setUp(self) -> None:
    pass

  def test_union_str_int(self):
    '''
    Should not raise TypeError if parameter type is within the Union
    '''
    @dataclass
    class BMClassUnion(BaseModel):
      a_union: Union[str, int]

    test = BMClassUnion(a_union=a_str)
    test2 = BMClassUnion(a_union=a_int)
    test3 = BMClassUnion.from_dict({'a_union': a_str})
    test3 = BMClassUnion.from_dict({'a_union': a_int})

  def test_union_list_BMSimpleAtt_int(self):
    '''
    Should not raise TypeError if parameter type is within the Union
    '''
    @dataclass
    class BMClassUnion(BaseModel):
      a_union: Union[list, BMSimpleAtt, int]

    test = BMClassUnion(a_union=a_list)
    test2 = BMClassUnion(a_union=a_int)
    test3 = BMClassUnion(a_union=BMSimpleAtt(**test_simple_att_params))

  def test_union_subclasses_from_dict1(self):
    '''
    Should not raise TypeError if parameter type is within the Union
    '''
    @dataclass
    class BMClassUnion(BaseModel):
      a_union: Union[list, BaseModel] 

    test3 = BMClassUnion(a_union=BMSimpleAtt(**test_simple_att_params))

  @unittest.expectedFailure
  def test_union_subclasses_from_dict2(self):
    '''
    Should not raise TypeError if parameter type is within the Union
    '''
    @dataclass
    class BMClassUnion(BaseModel):
      a_union: Union[list, BaseModel] 

    test = BMClassUnion.from_dict({'a_union': test_simple_att_params})
    test2 = BMClassUnion.from_dict({'a_union': a_list})

  def test_union_subclasses_from_dict3(self):
    '''
    Should not raise TypeError if parameter type is within the Union
    '''
    @dataclass
    class BMClassUnion(BaseModel):
      a_union: Union[list, BaseModel] 

    test3 = BMClassUnion(a_union=BMSimpleAtt(**test_simple_att_params)) 


### TEST WITH ORIGIN
# OK Union[X, Y]
# OK Union[X, Y, BaseModel]
# Union[Subclass1, Subclass2, class] from dict
# Union[List[BMclass], str]
# Optional[X] -> Union[X, NoneType]
# Literal[str, str, str]
# Literal[str, tuple, int]
# List[X]
# List[Union]
# dict[str, Any]
# dict[str, BM]
# dict[Union[int, tuple, str], list[str]]
# tuple[str, int, list]
# tuple[Union[str, list[str]], int, Literal[...] ]

if __name__=='__main__':
  unittest.main()