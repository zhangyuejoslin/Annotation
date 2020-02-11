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
    topo_or_dir = form[config]['type'].split(':')
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
    ## TPP, most belong to checking_with_NLVR the quantity
    elif topo_or_dir_value == 'TPP':
        res = compute_tpp(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    elif topo_or_dir_value == 'PP':
        res = compute_pp(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
    elif topo_or_dir_value == 'NTPP':
        res = compute_pp(form, config, tr, lm, ind, stru_rep, prop_check)
        return res
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
            return [li[1]]
        else: 
            return li
    else:
        return li



def compute_ec(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props)
    # print(lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif tr_props[0][0] in property_and_triplet_vocab.side_word or tr_props[0][0] in property_and_triplet_vocab.box_word:

        for lm_prop in lm_props:
            if tpp_formula(lm_prop[1], lm_prop[2], lm_prop[3], 0, 0, 100):
                return True
            else:
                return False
    elif lm_props[0][0] in property_and_triplet_vocab.side_word or lm_props[0][0] in property_and_triplet_vocab.box_word:

        for tr_prop in tr_props:
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100):
                return True
            else:
                return False
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if ec_formula(tr_prop[1], tr_prop[2], tr_prop[3], lm_prop[1], lm_prop[2], lm_prop[3]):
                    return True
    return False

def compute_dc(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props)
    # print(lm_props)

    if tr_props == [] or lm_props == []:
        return False
    elif lm_props[0][0] in property_and_triplet_vocab.side_word or lm_props[0][0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100) == False:
                return True
            # elif dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], 100, 100, 0)==True:
            #     return False
            else:
                return False
    elif tr_props[0][0] in property_and_triplet_vocab.side_word or tr_props[0][0] in property_and_triplet_vocab.box_word:
        for lm_prop in lm_props:
            if dc_formula(lm_prop[1], lm_prop[2], lm_prop[3], 0, 0, 100) == False:
                return True
            # elif dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], 100, 100, 0)==True:
            #     return False
            else:
                return False
    else:
        for tr_prop in tr_props:
            for lm_prop in lm_props:
                if dc_formula(tr_prop[1], tr_prop[2], tr_prop[3], lm_prop[1], lm_prop[2], lm_prop[3]):
                    return True
    return False

def compute_tpp(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props)
    # print(lm_props)

    if tr_props == [] or lm_props == []:
        return False

    elif tr_props[0][0] in  property_and_triplet_vocab.side_word or tr_props[0][0] in property_and_triplet_vocab.box_word:
        for lm_prop in lm_props:
            if tpp_formula(lm_prop[1], lm_prop[2], lm_prop[3], 0, 0, 100):
                return True


    elif lm_props[0][0] in property_and_triplet_vocab.side_word or lm_props[0][0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100):
                return True

    elif lm_props[0][0] in property_and_triplet_vocab.tower_word or tr_props[0][0] in property_and_triplet_vocab.tower_word:
        for tr_prop in tr_props:
            #80 sould be changed here
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100-20*len(tr_props)):
                return True
            # elif len(lm_props) != 0:
            #     return True
            else:
                return False

    elif tr_props[0] in property_and_triplet_vocab.box_word:
        if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
            return True
    elif tr_props[0] in property_and_triplet_vocab.tower_word:
        if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
            return True

    return False

def compute_ntpp(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])

    if tr_props == [] or lm_props == []:
        return False

    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word:
        for tr_prop in tr_props:
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100):
                return True
            else:
                return False
    elif lm_props[0][0] in property_and_triplet_vocab.tower_word or tr_props[0][0] in property_and_triplet_vocab.tower_word:
        for tr_prop in tr_props:
            #80 sould be changed here
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100):
                return True
            # elif len(lm_props) != 0:
            #     return True
            else:
                return False
    #
    # elif tr_props[0] in property_and_triplet_vocab.box_word:
    #     if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
    #         return True
    # elif tr_props[0] in property_and_triplet_vocab.tower_word:
    #     if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL'+str(config[-1])]['quantity']):
    #         return True

    return False


