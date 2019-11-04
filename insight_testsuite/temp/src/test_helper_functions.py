#!/usr/bin/python3
from define_functions import *
import unittest

#This script will test my helper functions by
#1. Defining testing class that inherits from TestCase (aka a test case)
#2. Within each test case I will have a series of methods to test the inputs/outputs relative to expectations


class TestMyRound(unittest.TestCase):
    def test_myround_inputs(self):
        """
        Test that zero rounds to zero
        """
        data = 0
        result = my_round(data)
        self.assertEqual(result, 0)

        data = 0.00
        result = my_round(data)
        self.assertEqual(result,0)


        """
        Test that 1.5 rounds to 2
        """
        data = 1.5
        result = my_round(data)
        self.assertEqual(result,2)

        """
        Test that 2.5 rounds to 3
        """
        data = 2.5
        result = my_round(data)
        self.assertEqual(result,3)


    def test_badinput(self):

        """
        Test that negative or non-numeric input raises exception
        """

        # should raise an exception for an immutable sequence
        data = -4
        self.assertRaises(ValueError, my_round, data)

        # should raise an exception for an immutable sequence
        data = "kjsdf"
        self.assertRaises(ValueError, my_round, data)

class TestCleanWhitespace(unittest.TestCase):
    def test_input_notstring(self):
        self.assertRaises(ValueError, CleanWhitespace,True)
        self.assertRaises(ValueError, CleanWhitespace,False)
        self.assertRaises(ValueError, CleanWhitespace,5)

    def test_typicalcase(self):
        self.assertEqual(CleanWhitespace(' lkj  d '),'lkj d')    

    def test_nowhitespace(self):
        self.assertEqual(CleanWhitespace('lkj'),'lkj')
    def test_allwhitespace(self):
        self.assertEqual(CleanWhitespace('\t'),'')
        self.assertEqual(CleanWhitespace('\n'),'')
        self.assertEqual(CleanWhitespace('  \r '),'')
        self.assertEqual(CleanWhitespace(''),'')


class TestIncreaseMonthByOne(unittest.TestCase):

    """ 
    Test Input type is correct
    """
    def test_input_type(self):
        self.assertRaises(TypeError,IncreaseMonthByOne,'2019/08/01')
        

    """ 
    Test Input attributes are correct
    """
    def test_input_attributes(self):
        self.assertRaises(ValueError,
            IncreaseMonthByOne,
            datetime.datetime.strptime('08/02/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p"))
        self.assertRaises(ValueError,
            IncreaseMonthByOne,
            datetime.datetime.strptime('10/01/2019 12:00:00 PM',"%m/%d/%Y %I:%M:%S %p"))


    """ 
    Test output is as expected
    """
    def test_output(self):
        self.assertEqual(
            IncreaseMonthByOne(
                datetime.datetime.strptime('08/01/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p")
                ),
            datetime.datetime.strptime('09/01/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p"))
        self.assertEqual(
            IncreaseMonthByOne(
                datetime.datetime.strptime('09/01/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p")
                ),
            datetime.datetime.strptime('10/01/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p"))

        self.assertEqual(
            IncreaseMonthByOne(
                datetime.datetime.strptime('12/01/2019 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p")
                ),
            datetime.datetime.strptime('01/01/2020 12:00:00 AM',"%m/%d/%Y %I:%M:%S %p"))


class TestPadDictlistWithCustomValues(unittest.TestCase):
    """
    Test that wrong input type will throw an error
    """
    def test_input_type(self):
        self.assertRaises(TypeError,
            PadDictlistWithCustomValues,
            5
            )
    def test_input_type(self):
        self.assertRaises(TypeError,
            PadDictlistWithCustomValues,
            [2,3,4,5]
            )
    def test_input_type(self):
        self.assertRaises(TypeError,
            PadDictlistWithCustomValues,
            {'key1':3,"key2":[1,2,4]}
            )
    def test_input_type(self):
        self.assertRaises(TypeError,
            PadDictlistWithCustomValues,
            {'key':5}
            )
    def test_input_type(self):
        self.assertRaises(TypeError,
            PadDictlistWithCustomValues,
            ({'key':5},{'key2':5})
            )
    """
    Test that looking for a key:value pair that exists will return same input
    """
    

    def test_input_same(self):
        self.assertEqual(PadDictlistWithCustomValues(
            key = 'Key2', 
            value = None,
            my_dictlist = 
            [{"Key1":1,"Key2":None},{"Clave1":5}],
            key_to_impute = 'new_key',
            imputed_value = 3
            ),
        [{"Key1":1,"Key2":None},{"Clave1":5}]
        )


    """
    Test that looking for a key:value pair that does not exist will return correct augmented output
    """


    def test_input_different(self):
        self.assertEqual(PadDictlistWithCustomValues(
            key = 'Key2', 
            value = 4,
            my_dictlist = 
            [{"Key1":1,"Key2":None},{"Clave1":5, 'Key2':3}],
            key_to_impute = 'Key9',
            imputed_value = 3
            ),
        [{"Key1":1,"Key2":None},{"Clave1":5, 'Key2':3},{"Key1":1,"Key2":4, 'Key9':3}]
        
        )
if __name__ == '__main__':
    unittest.main()



