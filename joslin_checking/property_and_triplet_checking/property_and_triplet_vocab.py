metric_vocab = ['']
area_vocab = ['corner', 'side', ]
item_vocab = ['box', 'tower', 'boxes', 'towers', ]

# Ontology
TOPOLOGY = ['DC', 'EC', 'TPP', 'NTPP']
DIRECTION = ['ABOVE', 'BELOW', 'LEFT', 'RIGHT'] # 'FRONT', 'BACK',

# quantity word
exact_word = ['exactly', 'exact', 'equal', 'equally', 'equally', 'only']
greater_word = ['at least', 'greater than']
less_word = ['at most', 'less than']

# EC word
ec_word = ['touch', 'touched', 'touches', 'attached', 'attached to',]

def entity_default():
    return ['one', 'top', 'box', 'ones', 'side', 'other', 'block', 'towers', 'edge', 'item', 'line', 'blocks', 'objects', 'items', 'together', 'corner', 'each', 'tower', 'base', 'it', 'its', 'objects', 'object', 'boxes', 'wall']

side_word = ['edge', 'side', 'corner', 'wall', 'base']
box_word = ['box', 'boxes']
tower_word = ['tower', 'towers']