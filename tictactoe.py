# Tic Tac Toe Player
from argparse import Action
import math
import copy
from operator import index

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

import copy
X = "X"
O = "O"
EMPTY = None

def prop_count(board, item):
    full_count = 0
    #print("'Board' length: {}".format(len(board)))
    for i in range(len(board)):
        #print("prop_count board: {}".format(board))
        sub_board = board[i]
        #print(f"sub_board: {sub_board}")
        sub_count = sub_board.count(item)
        full_count += sub_count
    return full_count


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #print("player()")
    if prop_count(board, X) > prop_count(board, O):
        #print("player == O")
        return O
    else:
        #print("player == X")
        return X
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j), row & column, available on the board.
    valid_act: list containing all valid actions
    """
    #print("actions()")
    board_clone = copy.deepcopy(board)
    valid_act = []
    for index in range(3):
        row = board_clone[index]
        empty_in_row = row.count(EMPTY)
        # print(empty_in_row)
        if empty_in_row > 0:
            for a in range(empty_in_row):
                column = row.index(EMPTY)
                row.remove(EMPTY)
                row.insert(0, "FAKE")
                # print(column)
                valid_act.append((index, column))
                # print(index, column)
                empty_in_row -= 1
    # what to do if board is full?
    # print("og_board: {}".format(board))
    # print("clone_board: {}".format(board_clone))
    return valid_act
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    print("result()")
    print("Action: {}".format(action))
    board_clone = copy.deepcopy(board)
    row = action[0]
    column = action[1]
    print("action_loc: {}".format(board_clone[row][column]))
    if board_clone[row][column] == EMPTY:
        row = board_clone[row]
        x_or_o = player(board)
        row.remove(row[column])
        row.insert(column, x_or_o)
        return board_clone
    else:
        return None
    #else:
        #raise ValueError # because of the invalid action - need to give a description


def eval_board(board):
    #print("eval_board()")
    horizontal = []    
    vertical = []
    diagonal = []
    for i in range(3):
        horizontal = [board[i][0], board[i][1], board[i][2]]
        vertical = [board[0][i], board[1][i], board[2][i]]
        if i== 0:
            diagonal = [board[0][0], board[1][1], board[2][2]]
        elif i == 2:
            diagonal = [board[0][2], board[1][1], board[2][0]]
        if horizontal.count(X) == 3 or vertical.count(
            X) == 3 or diagonal.count(X) == 3:
            return X
        elif horizontal.count(O) == 3 or vertical.count(
            O) == 3 or diagonal.count(O) == 3:
            return O
    return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #print("winner()")
    if prop_count(board, X) >= 3:
        winner = eval_board(board)
        #print(f"winner: {winner}")
    elif prop_count(board, O) >= 3:
        winner = eval_board(board)
        #print(f"winner: {winner}")
    else:
        #print("no winner")
        return None
    return winner
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #print("terminal()")
    if prop_count(board, EMPTY) == 0 or winner(board) != None:
        #print("utility == False")
        utility(board)
        #print("utility == True")
        return True
    else:
        return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #print("utility()")
    #print(f"{board[0]}")
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    #raise NotImplementedError
    

def insert_tuple(collection, list):
    '''Inserts tuples into new list'''
    index = -1
    while abs(index) <= len(collection):
        list.insert(0, collection[index])
        index -= 1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    print("minimax()")
    new_board = copy.deepcopy(board)
    turn = player(board)
    # print("player: {}".format(turn))
    board_list = board # list of all boards that were explored
    init_frontier = actions(board)
    global init_frontier_act
    init_frontier_act = 0
    frontier = copy.deepcopy(init_frontier)
    
    def min_value_act(board):
        '''Gets the minimum - lowest value action'''
        print("------------------")
        print("min_value_act")
        print(f"first actions to be taken {init_frontier}")
        #print("all_actions: {}".format(all_actions))
        v = 10
        optimal = ()
        print(f"initial_board: {board}")
        if terminal(board):
            print("board = terminal")
            return None
        while len(frontier) > 0:
            print("--------")
            action = frontier[0]
            print(f"individual action: {action}")
            board = result(board, action)
            print(f"new_board {board}")
            board_list.append(board)
            print(f"board_list: {board_list}")
            next_acts = make_frontier(board)
            frontier.remove(action)
            insert_tuple(next_acts, frontier)
            print(f"frontier/queue: {frontier}")
            print("min_value_act board: {}".format(board))
            if len(next_acts) == 0:
                print("board filled")
                board = find_parent_children()
            if v > value(board):
                optimal = init_frontier[init_frontier_act]
                print(f"optimal: {optimal}")
                v = value(board)
                if value(board) == -1:
                    return optimal
            print("value: {}".format(v))
            #print("'Board' length: {}".format(len(board)))
            #print("all_actions #2: {}".format(all_actions))
    #optimal = all_actions[0]
    #return optimal
    
    def find_parent_children():
        '''Finds a parent with two or more children
        Variables:
        board_list: list of boards (explored set)
        ''' 
        print("find_parent_children --------------")
        index = -1
        counter = 0
        while counter <= len(board_list):
            print(f"find_parent_children, board_list: {board_list}")
            next_acts = make_frontier(board_list[index])
            if len(next_acts) >= 1 and next_acts != None:
                print(f"board that we backtracked to: {board_list[index]}")
                if abs(index) == len(board_list):
                    init_frontier_act += 1
                return board_list[index]
            index -= 1
            counter += 1
        print("find_parent_children == failed")

    def make_frontier(board):
        '''Keeps the branches that haven't been explored and removes the others'''
        print("frontier()")
        frontier = []
        next_acts = actions(board)
        for action in next_acts:
            new_board = result(board, action)
            if board_list.count(new_board) == 0:
                frontier.append(action)
                print(f"frontier: {frontier}")
        return frontier

    def max_value_act(board):
        '''Gets the maximum - highest value action'''
        print("------")
        print("max_value_act")
        v = -10
        optimal = ()
        for action in all_actions:
            if terminal(board):
                print("board = terminal")
                return None
            print("max_value_act board: {}".format(board))
            next_acts = actions(result(board, action))
            print("next_acts: {}".format(next_acts))
            if v < value(board):
                optimal = action
                v = value(board)
                if value(board) == 1:
                    return optimal
            all_actions.extend(next_acts)
            all_actions.remove(action)
            print("all_actions: {}".format(all_actions))
            print("value: {}".format(v))
            print("'Board' length: {}".format(len(board)))
        return optimal

    if turn == X:
        opt_act = max_value_act(new_board)
    elif turn == O:
        opt_act = min_value_act(new_board)
    return opt_act

def value(new_board):
    '''Gets the value of an action'''
    v = utility(new_board)
    return v

#print("minimax: {}".format(minimax(board)))

'''
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    turn = player(board)
    all_actions = actions(board)
    #value_list = []
    value = -100
    new_board = copy.deepcopy(board) # copying the original board
    for action in all_actions: # all first layer actions 
        new_board = result(new_board, action)
        print("new_board: {}".format(new_board))
        value = utility(new_board)
        print("value: {}".format(value))
        # if turn == X and value == 1:
        #     return action
        # elif turn == O and value == 1:
        #     all_actions.remove(action)
        #     pass
        # elif turn == X and value == -1:
        #     all_actions.remove(action)
        #     pass
        # elif turn == O and value == -1:
        #     return action
        # elif value == 0:
        #     next_layer_act = actions(new_board)
        #     if len(next_layer_act) > 0:
        #         all_actions.extend(next_layer_act)
        # turn = player(new_board)
    return all_actions[-1]
'''
'''
if value > 0 and player == X:
    priority_actions.insert(0, action)
elif value < 0 and player == O:
    priority_actions.insert(0, action)
elif value == 0:
    priority_actions.append(action)
'''

    #return the best action

    #raise NotImplementedError
