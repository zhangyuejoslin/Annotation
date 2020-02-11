import json
import pandas
from property_and_triplet_checking import property_and_triplet_vocab

'''
Spatial Properties: 
color, quantity, shape, size, orientation, metric, area

Spatial Rel:
touching, touch --> touch
'''
def read_source_data(form_path, image_path):
    source_data = json.load(open(form_path, 'r'))

    img_data = json.load(open(image_path, 'r'))

    ### change source_data to the structure checked_data
    for form in source_data: # each sample
        for config in form.keys(): # each config in one sample
            # tr
            structure_formal_lang_tr_lm(form, config, 'SPT')
            # lm
            structure_formal_lang_tr_lm(form, config, 'SPL')
            # ind

    return source_data, img_data

def structure_formal_lang_tr_lm(form, config, flag):
    if isinstance(form[config]['Spatial_Entity'][flag+str(config[-1])], str):
        dict_hierarchy_above_tr_or_lm = form[config]['Spatial_Entity'][flag+str(config[-1])]
        form[config]['Spatial_Entity'][flag+str(config[-1])] = form['Config'+dict_hierarchy_above_tr_or_lm[-1]]['Spatial_Entity'][dict_hierarchy_above_tr_or_lm]
    form[config]['Spatial_Entity'][flag+str(config[-1])]['text'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('text', 'None')
    form[config]['Spatial_Entity'][flag+str(config[-1])]['color'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('color', 'None')
    form[config]['Spatial_Entity'][flag+str(config[-1])]['color'] = 'blue' if form[config]['Spatial_Entity'][flag+str(config[-1])]['color'] == '#0099ff' else form[config]['Spatial_Entity'][flag+str(config[-1])]['color']
    form[config]['Spatial_Entity'][flag+str(config[-1])]['shape'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('shape', 'None')
    form[config]['Spatial_Entity'][flag+str(config[-1])]['size'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('size', 'None')
    if str(form[config]['Spatial_Entity'][flag+str(config[-1])].get('quantity', 1)).isdigit():
        form[config]['Spatial_Entity'][flag + str(config[-1])]['compare'] = ''
    else:
        form[config]['Spatial_Entity'][flag+str(config[-1])]['compare'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('quantity', 1)
    form[config]['Spatial_Entity'][flag+str(config[-1])]['quantity'] = preprocessing_quantity(form, config, flag)
    form[config]['Spatial_Entity'][flag+str(config[-1])]['orientation'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('orientation', 'None')
    form[config]['Spatial_Entity'][flag+str(config[-1])]['metric'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('metric', 'None')
    form[config]['Spatial_Entity'][flag+str(config[-1])]['area'] = form[config]['Spatial_Entity'][flag+str(config[-1])].get('area', 'None')

def preprocessing_quantity(form, config, flag):
    ori = form[config]['Spatial_Entity'][flag+str(config[-1])].get('quantity', '1')
    ori = str(ori)
    spli = ori.split(' ')
    spli[-1] = change_string_to_num(spli[-1])
    if(len(spli)) == 1:
        ori = spli[-1]
    if spli[0] in property_and_triplet_vocab.exact_word:
        ori = spli[-1]

    if(len(spli))>2:
        if spli[0]+spli[1] == 'atmost':
            ori = 1
        elif spli[0]+spli[1] == 'atleast':
            ori = spli[-1]
        elif spli[0]+spli[1] == 'greaterthan':
            ori = spli[-1]
        elif spli[0]+spli[1] == 'lessthan':
            ori = 1
        elif spli[0] == 'exactly':
            ori = 0
    return int(ori)


def change_string_to_num(x):
    str_arr = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    int_arr = [1,2,3,4,5,6,7,8,9,10]
    ''' just check the box is contain this object '''
    if x == 'a' or x == 'an':
        x = 1
    elif x == 'some':
        x = 2
    elif x in str_arr:
        x = int_arr[str_arr.index(x)]
    return x
