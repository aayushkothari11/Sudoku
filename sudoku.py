import random
import copy
import time
import sys
sys.setrecursionlimit(10000)

total_numbers = 9
size_of_board = 81
block_size = 3

''' 5 difficulty levels '''

levels = {
    'extremely-easy': [40, 50, 5, "RandomizingGlobally"],
    'easy': [36, 39, 4,"RandomizingGlobally"],
    'medium': [32, 35, 3, "Jumping one Cell"],
    'hard': [28, 31, 2, "Wandering along S"],
    'evil': [22, 27, 0, "Left to Right then Top to Bottom"]
}


''' function that gives all the possible values at a given index  '''

def available(board, index):
    all_val = [True for i in range(9)]
    for i in range(total_numbers):
        pos_row = board[i + index // total_numbers * total_numbers]
        if pos_row != 0:
            all_val[pos_row - 1] = False

    for i in range(total_numbers):
        pos_col = board[i * total_numbers + index % total_numbers]
        if pos_col != 0:
            all_val[pos_col - 1] = False

    for i in range(total_numbers):
        pos_block = board[i % block_size + (i // block_size) * total_numbers + (index % total_numbers) // block_size * block_size + index // (total_numbers * block_size) * (total_numbers * block_size)]
        if pos_block != 0:
            all_val[pos_block - 1] = False

    possible_values = []
    for i in range(1,total_numbers+1):
        if (all_val[i - 1]):
            possible_values.append(i)

    return possible_values


''' place 11 numbers on the board to randomly initialize the board as per the paper '''

def initialize():
    index = 0
    field[index] = random.randint(1,total_numbers)
    for _ in range(0,10):
        index = random.randint(1,size_of_board-1)
        numbers = available(copy.copy(field),index)
        while not len(numbers)>0 and field[index] == 0:
            index = random.randint(1,size_of_board-1)
            numbers = available(copy.copy(field),index)
        field[index] = numbers[random.randint(0,len(numbers)-1)]


''' Generate temporary boards with adding the values at the given position '''

def add_values(temp_board,index):
    possible_values = available(temp_board, index)
    temp_fields = []
    for i in range(len(possible_values)):
        temp = copy.copy(temp_board)
        temp[index] = possible_values[i]
        temp_fields.append(temp)
    # random.shuffle(temp_fields)
    return temp_fields


''' Check if all indexes are filled or not '''

def fill_checker(board):
    for i in range(size_of_board):
        if board[i]==0:
            return False
    return True


''' Return the first empty position on the board '''

def empty_pos(board):
    for i in range(size_of_board):
        if board[i]==0:
            return i

'''
templates = []
if temp_board:
    templates.append(copy.copy(temp_board))

if templates and time.time() - start > 5:
    return templates[random.randint(0,len(templates)-1)]
'''


''' Depth first search to fill the board '''

def DFS(board, start, max_sol):
    global solCount

    if fill_checker(board):
        # solCount+=1
        # print("hi")
        # print(solCount)
        return board
    
    available_pos = empty_pos(board)
    temp_boards = add_values(board,available_pos)
    for i in range(len(temp_boards)):
        board = copy.copy(temp_boards[i])
        temp_board = DFS(board,start,max_sol)
        # if solCount > max_sol:
        #     return Noneif solCount > max_sol:
        #     return None

        if temp_board and time.time() - start > 1:
            return temp_board


''' Count the number of filled indexes on the board '''

def count_filled(board):
    count = 0
    for i in range(size_of_board):
        if board[i]!=0:
            count+=1
    return count


''' DFS to find a solution '''

def solution(board,possible_dig):
    if fill_checker(board):
        return True

    boolean = False
    available_pos = empty_pos(board)
    temp_boards = add_values(board,available_pos)
    for i in range(len(temp_boards)):
        board = copy.copy(temp_boards[i])
        if solution(board.copy(),possible_dig):
            boolean = True
            break
    
    return boolean


''' Check if the solution is unique or not '''

def unique(board, original_val, index,possible_dig):
    temp_boards = add_values(board,index)
    for i in range(len(temp_boards)):
        board = copy.copy(temp_boards[i])
        if board[index] != original_val:
            # print(board)
            if solution(board,possible_dig):
                return False
    return True


''' 4 algos mentioned in paper for digging '''

def Left2RightAndTop2Bottom(index):
    return (index+1) % size_of_board


def WanderingAlongS(index):
    if index<0:
        return 0
    if (index//total_numbers)%2==0:
        if (index+1)%total_numbers==0:
            index = index + total_numbers
        else:
            index = index + 1
    else:
        if index % total_numbers == 0:
                index = index + total_numbers
        else:
            index = index - 1
    return index % size_of_board


def RandomizingGlobally(board1):
    index = random.randint(0, 80)
    return index


def JumpingOneCell(index):
    if index<0:
        return 0
    if (index//total_numbers)%2==0:
        if (index+1)%total_numbers==0:
            index = index + total_numbers - 1
        elif (index+2)%total_numbers==0:
            index = index + total_numbers + 1
        else:
            index = index + 2
    else:
        if index % total_numbers == 1:
            index = index + total_numbers - 1
        elif index % total_numbers == 0:
            index = index + total_numbers + 1
        else:
            index = index - 2
    if index % size_of_board != index:
            index = (index + 1) % 2
    return index


''' Count min number of elements in a row and column '''

def count_RC(board):
    min_RC = 9
    for i in range(total_numbers):
        row_count, col_count = 0,0
        for j in range(total_numbers):
            if board[i * total_numbers + j] != 0:
                row_count+=1
            if board[j * total_numbers + i] != 0:
                col_count+=1

        min_RC = min(min(row_count, col_count), min_RC)
        
    return min_RC
    

''' Dig out numbers from the board until we get a minimal board which can be solved '''   

def digging(board, difficulty):
    start = time.time()
    level = levels[difficulty]
    # print(level)
    min_filled, maxfilled = level[0], level[1]
    min_RC = level[2]
    count = 0
    filled = random.randint(min_filled,maxfilled)
    possible_dig = [True for _ in range(size_of_board)]
    count_available = size_of_board
    position = -1
    while count_filled(board) >= filled:
        if time.time()-start>3:
            return None
        count+=1
        if difficulty =="extremely-easy":
            position = RandomizingGlobally(board.copy())
        elif difficulty =="easy":
            position = RandomizingGlobally(board.copy())
        elif difficulty =="medium":
            position = JumpingOneCell(position)
        elif difficulty =="hard":
            position = WanderingAlongS(position)
        elif difficulty =="evil":
            if count%3==0:
                position = random.randint(0,80)
            position = Left2RightAndTop2Bottom(position)
        
        temp = board.copy()
        actual_pos = board[position]
        temp[position] = 0
        # print(position)
        # print(board)
        if possible_dig[position] and unique(temp.copy(), actual_pos, position,possible_dig) and count_RC(temp) >= min_RC:
                board = temp.copy()

        possible_dig[position] = False
        count_available-=1

    # print(time.time()-start)
    return board


''' Print the board '''

def print_board(to_print):
    board = ""
    for i in range(size_of_board):
        if i != 0:
            if i % (total_numbers * block_size) == 0:
                board += "\n-------|-------|-------\n"
            elif i % total_numbers == 0:
                board += "\n"
            elif i % block_size == 0:
                board += " |"

        board += " "

        if to_print[i] != 0:
            board += str(to_print[i])
        else:
            board += " "

    return board



start = time.time()
board = None
while board==None:
    field = [0 for i in range(size_of_board)]
    initialize()
    board = DFS(field.copy(),start,100)
    ans = digging(board.copy(), "extremely-easy")
    if ans == None:
        board = None
        continue
    print(print_board(ans))
    # print(count_filled(ans))

