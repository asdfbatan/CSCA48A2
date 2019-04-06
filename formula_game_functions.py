"""
# Zhang Ti zhan5263 1004424517
# Copyright Nick Cheng, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.
def build_tree(formula):
    '''
    (string) -> FormulaTree
    This function takes in a string representation of formula.
    Returns the FormulaTree which represents the given formula if vaild.
    Otherwise None is returned.
    REQ: the formula given must be a string representation
    '''
    # idea: this functon use recursion to be efficient
    #       apart the formula into small parts and build each leaf
    '''
    this is a fail part for testing valid formula
    symbol_list = "xyz+-*()"
    for char in formula:
        if symbol_list.find(char) != -1:
            pass
        else:
            return None
    '''
    # the base case of a leaf on the tree is that only one lowercase letter
    if len(formula) == 1 and formula[0].islower():
        # build one leaf of the tree
        return Leaf(formula)
    # if the formula starts with "-", it means a not tree
    elif formula[0] == "-":
        # build a NotTree and send the rest of the formula into the recursion
        return NotTree(build_tree(formula[1:]))
    # for the symbol "+", "*", there must be a blanket before and after them
    elif formula[0] == "(":
        # here calls a helper function to find the place where the first symbol in the blanket is
        index = _get_place(formula)
        # build an AndTree, remove the blanket
        # apart the formula to two parts: before the "*" and after
        # send both parts into the recursion to get result for the AndTree
        if formula[index] == "*":
            return AndTree(build_tree(formula[1:index]), build_tree(formula[index+1:-1]))
        # same step of "+" as the "*" above
        elif formula[index] == "+":
            return OrTree(build_tree(formula[1:index]), build_tree(formula[index+1:-1]))
    # 'else' means the formula is not valid, therefore None is returned as required
    else:
        return None


def _get_place(formula):
    '''
    (string) -> int
    This is a private helper function to the function build_tree
    It can find the place where the middle connection symbol in the blanket is
    and return its position in the original formula for use
    REQ: formula must be a string representation
    '''
    # find how many times "+" appears
    count1 = formula.count("+")
    # set the original value: the first time "+" appears
    n = 1
    while n <= count1:
        # find the place of nth "+"
        index1 = _find_appear_by_time("+", formula, n)
        # find if this "+" is the middle connection of the formula
        index1_ava = _check_if_right(formula, index1)
        # if it is, then return the index
        if index1_ava:
            return index1
        # if not, move forward
        n += 1
    # the same process as above for "*"
    count2 = formula.count("*")
    n = 1
    while n <= count2:
        index2 = _find_appear_by_time("*", formula, n)
        index2_ava = _check_if_right(formula, index2)
        if index2_ava:
            return index2
        n += 1    


def _check_if_right(formula, index):
    '''
    (string, int) -> bool
    This is a private helper function to the function _get_place
    to find if the given index position is the middle connection of the formula
    REQ: formula must be a string representation
    REQ: index must be a interger
    '''
    # idea: if the index is in the middle
    #       then on its left side
    #       # of "(" must be 1 figure bigger than # of ")"
    # count and compare the # of "(" ")" on the left side of index
    left_count = formula.count("(", 0, index) - formula.count(")", 0, index) == 1
    # count and compare the # of "(" ")" on the right side of index
    right_count = formula.count(")", index) - formula.count("(", index) == 1
    # if both sides are right, then the index is in the middle position
    return left_count and left_count


def _find_appear_by_time(symbol, formula, i):
    '''
    (string, string, int) -> int
    This is a private helper function to the function _get_place
    to find the place of nth symbol ouccurence
    REQ: symbol must be a string representation
    REQ: formula must be a string representation
    REQ: i must be a interger
    '''
    # set a variable counting the occ
    count = 0
    while i > 0:
        index = formula.find(symbol)
        # restore the formula after symbol first appear
        formula = formula[index+1:]
        i -= 1
        # accumulating the position number for the symbol
        count = count + index + 1
    return count - 1


def evaluate(root, variables, values):
    '''
    (FormulaTree, string, string) -> int
    This function takes in:
    1.a formula in the form of FormulaTree
    2.the variables in use
    3.a values' string representation correspongding to variables
    and it calculate the truth value and return the final result
    REQ: the root must be in the form of FormulaTree
    REQ: the variables must be string
    REQ: the values must be string
    REQ: the contents inthe string "values" must be "1" or "0"
    '''
    # idea: judge the type of the current positon
    #       and count them in corresponding ways
    # base case:every line of the FormulaTree ends with a leaf, so it's the base case
    if isinstance(root, Leaf):
        # idea: to get the value of the leaf, first get the variable of the leaf.
        #       then find the position of the leaf in the string "variables"
        #       then use the position index to fingd the value corresponding in "values"
        position = variables.index(root.get_symbol())
        # turn the value of the leaf into true or false for simplier calculation
        result_bool = values[position] == "1"
    # if the current position is a NotTree, calculate the reverse and send the children to recursion
    elif isinstance(root, NotTree):
        result_bool = not evaluate(root.get_children()[0], variables, values)
    # if it's AndTree, do the and calculation for both children and send them to recursion
    elif isinstance(root, AndTree):
        result_bool = evaluate(root.get_children()[1], variables, values) and evaluate(root.get_children()[0], variables, values)        
    # if it's OrTree, do the or calculation for both children and send them to recursion
    elif isinstance(root, OrTree):
        result_bool = evaluate(root.get_children()[0], variables, values) or evaluate(root.get_children()[1], variables, values)
    # turn the True or False result into integer "1", "0" respectively
    return int(result_bool)


def draw_formula_tree(root):
    '''
    (FormulaTree) -> string
    This function takes in a single input root of a FormulaTree
    call the hepler function as it needs more inputs
    then return a formula tree in a form of strings
    REQ: the root must be in the form of FormulaTree
    >>>root = build_tree("--(a+(b+(c+(d+e))))")
    >>>draw_formula_tree(root)
    >>>'- - + + + + e\n            d\n          c\n        b\n      a'
    '''
    # to make the line shorter
    result = draw_formula_tree_helper(root, "", 0)
    return result


def draw_formula_tree_helper(root, blank = "", level = 0):
    '''
    (FormulaTree, string, int) -> string
    This is a helper function to the function draw_formula_tree
    which construct the main operation to turn a FormulaTree into a string representation
    REQ: the root must be in the form of FormulaTree
    REQ: blank must be a string
    REQ: level must be an int
    '''
    # in case for the vairable name mentioned above
    global result_draw
    # idea: sort the type of the current place on FormulaTree, order them
    # for leaf (base case):
    if isinstance(root, Leaf):
        # number of "blank" shows the position of the leaf in the tree
        result_draw = blank * level + root.get_symbol()
    # for OrTree and AndTree, they both have two children, so it's the same
    elif isinstance(root, OrTree) or isinstance(root, AndTree):
        # first print the symbol out
        result_draw = blank * level + root.get_symbol() + " "
        # put the first child into recursion 
        result_draw += draw_formula_tree_helper(root.get_children()[1], "", level+1)
        # change the line
        result_draw += "\n"
        # put the second child into recursion with indents
        # to keep the same positionwith the first children
        result_draw += draw_formula_tree_helper(root.get_children()[0], "  ", level+1)
    # for NotTree:
    elif isinstance(root, NotTree):
        # first print the symbol out, then put the children of thfe NotTree into recursion
        result_draw = blank * level + root.get_symbol() + " " + draw_formula_tree_helper(root.get_children()[0], "", level+1)    
    return result_draw


def play2win(root, turns, variables, values):
    '''
    (FormulaTree, string, string, string) -> int
    This function takes in the necessary information of the formula game
    return the best next move for the player whose turn is next
    REQ: the root must be in the form of FormulaTree
    REQ: the turns must be string
    REQ: the variables must be string
    REQ: the values must be string
    '''
    # set the basic value of players
    player_a = "A"
    player_e = "E"
    # set the basic value of players' preferred result
    player_a_result = 0
    player_e_result = 1
    # get prefered result for e's turn
    if turns[len(values)] == player_e:
        goal = player_e_result
    # get prefered result for a's turn
    else:
        goal = player_a_result
    # choose 1 and 0 seperately to see the goal for each one
    choose_1 = _possible_to_win(root, turns, variables, values + "1", goal)
    choose_0 = _possible_to_win(root, turns, variables, values + "0", goal)
    # if choose 0 leads to win
    if choose_1 == bool(goal):
        result = 1
    # if choose 1 leads to win
    elif choose_0 == bool(goal):
        result = 0
    # if there's no winning strategy or both leads to win
    if (choose_0 and choose_1) or not(choose_0 and choose_1):
        result = goal    
    return result

def _possible_to_win(root, turns, variables, values, goal):
    '''
    (FormulaTree, string, string, string, string) -> bool
    This is a private helper function to the function play2win
    it shows whether it's possible to win or not
    REQ: the root must be in the form of FormulaTree
    REQ: the turns must be string
    REQ: the variables must be string
    REQ: the values must be string
    '''
    # Note: actually there won't be given 3 values at first
    #       so this "if" part is only write for recursion
    # if all the turns are complete, just evaluate
    if len(values) == len(turns):
        formula_result = evaluate(root, variables, values)
        # see if the bool is the same as goal wanted
        result = bool(formula_result) == goal
    # if the turns are not completed
    else:
        # try for choosing 0 this time to see if the result is as wanted
        result = _possible_to_win(root, turns, variables, values + "0", goal)
        # if the result is not the same as goal, try for choosing 1 this time
        if not result:
            result = _possible_to_win(root, turns, variables, values + "1", goal)
            # if both result are not as wanted, return 1 for E and 0 for A
            if not result:
                result = goal
    return result
