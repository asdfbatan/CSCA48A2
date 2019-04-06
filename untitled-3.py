def tryit():
    truee = True
    falsee = False
    return int(truee)

def build_tree(formula):
    '''
    (String) -> FormulaTree
    This function takes in a string representation of formula.
    Returns the FormulaTree which represents the given formula if vaild.
    Otherwise None is returned.
    REQ: the formula given must be a string representation
    '''
    # the base case of a leaf on the tree is that only one lowercase letter
    if len(formula) == 1 and islower():
        # build one leaf of the tree
        return leaf(formula)
    elif formula[0] == "-":
        return NotTree(build_tree(formula[1:]))
    elif formula[0] == "(":
        index = _get_index(formula, 0)
        if formula[index] == "+":
            return OrTree(build_tree(formula[1:index-1]), build_tree(formula[index+1:-1]))
        elif formula[index] == "*":
            return AndTree(build_tree(formula[1:index-1]), build_tree(formula[index+1:-1]))
    else:
        return None



def _get_place(formula):
    '''
    (string) -> int
    This is a private helper function to the function build_tree
    It can find the place where the first connection symbol in the blanket is
    and return its position in the original formula for use
    REQ: orig_formula must be a string representation
    REQ: index must be a interger
    '''
    # find the place of first "+"
    count1 = formula.count("+")
    n = 1
    while n <= count1:
        index1 = find_appear_by_time("+", formula, n)
        index1_ava = check_if_right(formula, index1)
        if index1_ava:
            return index1
        n += 1
    
    # find the place of first "*"
    count2 = formula.count("*")
    n = 1
    while n <= count2:
        index2 = find_appear_by_time("*", formula, n)
        index2_ava = check_if_right(formula, index2)
        if index2_ava:
            return index2
        n += 1    



def check_if_right(formula, index):
    left_count = formula.count("(", 0, index) - formula.count(")", 0, index) == 1
    right_count = formula.count(")", index) - formula.count("(", index) == 1
    return left_count and left_count
#字符串n次出现的位置 
def find_appear_by_time(substr, str, i):
    count = 0
    while i > 0:
        index = str.find(substr)
        if index == -1:
            return -1
        else:
            str = str[index+1:]   #第一次出现的位置截止后的字符串
            i -= 1
            count = count + index + 1   #字符串位置数累加
    return count - 1




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
    # the base case of a leaf on the tree is that only one lowercase letter
    if len(formula) == 1 and formula[0].islower():
        # build one leaf of the tree
        result = Leaf(formula)
    # if the formula starts with "-", it means a not tree
    elif formula[0] == "-":
        # build a NotTree and send the rest of the formula into the recursion
        result = NotTree(build_tree(formula[1:]))
    # for the symbol "+", "*", there must be a blanket before and after them
    elif formula[0] == "(":
        # here calls a helper function to find the place where the first symbol in the blanket is
        index = _get_place(formula)
        # build an AndTree, remove the blanket
        # apart the formula to two parts: before the "*" and after
        # send both parts into the recursion to get result for the AndTree
        if formula[index] == "*":
            result = AndTree(build_tree(formula[1:index]), build_tree(formula[index+1:-1]))
        # same step of "+" as the "*" above
        elif formula[index] == "+":
            result = OrTree(build_tree(formula[1:index]), build_tree(formula[index+1:-1]))
    # 'else' means the formula is not valid, therefore None is returned as required
    else:
        return None
    '''if build_tree(formula).find("None"):
        return None'''
