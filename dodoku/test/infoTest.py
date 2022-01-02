'''
    Created on Sept 28, 2021
    
    @author:    Roy Harmon
'''
import unittest
import dodoku.info as info

class InfoTest(unittest.TestCase):

    def test_Info_010_ShouldReturnMyUserName(self):
        expectedResult = {'user': 'rrh0008'}
        parms = {'op': 'info'}
        actualResult = info._info(parms)
        self.assertDictEqual(expectedResult, actualResult)
        