''' Python script to check whther the board generated is valid or not '''

import numpy as np

def notInRow(arr, row):
    st = set()  
  
    for i in range(0, 9):
        if arr[row][i] in st:  
            return False

        st.add(arr[row][i])  
      
    return True


def notInCol(arr, col):  
    st = set()  
  
    for i in range(0, 9):
        if arr[i][col] in st: 
            return False
  
        st.add(arr[i][col])  
      
    return True


def notInBox(arr, startRow, startCol):  
  
    st = set()  
  
    for row in range(0, 3):  
        for col in range(0, 3):  
            curr = arr[row + startRow][col + startCol]  

            if curr in st:  
                return False
  
            st.add(curr)  
          
    return True
  
def isValid(arr, row, col):  
  
    return (notInRow(arr, row) and notInCol(arr, col) and
            notInBox(arr, row - row % 3, col - col % 3))  
  
def isValidConfig(arr, n):  
  
    for i in range(0, n):  
        for j in range(0, n):

            if not isValid(arr, i, j):  
                return False
          
    return True

arr = [8, 4, 5, 3, 9, 2, 1, 6, 7, 1, 3, 7, 8, 4, 6, 5, 9, 2, 9, 6, 2, 1, 5, 7, 3, 4, 8, 5, 7, 9, 4, 8, 3, 6, 2, 1, 4, 8, 1, 6, 2, 5, 7, 3, 9, 6, 2, 3, 9, 7, 1, 8, 5, 4, 2, 1, 8, 5, 3, 9, 4, 7, 6, 3, 9, 6, 7, 1, 4, 2, 8, 5, 7, 5, 4, 2, 6, 8, 9, 1, 3]
arr = np.array(arr).reshape((9,9))
print(isValidConfig(arr,9))