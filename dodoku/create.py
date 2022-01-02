'''
    Created on Sept 28, 2021
    
    @author:    Roy Harmon
'''
import hashlib
import random

def _create(parms):
    if(not('level' in parms)):
        level = '1'
    else:
        level = __levelCheck(parms['level'])
    if level == 'error':
        return {'status': 'error: invalid level'}
        
    rowGrid = __returnGrid(level)
    
    integrityString = __getIntegrityString(rowGrid)

    result = {'grid': rowGrid, 'integrity': integrityString, 'status': 'ok'}
    return result

def __levelCheck(level):
    if level == '':
        return '1'
    if not level.isdecimal():
        return 'error'
    if int(level) < 1:
        return 'error'
    if int(level) > 3:
        return 'error'
    return level

def __returnGrid(level):
    if level == '1':
        return [0,-2,0,0,-1,0,0,-4,0,-8,0,-1,-9,0,0,0,0,-5,0,\
            0,0,0,-3,0,0,-1,0,0,-3,0,0,0,0,-4,0,-6,-5,0,-9,0,0,0,0,0,-7,0,0,0,0,0,0,-2,-8,\
            0,-2,0,0,-6,0,0,0,0,0,0,-1,-4,0,-6,0,0,0,-6,0,0,-3,0,0,0,-2,0,0,-1,0,-9,0,-4,0,\
            -5,-7,0,0,0,0,0,0,-7,0,0,-5,0,0,-6,0,0,0,0,-9,0,-2,0,0,0,0,0,-4,0,-8,-7,0,-9,0,\
            0,0,0,0,0,0,-5,0,0,-9,0,0,0,0,-4,0,0,-6,0,-3,-9,0,0,0,-6,0,0,-5,0,0,-3,-1]
    if level == '2':
        return [0,-6,0,0,0,0,0,-5,-9,-9,-3,0,-4,-8,0,0,0,0,0,0,0,0,0,\
            -7,-3,0,0,0,-5,0,0,-1,0,0,-4,-6,0,0,0,0,0,-6,0,-9,0,0,-8,-1,-2,0,0,0,0,0,0,0,0,\
            0,-7,0,0,0,0,0,0,0,0,-5,0,-8,0,-4,0,0,-1,0,0,0,-7,0,0,-6,0,-2,0,-9,0,0,0,0,0,0,\
            0,0,-5,0,0,0,0,0,0,0,0,0,-9,-5,-3,0,0,-7,0,-4,0,0,0,0,0,-5,-8,0,0,-1,0,0,-9,0,0,\
            0,-2,-1,0,0,0,0,0,0,0,0,0,-9,-8,0,-6,-1,-6,-1,0,0,0,0,0,-7,0]
    if level == '3':
        return [0,0,0,0,-6,0,0,0,0,0,0,0,-4,0,-9,0,0,0,0,0,-9,-7,0,-5,-1,0,0,0,-5,-2,0,\
            -7,0,-8,-9,0,-9,0,0,-5,0,-2,0,0,-4,0,-8,-3,0,-4,0,-7,-2,0,0,0,-1,-2,0,-8,0,0,0,\
            0,-3,0,0,0,0,0,0,0,-6,0,-4,0,0,0,-8,0,-7,0,0,0,0,0,0,0,-5,0,0,0,0,-1,0,-6,-3,0,\
            0,0,-9,-8,0,-5,0,-1,-2,0,-2,0,0,-7,0,-1,0,0,-3,0,-4,-3,0,-8,0,-6,-5,0,0,0,-7,-3,\
            0,-5,-9,0,0,0,0,0,-4,0,-2,0,0,0,0,0,0,0,-6,0,0,0,0]

def __getIntegrityString(rowGrid):
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
    for ind in transposeGrid:
        columnGridString = columnGridString + str(rowGrid[ind])
    
    integrityHash = hashlib.sha256()
    integrityHash.update(columnGridString.encode())
    integrityHashDigest = integrityHash.hexdigest()
    integrityHashDigest = integrityHashDigest.lower()
    integrityStart = random.randrange(len(integrityHashDigest) - 8)
    integrityString = integrityHashDigest[integrityStart:integrityStart + 8]
    return integrityString

