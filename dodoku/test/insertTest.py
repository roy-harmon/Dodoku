'''
    Created on Oct 20, 2021
    
    @author:    Roy Harmon
'''
from unittest import TestCase
import dodoku.insert as insert 

class InsertTest(TestCase):
#-------------------------------------------------------------------------------
# -- Acceptance tests for op=insert
# Interface Analysis
#    input:  URL with pattern https://name-of-server.com/dodoku?
#                        op=insert
#                        &cell=
#                        &value=
#                        &grid=
#                        &integrity=
#            op -> "insert"
#            cell -> r'^([rR])(\d\d?)([cC])(\d\d?)$', where
#                        (\d\d?) is in range [1,15]
#                        and the entire reference refers to a valid grid cell;
#                        mandatory; 
#                        unvalidated
#            value -> r'^([123456789])$'; 
#                        optional, defaults to 0; 
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

#            BVA for cell
#                010 - return grid, integrity, status
#                015 - low row, low col; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                020 - low row, high col; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                025 - high row, low col; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                030 - high row, high col; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                035 - overlapping grid row and col; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                040 - RxCy; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                045 - rxcy; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                910 - below bound row; other parms nominal
#                    result:  status=error:
#                912 - above bound row; other parms nominal
#                    result:  status=error:
#                914 - non-int row; other parms nominal
#                    result:  status=error:
#                916 - missing row; other parms nominal
#                    result:  status=error:
#                918 - below bound col; other parms nominal
#                    result:  status=error:
#                920 - above bound col; other parms nominal
#                    result:  status=error:
#                922 - non-int col; other parms nominal
#                    result:  status=error:
#                924 - missing col; other parms nominal
#                    result:  status=error:
#                926 - extraneous items in cell parm; other parms nominal
#                    result:  status=error:
#                928 - outside upper bound rc; other parms nominal
#                    result:  status=error:
#                930 - outside lower bound rc; other parms nominal
#                    result:  status=error:
#                932 - reference to immutable cell; other parms nominal
#                    result:  status=error:
#                934 - missing cell value; other parms nominal
#                    result:  status=error:
#                936 - missing cell parm; other parms nominal
#                    result:  status=error:

#            BVA for value
#                055 - nominal value, obeys rules; other parms nominal
#                    result: valid grid, valid integrity, status=ok
#                060 - nominal value, violates rules; other parms nominal
#                    result: valid grid, valid integrity, status=warning
#                065 - low bound value, obeys rules; other parms nominal
#                    result: valid grid, valid integrity, status=ok
#                070 - high bound value, obeys rules; other parms nominal
#                    result: valid grid, valid integrity, status=ok
#                080 - missing value value; other parms nominal
#                    result: valid grid, valid integrity, status=ok
#                085 - missing value parm; other parms nominal
#                    result: valid grid, valid integrity, status=ok
#                940 - non-int value; other parms nominal
#                    result:  status=error:
#                942 - below bound value; other parms nominal
#                    result:  status=error:
#                944 - above bound value; other parms nominal
#                    result:  status=error:

#            BVA for grid
#                090 - nominal grid; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                950 - short grid; other parms nominal
#                    result:  status=error:
#                955 - long grid; other parms nominal
#                    result:  status=error:
#                960 - grid with non-ints; other parms nominal
#                    result:  status=error
#                965 - grid with out-of-bound ints; other parms nominal
#                    result:  status=error
#                970 - non-list grid; othe parms nominal
#                    result:  status=error
#                975 - missing grid value; other parms nominal
#                    result:  status=error:
#                980 - missing grid parm; other parms nominal
#                    result:  status=error:

#            BVA for integrity
#                095 - valid integrity; other parms nominal
#                    result:  valid grid, valid integrity, status=ok
#                982 - invalid integrity; other parms nominal
#                    result:  status=error:
#                984 - bad length integrity; other parms nominal
#                    result:  status=error:
#                986 - missing integrity value; other parms nominal
#                    result:  status=error:
#                988 - missing integrity parm; other parms nominal
#                    result:  status=error:
#
# Side-Effect Analysis
#    no side effects
#
# Acceptable level of risk:   BVA

# ------------------------------------------

