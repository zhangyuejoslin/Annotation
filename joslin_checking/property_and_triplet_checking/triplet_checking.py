from property_and_triplet_checking import ontology_kb_matching
from property_and_triplet_checking import property_and_triplet_vocab

def rel_check(form, config, stru_rep, prop_check):
    tr = form[config]['Spatial_Entity']['SPT'+str(config[-1])]
    lm = form[config]['Spatial_Entity']['SPL'+str(config[-1])]
    indicator = form[config]['Spatial_Entity']['SPI'+str(config[-1])]
    is_rel_correct = topo_or_dir_check(form, config, tr, lm, indicator, stru_rep, prop_check)
    return is_rel_correct

'''
Spatial Properties: 
Color, Quantity, Shape, Size, Orientation, metric, Area
'''
def topo_or_dir_check(form, config, tr, lm, ind, stru_rep, prop_check):
    topo_or_dir = form[config]['Type'].split(':')
    topo_or_dir_key, topo_or_dir_value = topo_or_dir[0], topo_or_dir[1]
    # print(prop_check)
    ## EC
    if topo_or_dir_value == 'EC':
        res = compute_ec(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## DC
    elif topo_or_dir_value == 'DC':
        res = compute_dc(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## TPP, most belong to checking the quantity
    elif topo_or_dir_value == 'TPP':
        res = compute_TPP(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## NTPP
    ## LEFT
    elif topo_or_dir_value == 'LEFT':
        res = compute_left(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## RIGHT
    elif topo_or_dir_value == 'RIGHT':
        res = compute_right(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## ABOVE
    elif topo_or_dir_value == 'ABOVE':
        res = compute_above(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## BELOW
    elif topo_or_dir_value == 'BELOW':
        res = compute_below(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    ## FRONT
    ## BEHIND
    return False


def merge_same_list_to_one(li):
    if len(li) >= 2:
        if li[0] == li[1]:
            return li[1]
        else: 
            return li
    else:
        return li

def compute_ec(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 0):
                return True
            elif ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], 100, 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], lm_prop[1], lm_prop[2], lm_prop[3]):
                    return True
    return False

def compute_dc(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 0):
                return True
            elif dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], 100, 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], lm_prop[1], lm_prop[2], lm_prop[3]):
                    return True
    return False

def compute_TPP(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 0):
                return False
            elif ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], 100, 100, 0)==True:
                return False
    elif tr_props[0] in property_and_triplet_vocab.box_word:
        if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
            return True
    elif tr_props[0] in property_and_triplet_vocab.tower_word:
        if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
            return True
    return False

def compute_left(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if is_left(tr_prop[1], tr_prop[2], 0, 0):
                return True
            elif is_left(tr_prop[1], tr_prop[2], 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if is_left(tr_prop[1], tr_prop[2], lm_prop[1], lm_prop[2]):
                    return True
    return False

def compute_right(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if is_right(tr_prop[1], tr_prop[2], 0, 0):
                return True
            elif is_right(tr_prop[1], tr_prop[2], 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if is_right(tr_prop[1], tr_prop[2], lm_prop[1], lm_prop[2]):
                    return True
    return False

def compute_above(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if is_above(tr_prop[1], tr_prop[2], 0, 0):
                return True
            elif is_above(tr_prop[1], tr_prop[2], 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if is_above(tr_prop[1], tr_prop[2], lm_prop[1], lm_prop[2]):
                    return True
    return False

def compute_below(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props, lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if is_below(tr_prop[1], tr_prop[2], 0, 0):
                return True
            elif is_below(tr_prop[1], tr_prop[2], 100, 0)==True:
                return True
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if is_below(tr_prop[1], tr_prop[2], lm_prop[1], lm_prop[2]):
                    return True
    return False

def ec_formula(x1, y1, size1, x2, y2, size2):
    if int(x1) + int(size1) == int(x2) or int(x2) + int(size2) == int(x1) or int(y1) + int(size1) == int(y2) or int(y2) + int(size2) == int(y1):
        return True
    else:
        return False

def dc_formula(x1, y1, size1, x2, y2, size2):
    if int(x1) + int(size1) == int(x2) or int(x2) + int(size2) == int(x1) or int(y1) + int(size1) == int(y2) or int(y2) + int(size2) == int(y1):
        return False
    else:
        return True

def is_above(x1, x2, y1, y2):
    return True if y1 < y2 else False

def is_below(x1, x2, y1, y2):
    return True if y1 > y2 else False

def is_left(x1, x2, y1, y2):
    return True if x1 < x2 else False

def is_right(x1, x2, y1, y2):
    return True if x1 > x2 else False