def compute_pp(form, config, tr, lm, ind, stru_rep, prop_check):
    tr_props = merge_same_list_to_one(prop_check['tr'])
    lm_props = merge_same_list_to_one(prop_check['lm'])
    # print(tr_props)
    # print(lm_props)
    item_true = []
    if tr_props == [] or lm_props == []:
        return False

    elif tr_props[0][0] in property_and_triplet_vocab.side_word or tr_props[0][0] in property_and_triplet_vocab.box_word:
        if lm_props[0][0] in property_and_triplet_vocab.new_item_word:
            for lm_prop in lm_props:
                if pp_formula(lm_prop[1], lm_prop[2], lm_prop[3], 0, 0, 100) == True:
                    item_true.append(True)

        else:
            for lm_prop in lm_props:
                if pp_formula(lm_prop[1], lm_prop[2], lm_prop[3], 0, 0, 100) == True:
                    return True
                else:
                    return False

        if len(item_true) == int(form[config]['Spatial_Entity']['SPL' + str(config[-1])]['quantity']):
            return True
        else:
            return False


    elif lm_props[0] in property_and_triplet_vocab.side_word or lm_props[0] in property_and_triplet_vocab.box_word :
        for tr_prop in tr_props:
            if pp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 100) == False:
                return True
            else:
                return False
    elif lm_props[0][0] in property_and_triplet_vocab.tower_word or tr_props[0][0] in property_and_triplet_vocab.tower_word:

        for tr_prop in tr_props:
            # 80 sould be changed here
            if tpp_formula(tr_prop[1], tr_prop[2], tr_prop[3], 0, 0, 80):
                return True
            # elif len(lm_props) != 0:
            #     return True
            else:
                return False

    # elif tr_props[0] in property_and_triplet_vocab.box_word:
    #
    #     if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL' + str(config[-1])]['quantity']):
    #         return True
    #
    # elif tr_props[0] in property_and_triplet_vocab.tower_word:
    #     if len(prop_check['lm']) == int(form[config]['Spatial_Entity']['SPL' + str(config[-1])]['quantity']):
    #          return True



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


    if tr_props == [] or lm_props == []:
        return False
    elif tr_props[0][0] in property_and_triplet_vocab.side_word or tr_props[0][0] in property_and_triplet_vocab.box_word:
        for lm_prop in lm_props:
            if is_above(lm_prop[1], lm_prop[2], 0, 0):
                return True
            elif is_above(lm_prop[1], lm_prop[2], 100, 0)==True:
                return True
    elif lm_props[0][0] in property_and_triplet_vocab.side_word or lm_props[0][0] in property_and_triplet_vocab.box_word:
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
    #print(tr_props, lm_props)

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
    if int(x1) == size1 or int(y1) == size1 or int(x1) == size2 or int(y1) == size2 or int(x1) + size1  == size2 or int(y1) + size1  == size2:
        return True
    else:
        return False

def tpp_formula(x1, y1, size1, x2, y2, size2):

    if int(x1) == size1 or int(y1) == size1 or int(x1) == size2 or int(y1) == size2 or int(x1) + size1  == size2 or int(y1) + size1  == size2:
        return True
    else:
        return False

def ntpp_formula(x1, y1, size1, x2, y2, size2):

    if int(x1) + size1  < size2 or int(y1) + size1  < size2:
        return True
    else:
        return False

def pp_formula(x1, y1, size1, x2, y2, size2):

    if int(x1) + size1  <= size2 or int(y1) + size1  <= size2:
        return True
    else:
        return False

def is_above(x1, x2, y1, y2):
    return True if y1 < y2 else False

def is_below(x1, x2, y1, y2):
    return True if y1 > y2 else False

def is_left(x1, x2, y1, y2):
    return True if x1 < x2 else False

def is_right(x1, x2, y1, y2):
    return True if x1 > x2 else False