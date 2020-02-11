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
    return ['one', 'top', 'box', 'ones', 'side', 'other', 'block', 'edge', "object", "objects","item", "items", 'line', 'blocks', 'together', 'corner', 'each', 'tower', 'base', 'it', 'its', 'object', 'boxes', 'wall']

number = {"a": 1, "an": 1, "two":2}
side_word = ['edge', 'side', 'corner', 'wall', 'base']
box_word = ['box', 'boxes', 'wall']
tower_word = ['tower', 'towers']
item_word = ['object', 'objects', "item", "items"]
new_item_word = ["item", "items",'block']
mixed_words = ["box", "boxes", 'object', 'objects','wall', 'items', 'item', "tower", 'towers','exactly']