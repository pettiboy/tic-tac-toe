"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # if board is empty then it is X's turn
    if board == initial_state():
        return X

    x_count = o_count = 0

    # loop over the board to count nuber of Xs and Os
    for sublist in board:
        for variable in sublist:
            if variable == X:
                x_count += 1
            elif variable == O:
                o_count += 1

    # if number of X's on the board are equal to number of O's then it is X's turn
    if x_count == o_count:
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()

    # enumerate is used to obtain index
    # for list in board
    for i, row in enumerate(board):
        # loop over values in that list
        for j, element in enumerate(row):
            # if element is empty means that move can be made
            if element == None:
                # add that action to the set
                all_actions.add((i,j))
    
    return all_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # the original board should be left unmodified: 
    # because Minimax will ultimately require considering many different board states during its computation
    board_copy = copy.deepcopy(board)

    # for list in board
    for i, row in enumerate(board_copy):
        # loop over values in that list
        for j, element in enumerate(row):
            # if the value being looped over is the action
            if (i, j) == action:
                # if element is none then the action passed is invalid
                if element != None:
                    raise Exception("Invalid action")
                # call the player function to check whose turn it is
                # and edit the board_copy's action element to that players turn
                board_copy[i][j] = player(board)

    # return the new board
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    possible_winning_combinations = []
    
    # add all 3 rows to possible_winning_combinations
    for row in board:
        possible_winning_combinations.append(row)

    # declare 5 lists, 3 for columns and 2 for diagnals
    list1, list2, list3, list4, list5 = ([] for i in range(5))

    # add all 3 colums to list1, list2 and list3
    for i, row in enumerate(board):
        for j, element in enumerate(row):            
            if j == 0:
                list1.append(element)
            if j == 1:
                list2.append(element)
            if j == 2:
                list3.append(element)

    # add diagnals to list4 and list5
    for i, row in enumerate(board):
        for j, element in enumerate(row):            
            if i == j:
                list4.append(element)
            if (i, j) in ((0, 2), (1, 1), (2, 0)):
                list5.append(element) 
    
    # add list of columns and diagnals to possible_winning_combinations
    possible_winning_combinations += [list1, list2, list3, list4, list5]

    # check if all items are same in any list contained in possible_winning_combinations
    for i, row in enumerate(possible_winning_combinations):
        # if all members of the row are equal then we have a winner
        if all_equal(row):
            # the winner will be first element of that row
            try:
                # all indexes of that row will contain the winner (X or O)
                return row[0]
            except:
                return None

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if someone won the game then it is a terminal state
    if winner(board) is not None:
        return True

    # check if the board is full
    board_list = [item for sublist in board for item in sublist] # gets values of, list of lists

    # if any no values are None in board then it is  aterminal state
    # any will return True if x is None
    # we want x not to be None...
    if not any(x is None for x in board_list):
        return True
    
    # else return false
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_status = winner(board)
    
    if winner_status == X:
        return 1
    elif winner_status == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # consider X as max player
    # The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    if player(board) == X:
        values = []
        for action in actions(board):
            values.append(tuple([min_value(result(board, action)), action]))
        return max(values)[1]

    # consider O as min player
    # The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).
    if player(board) == O:
        values = []
        for action in actions(board):
            values.append(tuple([max_value(result(board, action)), action]))
        return min(values)[1]
 

def max_value(board):
    """
    Takes a `board` and returns as output the `value` of that board
    if I am trying to maximize the `value` of that `board`
    """
    # I want v to be as high as possible at the end 
    # so initially I will set it as low as I can
    v = - math.inf

    # if the game is over then 
    if terminal(board):
        # the utility function will calculate the value of the board
        return utility(board)

    # loop over all possible actions on the board
    for action in actions(board):
        # v should be the maximum of v AND the best that the min player can do
        v = max(  v, min_value( result(board, action) )  )

    return v

def min_value(board):
    """
    Takes a `board` and returns as output the `value` of that board
    if I am trying to minimize the `value` of that `board`
    """
    # I want v to be as low as possible at the end 
    # so initially I will set it as high as I can
    v = math.inf
    
    # if the game is over then 
    if terminal(board):
        # the utility function will calculate the value of the board
        return utility(board)

    # loop over all possible actions on the board
    for action in actions(board):
        # v should be the minimum of v AND the best that the max player can do
        v = min(  v, max_value( result(board, action) )  )

    return v


def all_equal(iterator):
    """
    Returns True if in given `iterator` (list, tuple etc.) all `values` 
    are `equal` else reutns False
    """
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)