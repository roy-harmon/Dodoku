'''
    Created on Sept 28, 2021
    
    @author:    Roy Harmon
'''
from unittest import TestCase
import dodoku.create as create 

class CreateTest(TestCase):
        
    def test_Create_010_ShouldReturnThreeValues(self):
        parms = {'op': 'create','level': '1'}
        actualResult = create._create(parms)
        self.assertIn('grid', actualResult)
        self.assertIn('integrity', actualResult)
        self.assertIn('status', actualResult)
        self.assertEqual(len(actualResult), 3)
        
    def test_Create_020_ShouldCreateWithLowLevel(self):
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1], \
            'integrity': 'e8318e73', 'status': 'ok'}
        parms = {'op': 'create', 'level': '1'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_030_ShouldCreateWithMidLevel(self):
        expectedResult = {'grid': [0,-6,0,0,0,0,0,-5,-9,-9,-3,0,-4,-8,0,0,0,0,0,0,0,0,0,\
            -7,-3,0,0,0,-5,0,0,-1,0,0,-4,-6,0,0,0,0,0,-6,0,-9,0,0,-8,-1,-2,0,0,0,0,0,0,0,0,\
            0,-7,0,0,0,0,0,0,0,0,-5,0,-8,0,-4,0,0,-1,0,0,0,-7,0,0,-6,0,-2,0,-9,0,0,0,0,0,0,\
            0,0,-5,0,0,0,0,0,0,0,0,0,-9,-5,-3,0,0,-7,0,-4,0,0,0,0,0,-5,-8,0,0,-1,0,0,-9,0,0,\
            0,-2,-1,0,0,0,0,0,0,0,0,0,-9,-8,0,-6,-1,-6,-1,0,0,0,0,0,-7,0], \
            'integrity': 'cfa48f72', 'status': 'ok'}
        parms = {'op': 'create', 'level': '2'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '6fcd71ef7722e7573d2f607a35cfa48f72b03c4cea135ac31f7ef73a58e50a8a'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_040_ShouldCreateWithHighLevel(self):
        expectedResult = {'grid': [0,0,0,0,-6,0,0,0,0,0,0,0,-4,0,-9,0,0,0,0,0,-9,-7,0,-5,-1,0,0,0,-5,-2,0,\
            -7,0,-8,-9,0,-9,0,0,-5,0,-2,0,0,-4,0,-8,-3,0,-4,0,-7,-2,0,0,0,-1,-2,0,-8,0,0,0,\
            0,-3,0,0,0,0,0,0,0,-6,0,-4,0,0,0,-8,0,-7,0,0,0,0,0,0,0,-5,0,0,0,0,-1,0,-6,-3,0,\
            0,0,-9,-8,0,-5,0,-1,-2,0,-2,0,0,-7,0,-1,0,0,-3,0,-4,-3,0,-8,0,-6,-5,0,0,0,-7,-3,\
            0,-5,-9,0,0,0,0,0,-4,0,-2,0,0,0,0,0,0,0,-6,0,0,0,0], \
           'integrity': '31057f94', 'status': 'ok'}
        parms = {'op': 'create', 'level': '3'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = 'eb572835ffe2015c731057f94d46fa77430ad6fd332abb0d7dd39d5f2ccadea9'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_050_ShouldCreateWithNoLevel(self):
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1], \
            'integrity': 'e8318e73', 'status': 'ok'}
        parms = {'op': 'create', 'level': ''}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_060_ShouldCreateWithMissingLevel(self):
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1], \
            'integrity': 'e8318e73', 'status': 'ok'}
        parms = {'op': 'create'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_070_ShouldReturnStatisticallyProperIntegrityValue(self):
        parms = {'op': 'create', 'level': '1'}
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        stringDictionary = {}
        samplesCount = 57
        for _ in range(samplesCount):
            actualResult = create._create(parms)
            integrityString = actualResult['integrity']
            if integrityString in stringDictionary:
                stringDictionary[integrityString] += 1
            else:
                stringDictionary.update({integrityString: 1})
            self.assertTrue(integrityString in hashString)
        for subString in stringDictionary:
            self.assertLessEqual(stringDictionary[subString], 6, "Substring " + subString \
                 + " appeared " + str(stringDictionary[subString]) + " times!")
            
    def test_Create_080_ShouldReturnStatusOK(self):
        parms = {'op': 'create','level': '1'}
        actualResult = create._create(parms)
        self.assertIn('status', actualResult)
        self.assertEqual(actualResult['status'], 'ok')
        
    def test_Create_090_ShouldIgnoreCaseSensitiveLevel(self):
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1], \
            'integrity': 'e8318e73', 'status': 'ok'}
        parms = {'op': 'create', 'Level': '3'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_100_ShouldIgnoreExtraParms(self):
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1], \
            'integrity': 'e8318e73', 'status': 'ok'}
        parms = {'op': 'create', 'extraneous': '3'}
        actualResult = create._create(parms)
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Create_910_ShouldErrorOnNonNumericLevel(self):
        parms = {'op': 'create', 'level': 'a'}
        expectedResult = {'status': 'error: invalid level'}
        actualResult = create._create(parms)
        self.assertDictEqual(expectedResult, actualResult)
        
    def test_Create_920_ShouldErrorOnNonIntLevel(self):
        parms = {'op': 'create', 'level': '1.2'}
        expectedResult = {'status': 'error: invalid level'}
        actualResult = create._create(parms)
        self.assertDictEqual(expectedResult, actualResult)
        
    def test_Create_930_ShouldErrorOnTooLowLevel(self):
        parms = {'op': 'create', 'level': '0'}
        expectedResult = {'status': 'error: invalid level'}
        actualResult = create._create(parms)
        self.assertDictEqual(expectedResult, actualResult)
        
    def test_Create_930_ShouldErrorOnTooHighLevel(self):
        parms = {'op': 'create', 'level': '4'}
        expectedResult = {'status': 'error: invalid level'}
        actualResult = create._create(parms)
        self.assertDictEqual(expectedResult, actualResult)