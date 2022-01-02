'''
    Created on Oct 21, 2021
    
    @author:    Roy Harmon
'''
import re
import hashlib
import random
def _insert(parms):
    result = {}
    validation = __validateParms(parms)
    if 'status' in validation and validation['status'].startswith('error:'):
        result['status'] = validation['status']
        return result
    if parms['value'] == '':
        val = 0
    else:
        val = int(parms['value'])
    cell = parms['cell']
    result['grid'] = __updateGrid(val,cell,parms['grid'])
    result['integrity'] = __getIntegrity(result['grid'])
    violatesRules = __checkWarning(val, cell, result['grid'])
    if violatesRules == 1:
        result['status'] = 'warning'
    else:
        result['status'] = 'ok'
    return result

def __validateParms(parms):
    if (not('value' in parms)):
        parms['value'] = ''
    if (not('cell' in parms)):
        return {'status':'error: invalid cell'}
    if (not('grid' in parms)):
        return {'status':'error: invalid grid'}
    if (not('integrity' in parms)):
        return {'status':'error: invalid integrity'}
    if __validateValue(parms['value']) == 0:
        return {'status':'error: invalid value'}
    if __validateGrid(parms['grid']) == 0:
        return {'status':'error: invalid grid'}
    if __validateCell(parms['cell'], parms['grid']) == 0:
        return {'status':'error: invalid cell'}
    if __checkIntegrity(parms['grid'], parms['integrity']) == 0:
        return {'status':'error: invalid integrity'}
    return parms

def __checkIntegrity(grid, integrityString):
    if len(integrityString) != 8:
        return 0
    if integrityString in __getIntegrityHash(grid):
        return 1
    else: 
        return 0

def __getIntegrityString(integrityHashDigest):
    integrityStart = random.randrange(len(integrityHashDigest) - 8)
    integrityString = integrityHashDigest[integrityStart:integrityStart + 8]
    return integrityString

def __getIntegrityHash(grid):
    transposeGrid = (0, 9, 18, 27, 36, 45, 54, 69, 84, 1, 10, 19, 28, 37, 46, 55, \
         70, 85, 2, 11, 20, 29, 38, 47, 56, 71, 86, 3, 12, 21, 30, 39, 48, 57, 72, 87, 4, \
         13, 22, 31, 40, 49, 58, 73, 88, 5, 14, 23, 32, 41, 50, 59, 74, 89, 6, 15, 24, 33, \
         42, 51, 60, 75, 90, 99, 108, 117, 126, 135, 144, 7, 16, 25, 34, 43, 52, 61, 76, \
         91, 100, 109, 118, 127, 136, 145, 8, 17, 26, 35, 44, 53, 62, 77, 92, 101, 110, \
         119, 128, 137, 146, 63, 78, 93, 102, 111, 120, 129, 138, 147, 64, 79, 94, 103, \
         112, 121, 130, 139, 148, 65, 80, 95, 104, 113, 122, 131, 140, 149, 66, 81, 96, \
         105, 114, 123, 132, 141, 150, 67, 82, 97, 106, 115, 124, 133, 142, 151, 68, 83, \
         98, 107, 116, 125, 134, 143, 152)
    columnGridString = ''
    if type(grid) == type('str'):
        grid = re.findall("(\-?\d)", grid)
    for indx in transposeGrid:
        columnGridString = columnGridString + str(grid[indx])
    integrityHash = hashlib.sha256()
    integrityHash.update(columnGridString.encode())
    integrityHashDigest = integrityHash.hexdigest()
    integrityHashDigest = integrityHashDigest.lower()
    return integrityHashDigest

def __getIntegrity(grid):
    integrityHash = __getIntegrityHash(grid)
    integrityString = __getIntegrityString(integrityHash)
    return integrityString

def __validateCell(cellAddress, grid):
    regMatches = re.search("^[Rr](\d{1,2})[Cc](\d{1,2})$", cellAddress)
    if regMatches == None:
        return 0
    row = int(regMatches.group(1))
    col = int(regMatches.group(2))
    if row < 1 or row > 15:
        return 0
    if col < 1 or col > 15:
        return 0
    cellIndex = __getCellIndex(cellAddress)
    if cellIndex == -1:
        return 0
    matches = re.findall("(\-?\d)", grid)
    cellValue = matches[cellIndex]
    if int(cellValue) < 0:
        return 0
    return 1

def __validateValue(value):
    if value == '':
        return 1
    if not value.isdecimal():
        return 0
    if int(value) < 1 or int(value) > 9:
        return 0
    return 1

def __validateGrid(grid):
    grid = grid.replace(" ", "")
    fullGrid = re.search("^\[([\-\d,]+)\]$", grid)
    if fullGrid == None:
        return 0
    grid = re.findall("(\-?\d)", grid)
    if len(grid) != 153:
        return 0
    for cellValue in grid:
        if int(cellValue) < -9 or int(cellValue) > 9:
            return 0
    return 1

def __checkWarning(cellValue, cell, grid):
    if cellValue == 0:
        return 0
    cellIndex = __getCellIndex(cell)
    if __findInArray(cellValue, __warnRows(cellIndex), grid) == 1:
        return 1
    if __findInArray(cellValue, __warnCols(cellIndex), grid) == 1:
        return 1
    if __findInArray(cellValue, __warnSubs(cellIndex), grid) == 1:
        return 1
    return 0

