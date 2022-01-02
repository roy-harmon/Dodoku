from unittest import TestCase
import dodoku.recommend as recommend 

class RecommendTest(TestCase):
#-------------------------------------------------------------------------------
# -- Acceptance tests for op=recommend
# Interface Analysis
#    input:  URL with pattern https://name-of-server.com/dodoku?
#                        op=recommend
#                        &cell=
#                        &grid=
#                        &integrity=
#            op -> "recommend"
#            cell -> r'^([rR])(\d\d?)([cC])(\d\d?)$', where
#                        (\d\d?) is in range [1,15]
#                        and the entire reference refers to a valid grid cell;
#                        mandatory; 
#                        unvalidated
#            grid -> r'^(\[(-?\d,){152}-?\d\])$'; 
#                        mandatory;
#                        unvalidated
#            integrity -> r'^([\dabcdef]{8})$' and
#                        is substring of SHA-256 hash of grid in column-major order;
#                        mandatory;
#                        unvalidated
#    output: dictionary item of specific interest is status:
#        Normal:
#                grid -> r'^(\[(-?\d,){152}-?\d\])$'
#                integrity -> r'^([\dabcdef]{8})$' and
#                        is randomly selected substring of SHA-256 hash of grid in column-major order;
#                status -> r'^((ok)|(warning))$'
#        Abnormal
#                status -> r'^((error:).*)'
#
# Input grid integrity string: '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        
    def test_Recommend_010_ShouldReturnTwoValues(self):
        parms = {'op': 'recommend',
                'cell': 'r1c1',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        self.assertIn('recommendation', actualResult)
        self.assertEqual(type(actualResult['recommendation']), type([]))
        self.assertIn('status', actualResult)
        self.assertEqual(len(actualResult), 2)
        
    def test_Recommend_020_ValidParms_EmptyCell(self):
        parms = {'op': 'recommend',
                'cell': 'r1c1',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [3,6,7,9],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_030_ValidParms_UserCell(self):
        parms = {'op': 'recommend',
                'cell': 'r1c1',
                'integrity': 'cb81722d',
                'grid': '[3,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [3,6,7,9],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_040_ValidParms_ImmutableCell(self):
        parms = {'op': 'recommend',
                'cell': 'r1c2',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_050_ValidParms_MultipleRecs(self):
        parms = {'op': 'recommend',
                'cell': 'r1c1',
                'integrity': 'b22139cd',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                    '-8,6,-1,-9,0,0,0,0,-5,' + \
                    '0,0,0,0,-3,0,0,-1,0,' + \
                    '0,-3,0,0,0,0,-4,0,-6,' + \
                    '-5,0,-9,0,0,0,0,0,-7,' + \
                    '0,0,0,0,0,0,-2,-8,0,' + \
                    '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                    '0,0,-6,0,0,-3,0,0,4,-2,0,0,-1,0,-9,' + \
                    '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,4,-5,' + \
                                   '0,0,-6,0,0,0,0,-9,0,' + \
                                   '-2,0,0,0,0,0,-4,0,-8,' + \
                                   '-7,0,-9,0,0,0,0,0,0,' + \
                                    '0,-5,0,0,-9,0,0,0,4,' + \
                                    '-4,0,0,-6,0,-3,-9,0,0,' + \
                                    '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [3,7,9],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_060_ValidParms_NoValidRecs(self):
        parms = {'op': 'recommend',
                'cell': 'r1c1',
                'integrity': '0ac4199c',
                'grid': '[0,-2,0,0,-1,0,3,-4,0,-8,6,-1,-9,0,0,0,0,-5,0,9,0,0,' + \
                '-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,' + \
                '0,0,-2,-8,0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,7,0,-6,0,0,-3,' + \
                '0,0,4,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,4,-5,0,0,' + \
                '-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,0,0,-5,' + \
                '0,0,-9,0,0,0,4,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
            
    def test_Recommend_070_ValidParms_OverlapCell(self):
        parms = {'op': 'recommend',
                'cell': 'r8c8',
                'integrity': '862de7e8',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,' + \
                '-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,' + \
                '0,0,-2,-8,0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0' + \
                ',0,4,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,4,-5,0,0,-6,' + \
                '0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,0,0,-5,0,0,' + \
                '-9,0,0,0,4,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [7],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_070_ValidParms_OverlapCell(self):
        parms = {'op': 'recommend',
                'cell': 'r8c8',
                'integrity': '862de7e8',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,' + \
                '-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,' + \
                '0,0,-2,-8,0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0' + \
                ',0,4,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,4,-5,0,0,-6,' + \
                '0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,0,0,-5,0,0,' + \
                '-9,0,0,0,4,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'recommendation': [7],'status':'ok'}
        self.assertEqual(expectedResult['recommendation'], actualResult['recommendation'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_910_InvalidCell(self):
        parms = {'op': 'recommend',
                'cell': 'r1c10',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_920_InvalidGrid(self):
        parms = {'op': 'recommend',
                'cell': 'r1c10',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-10]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Recommend_930_InvalidIntegrity(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73424',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,' + \
                         '-8,0,-1,-9,0,0,0,0,-5,' + \
                         '0,0,0,0,-3,0,0,-1,0,' + \
                         '0,-3,0,0,0,0,-4,0,-6,' + \
                         '-5,0,-9,0,0,0,0,0,-7,' + \
                         '0,0,0,0,0,0,-2,-8,0,' + \
                         '-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,' + \
                         '0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,' + \
                         '0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,' + \
                         '0,0,-6,0,0,0,0,-9,0,' + \
                         '-2,0,0,0,0,0,-4,0,-8,' + \
                         '-7,0,-9,0,0,0,0,0,0,' + \
                         '0,-5,0,0,-9,0,0,0,0,' + \
                         '-4,0,0,-6,0,-3,-9,0,0,' + \
                         '0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = recommend._recommend(parms)
        expectedResult = {'status': 'error: invalid integrity'}
        self.assertEqual(expectedResult['status'], actualResult['status'])