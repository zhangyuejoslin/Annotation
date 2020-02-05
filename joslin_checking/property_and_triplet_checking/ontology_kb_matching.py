'''
Ontology:
Direction, TOPOLOGY
'''
# '''
# Direction
# '''
# def is_above(x1, x2, y1, y2):
#     return True if y1 < y2 else False

# def is_below(x1, x2, y1, y2):
#     return True if y1 > y2 else False

# def is_left(x1, x2, y1, y2):
#     return True if x1 < x2 else False

# def is_right(x1, x2, y1, y2):
#     return True if x1 > x2 else False

# # in fact, in 2d-image, it is unnecessary.
# def is_front(x1, x2, y1, y2):
#     return True if y1 < y2 else False

# def is_back(x1, x2, y1, y2):
#     return True if y1 < y2 else False

# '''
# TOPOLOGY:
# Externally connected (EC), 
# Disconnected (DC), 
# Proper part (PP), like contain, box with sth.
# '''
# def is_ec(x1, x2, size_1, y1, y2, size_2):
#     return True if ( (x1+size_1) == x2 ) or ( (x1-size_1) == x2 ) or\
#                    ((y1 + size_1) == y2) or ( (y1 - size_1) == y2 ) else False

# def is_dc(x1, x2, size_1, y1, y2, size_2):
#     return True if ((x1 + size_1) != x2) or ((x1 - size_1) != x2) or \
#                    ((y1 + size_1) != y2) or ((y1 - size_1) != y2) else False

# def is_tpp(x1, x2, y1, y2, keyword): # touch pp
#     return True if y1 < y2 else False

# def is_ntpp(x1, x2, y1, y2, keyword): # not touch pp
#     return True if y1 < y2 else False


'''
DISTANCE
'''
# NULL


'''
Property:
count-value, color-value, shape-value, size-value, spacial-value, logic-value, equal-value
'''

'''
count:
'''
def number_kb():
    # ignore 'any', 'odd', 'even'
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'an', 'two', 'three', 'four', 'five', 'six'
            'seven', 'eight', 'nine', 'some', 'all', ]

'''
color:
'''
def color_kb():
    return ['blue', 'yellow', 'black', ]
    # don't add 'color'
'''
shape
'''
def shape_kb():
    return ['triangle', 'circle', 'square']

def general_entity_kb():
    return ['block', 'item', 'blocks', 'items', 'object', 'objects', 'base', 'bases']

'''
If the head entity is just a general abstraction, then just return true, because they
are not have property.
'''
def always_correct_entity_kb():
    return ['box', 'boxes', 'towers', 'tower', 'wall', 'edge', 'base']

def pp_entity_kb():
    return ['box', 'boxes', 'towers', 'tower']
'''
size
'''
def size_kb():
    return ['small', 'middle', 'large']

'''
spacial
'''
def spacial_kb():
    return ['above', 'below', 'left', 'right', 'front', 'back']

'''
logic
'''
def logic_kb():
    return ['or', 'and', 'not', 'no']

'''
equal-value
'''
def equal_kb():
    return ['greater than', 'less than', 'at least', 'at most', 'exactly']

def compare_kb():
    return ['greater than', 'less than', 'different', 'equal', 'different', 'same', 'another']

'''
torching problem and tower problem
'''
# touching problem
def touching_word():
    return ['touch', 'touching']

def is_touching_wall(x, y):
    return True if (x == 0 or y == 0 or x == 100 or y == 100) else False


def is_touching_edge(x, y):
    return True if (x == 0 or y == 0 or x == 100 or y == 100) else False


def is_touching_corner(x, y):
    return True if ((x == 0 and y == 0) or (x == 0 and y == 100) or (x == 100 and y == 0) or (x == 100 and y == 100)) else False

def entity_kb():
    # return ['block', 'item', 'blocks', 'items', 'box', 'triangle', 'circle', 'square',
    #         'towers', 'tower', 'wall', 'edge', 'base', 'triangles', 'circles', 'squares',
    #         'object', 'objects']
    return ['one', 'top', 'box', 'ones', 'side', 'triangles', 'other', 'circle', 'block',
            'triangle', 'towers', 'square', 'edge', 'item', 'line', 'squares', 'blocks',
            'objects', 'items', 'together', 'corner', 'each', 'tower', 'circles', 'circle',
            'base', 'it', 'its', 'black', 'objetcs', 'object', 'boxes', 'wall']

