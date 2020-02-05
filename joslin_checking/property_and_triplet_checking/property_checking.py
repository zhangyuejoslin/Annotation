from property_and_triplet_checking import property_and_triplet_vocab
'''
block also means one of triangle, circle and square.
'''

def remove_s_es(word):
    if word.endswith('ies'):
        return word[0:len(word)-3]+'y'
    if word.endswith('s'):
        return word[0: len(word)-1]
    return word



'''
Spatial Properties: 
Color, Quantity, Shape, Size, Orientation, metric, Area
'''

def trajactor_or_landmark_check(form, unit_input, stru_rep): # output: return the corresponding kb x_loc anc y_loc
    result = []
    tower_result = []
    for sr in stru_rep:
        # tower_result.append((sr['x_loc']))
        sr['color'] = 'blue' if sr['color'] == '#0099ff' else sr['color'].lower()
        unit_input['text'] = 'box' if unit_input['color'] == 'grey' else unit_input['text']
        unit_input['color'] = 'None' if unit_input['color'] == 'grey' else unit_input['color']
        if sr['type'] == unit_input['text'] \
            and ( sr['color'].lower()==unit_input['color'] or unit_input['color']=='None' ) \
            and ( compute_size(sr['size']) == unit_input['size'] or unit_input['size']=='None' ):
                result.append([unit_input['text'], sr['x_loc'], sr['y_loc'], sr['size']])

        # maybe next step of work to text "tower"
        elif unit_input['text'] in property_and_triplet_vocab.entity_default():
            if unit_input['color'] == sr['color'].lower():
                result.append([unit_input['text'], sr['x_loc'], sr['y_loc']])
            elif unit_input['color']=='None':
                result.append([unit_input['text']])

    if len(set(tower_result)) == len(tower_result):
        result = []
        return result


    if unit_input['quantity'] != 'None' and len(result) < unit_input['quantity']: # check whether the quantity is correct.
        result = []
    return result

def prop_check(form, config, stru_rep):
    tr = form[config]['Spatial_Entity']['SPT'+str(config[-1])]
    lm = form[config]['Spatial_Entity']['SPL'+str(config[-1])]
    # if isinstance(tr, str):
    #     tr = form['Config'+tr[-1]]['Spatial_Entity'][tr]
    # if isinstance(lm, str):
    #     lm = form['Config'+lm[-1]]['Spatial_Entity'][lm]
    is_tr_correct = trajactor_or_landmark_check(form, tr, stru_rep)
    is_lm_correct = trajactor_or_landmark_check(form, lm, stru_rep)
    return dict(tr=is_tr_correct, lm=is_lm_correct)

def check_text(form, text, sr):
    # if text.startswith('SP'):
    #     text = form['Config'+text[-1]]['Spatial_Entity'][text]['text']
    #     print(text)
    text = remove_s_es(text)
    if text == 'None' or text in property_and_triplet_vocab.entity_default():
        return 1
    else:
        for d in sr:
            if d['type'] == text:
                return 1
        return 0

'''
'structured_rep': [[{'y_loc': 21, 'size': 20, 'type': 'triangle', 'x_loc': 27, 'color': 'Yellow'}]]
sr: structured_rep
text: the value of dict['type'] show in structured_rep
'''
def check_color(form, color, sr, text):
    if color == 'None':
        return 1
    else:
        for d in sr:
            if d['type'] == text.lower() and d['color'].lower() == color:
                return 1
        return 0

def check_size(form, size, sr, text):
    if size == 'None':
        return 1
    else:
        for d in sr:
            if d['type'] == text.lower() and compute_size(d['size']) == size:
                return 1
        return 0

def check_shape(form, shape, sr, text):
    if shape == 'None':
        return 1
    else:
        for d in sr:
            if d['type'] == text.lower() and d['shape'] == shape:
                return 1
        return 0

def compute_size(x):
    if x == 10:
        return "small"
    if x == 20:
        return "middle"
    if x == 30:
        return "large"


def check_quantity(form, quentity, sr, text):
    return 1
    if quentity == 'None':
        return 1
    else:
        count = 0
        for d in sr:
            if d['type'] == text.lower():
                count+=1
        # print('--------->', count, quentity)
        if count >= int(quentity):
            return 1
        return 0

def property_unit_test():
    return 0

'''
yue zhang code
'''
def check_area(form, area, sr, text):
    # eg. in the corner of, side, top, bottom, blabla....
    return 1

def check_metric(form, metric, sr, text):
    # what's the meaning of metric? Maybe metric is only working for the Navigation.
    return 1