# Input grid integrity string: '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        
    def test_Insert_010_ShouldReturnThreeValues(self):
        parms = {'op': 'insert',
                'cell': 'r1c1',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        self.assertIn('grid', actualResult)
        self.assertEqual(type(actualResult['grid']), type([]))
        self.assertIn('integrity', actualResult)
        self.assertIn('status', actualResult)
        self.assertEqual(len(actualResult), 3)
        
    def test_Insert_015_LowRowLowCol(self):
        parms = {'op': 'insert',
                'cell': 'r1c1',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [3,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '31f66be2552d8f77f2d68cb81722d7b7980e5483b9c66ce468144a8839c7ec12'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_020_LowRowHighCol(self):
        parms = {'op': 'insert',
                'cell': 'r1c9',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,3,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '80af736f5ceeeb8cfd2fef2c84eb5fc93393d97377a0c82c91f13c12932b33a9'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_025_HighRowLowCol(self):
        parms = {'op': 'insert',
                'cell': 'r15c7',
                'value': '8',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,8,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '3b3fafca00204c4a65edb0179ed87dff352ba135b8a19d5d6b1d25e10ea15e36'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_030_HighRowHighCol(self):
        parms = {'op': 'insert',
               'cell': 'r14c15',
                'value': '7',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,7,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '65e961e84820a6bef5b6ee6fade2584968925b458092e37dcf54f984aeb6937d'
        self.assertTrue(actualResult['integrity'] in hashString)

    def test_Insert_035_OverlappingGridRowCol(self):
        parms = {'op': 'insert',
                 'cell': 'r8c8',
                'value': '7',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,7,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '84feccb062beb03743bca800bdf3d31753ee6b3b583009f748ab23c97e2bf978'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_040_RxCy(self):
        parms = {'op': 'insert',
                'cell': 'R8C8',
                'value': '7',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,7,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}        
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '84feccb062beb03743bca800bdf3d31753ee6b3b583009f748ab23c97e2bf978'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_045_rxcy(self):
        parms = {'op': 'insert',
                'cell': 'r8c8',
                'value': '7',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,7,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '84feccb062beb03743bca800bdf3d31753ee6b3b583009f748ab23c97e2bf978'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_910_TooLowRow(self):
        parms = {'op': 'insert',
                'cell': 'r0c8',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_912_TooHighRow(self):
        parms = {'op': 'insert',
                'cell': 'r16c8',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_914_NonIntegerRow(self):
        parms = {'op': 'insert',
                'cell': 'r1.5c8',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_918_TooLowCol(self):
        parms = {'op': 'insert',
                'cell': 'r12c2',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_920_TooHighCol(self):
        parms = {'op': 'insert',
                'cell': 'r2c12',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_926_CellParmItems(self):
        parms = {'op': 'insert',
                'cell': 'r1c8llama',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_932_ImmutableCell(self):
        parms = {'op': 'insert',
                'cell': 'r1c2',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_934_MissingCellValue(self):
        parms = {'op': 'insert',
                'cell': '',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_936_MissingCellParm(self):
        parms = {'op': 'insert',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid cell'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_060_NominalBreakRules(self):
        parms = {'op': 'insert',
                'cell': 'r8c8',
                'value': '3',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,3,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'warning'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = 'ac860089b9970e67e94262d377f657dd48198c14a09c0a75fa8505227ffbee7a'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_065_LowFollowRules(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '1',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,1,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '24c7664dee6381310b72a961df833dc18e8a7bfa492e943bff27d07288cdadde'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_070_HighFollowRules(self):
        parms = {'op': 'insert',
                'cell': 'r1c1',
                'value': '9',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [9,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,
            0,0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '72ac50e6cf01d8edc2f9c783e6840a35eaa26899b150eaf32cc6a22b86566b8c'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_080_MissingValueValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)   
             
    def test_Insert_085_MissingValueParm(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_940_NonIntValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '1.5',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid value'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_942_TooLowValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '0',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid value'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_944_TooHighValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '10',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid value'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_090_NominalGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
            'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '5a3f0c31993d46bcb2ab5f3e8318e734231ee8bdb26cba545fadd7b1732888cd'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_950_ShortGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_955_LongGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1, 0]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_960_NonIntGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,A]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_965_OutofBoundsGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-10]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_970_NonListGrid(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': '0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_975_MissingGridValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423',
                'grid': ''}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_980_MissingGridParm(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73423'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid grid'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_095_ValidIntegrity(self):
        parms = {'op': 'insert',
                'cell': 'r8c8',
                'value': '7',
                'integrity': '18e73423',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'grid': [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,0,0,0,
            -3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,0,-2,0,
            0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,7,0,-2,0,0,-1,0,-9,0,-4,0,-5,-7,0,
            0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,0,0,0,0,
            0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1],
           'integrity': 'ff3f7ea9','status':'ok'}
        self.assertEqual(expectedResult['grid'], actualResult['grid'])
        self.assertEqual(expectedResult['status'], actualResult['status'])
        hashString = '84feccb062beb03743bca800bdf3d31753ee6b3b583009f748ab23c97e2bf978'
        self.assertTrue(actualResult['integrity'] in hashString)
        
    def test_Insert_982_InvalidIntegrity(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e73424',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid integrity'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_984_BadLengthIntegrity(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '18e7342',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid integrity'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_986_MissingIntegrityValue(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'integrity': '',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid integrity'}
        self.assertEqual(expectedResult['status'], actualResult['status'])
        
    def test_Insert_988_MissingIntegrityParm(self):
        parms = {'op': 'insert',
                'cell': 'r9c1',
                'value': '',
                'grid': '[0,-2,0,0,-1,0,0,-4,0,\
                         -8,0,-1,-9,0,0,0,0,-5,\
                         0,0,0,0,-3,0,0,-1,0,\
                         0,-3,0,0,0,0,-4,0,-6,\
                         -5,0,-9,0,0,0,0,0,-7,\
                         0,0,0,0,0,0,-2,-8,0,\
                         -2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,\
                         0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,\
                         0,-4,0,-5,-7,0,0,0,0,0,0,-7,0,0,-5,\
                         0,0,-6,0,0,0,0,-9,0,\
                         -2,0,0,0,0,0,-4,0,-8,\
                         -7,0,-9,0,0,0,0,0,0,\
                         0,-5,0,0,-9,0,0,0,0,\
                         -4,0,0,-6,0,-3,-9,0,0,\
                         0,-6,0,0,-5,0,0,-3,-1]'}
        actualResult = insert._insert(parms)
        expectedResult = {'status': 'error: invalid integrity'}
        self.assertEqual(expectedResult['status'], actualResult['status'])