def __getCellIndex(cell):
    regMatches = re.search("[Rr](\d{1,2})[Cc](\d{1,2})", cell)
    row = int(regMatches.group(1))-1
    col = int(regMatches.group(2))-1
    indexGrid = ((0,1,2,3,4,5,6,7,8,-1,-1,-1,-1,-1,-1),
                (9,10,11,12,13,14,15,16,17,-1,-1,-1,-1,-1,-1),
                (18,19,20,21,22,23,24,25,26,-1,-1,-1,-1,-1,-1),
                (27,28,29,30,31,32,33,34,35,-1,-1,-1,-1,-1,-1),
                (36,37,38,39,40,41,42,43,44,-1,-1,-1,-1,-1,-1),
                (45,46,47,48,49,50,51,52,53,-1,-1,-1,-1,-1,-1),
                (54,55,56,57,58,59,60,61,62,63,64,65,66,67,68),
                (69,70,71,72,73,74,75,76,77,78,79,80,81,82,83),
                (84,85,86,87,88,89,90,91,92,93,94,95,96,97,98),
                (-1,-1,-1,-1,-1,-1,99,100,101,102,103,104,105,106,107),
                (-1,-1,-1,-1,-1,-1,108,109,110,111,112,113,114,115,116),
                (-1,-1,-1,-1,-1,-1,117,118,119,120,121,122,123,124,125),
                (-1,-1,-1,-1,-1,-1,126,127,128,129,130,131,132,133,134),
                (-1,-1,-1,-1,-1,-1,135,136,137,138,139,140,141,142,143),
                (-1,-1,-1,-1,-1,-1,144,145,146,147,148,149,150,151,152))
    return indexGrid[row][col]

def __warnRows(cellIndex):
    rows = ((0,1,2,3,4,5,6,7,8),
            (9,10,11,12,13,14,15,16,17),
            (18,19,20,21,22,23,24,25,26),
            (27,28,29,30,31,32,33,34,35),
            (36,37,38,39,40,41,42,43,44),
            (45,46,47,48,49,50,51,52,53),
            (54,55,56,57,58,59,60,61,62),
            (60,61,62,63,64,65,66,67,68),
            (69,70,71,72,73,74,75,76,77),
            (75,76,77,78,79,80,81,82,83),
            (84,85,86,87,88,89,90,91,92),
            (90,91,92,93,94,95,96,97,98),
            (99,100,101,102,103,104,105,106,107),
            (108,109,110,111,112,113,114,115,116),
            (117,118,119,120,121,122,123,124,125),
            (126,127,128,129,130,131,132,133,134),
            (135,136,137,138,139,140,141,142,143),
            (144,145,146,147,148,149,150,151,152))
    return getCellGroup(cellIndex, rows)

def getCellGroup(cellIndex, groups):
    groupList = []
    for groupCells in groups:
        if cellIndex in groupCells:
            groupList.append(groupCells)
    return groupList

def __warnCols(cellIndex):
    cols = ((0,9,18,27,36,45,54,69,84),
            (1,10,19,28,37,46,55,70,85),
            (2,11,20,29,38,47,56,71,86),
            (3,12,21,30,39,48,57,72,87),
            (4,13,22,31,40,49,58,73,88),
            (5,14,23,32,41,50,59,74,89),
            (6,15,24,33,42,51,60,75,90),
            (7,16,25,34,43,52,61,76,91),
            (8,17,26,35,44,53,62,77,92),
            (60,75,90,99,108,117,126,135,144),
            (61,76,91,100,109,118,127,136,145),
            (62,77,92,101,110,119,128,137,146),
            (63,78,93,102,111,120,129,138,147),
            (64,79,94,103,112,121,130,139,148),
            (65,80,95,104,113,122,131,140,149),
            (66,81,96,105,114,123,132,141,150),
            (67,82,97,106,115,124,133,142,151),
            (68,83,98,107,116,125,134,143,152))
    return getCellGroup(cellIndex, cols)

def __warnSubs(cellIndex):
    subs = ((0,1,2,9,10,11,18,19,20),
            (3,4,5,12,13,14,21,22,23),
            (6,7,8,15,16,17,24,25,26),
            (27,28,29,36,37,38,45,46,47),
            (30,31,32,39,40,41,48,49,50),
            (33,34,35,42,43,44,51,52,53),
            (54,55,56,69,70,71,84,85,86),
            (57,58,59,72,73,74,87,88,89),
            (60,61,62,75,76,77,90,91,92),
            (63,64,65,78,79,80,93,94,95),
            (66,67,68,81,82,83,96,97,98),
            (99,100,101,108,109,110,117,118,119),
            (102,103,104,111,112,113,120,121,122),
            (105,106,107,114,115,116,123,124,125),
            (126,127,128,135,136,137,144,145,146),
            (129,130,131,138,139,140,147,148,149),
            (132,133,134,141,142,143,150,151,152))
    return getCellGroup(cellIndex, subs)

def __findInArray(checkValue, checkArray, grid):
    valueCount = 0
    if len(checkArray) == 9:
        for index in checkArray:
            if abs(checkValue) == abs(grid[index]):
                valueCount += 1
        if valueCount > 1:
            return 1
    else:
        for arrayList in checkArray:
            valueCount = 0
            for index in arrayList:
                if abs(checkValue) == abs(grid[index]):
                    valueCount += 1
            if valueCount > 1:
                return 1
    return 0

def __updateGrid(cellValue, cellAddress, grid):
    cellIndex = __getCellIndex(cellAddress)
    if type(grid) == type('str'):
        grid = re.findall("(\-?\d)", grid)
    if type(grid) == type([]):
        for index in range(len(grid)):
            grid[index] = int(grid[index])
    grid[cellIndex] = cellValue
    return grid