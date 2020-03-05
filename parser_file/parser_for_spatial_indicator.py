import json

#parsing the json_file into sentence units
def parsing(json_file):
    sentence_list = []
    token_list = []
    sentence_token_dictionary = []
    for each_sentence in json_file['_views']['_InitialView']['Sentence']:
        if "begin" not in list(each_sentence.keys()):
            each_sentence['begin'] = 0
        sentence_list.append((each_sentence["begin"], each_sentence['end']))
    for each_token in json_file['_views']['_InitialView']['Token']:
        if "begin" not in list(each_token.keys()):
            each_token['begin'] = 0
        token_list.append((each_token["begin"], each_token['end']))
    sentence = json_file['_referenced_fss']['12']['sofaString'].split('\n')
    new_sentence_list = zip(sentence_list,sentence)
    for sentence_index, sentence_text in new_sentence_list:
        temp =[]
        token_text = []
        fss = []
        spatial_roles = []
        spatial_relations =[]
        each_element = {}
        each_element["sentence_index"] = sentence_index
        each_element['sentence_text'] = sentence_text
        for token_index in token_list:
            if token_index[0] >= sentence_index[0] and token_index[1] <= sentence_index[1]:
                temp.append(token_index)
        for item in zip(sentence_text.split(' '),temp):
            token_text.append(item)
        each_element['token_text'] = token_text
        for item1 in json_file['_referenced_fss'].items():
           if item1[0] != "12":
            if item1[1]['begin'] >= sentence_index[0] and item1[1]['end'] <= sentence_index[1]:
                fss.append(item1)
        for item2 in json_file['_views']['_InitialView']['Spatial_roles']:
             if type(item2) != int:
                 if item2['begin'] >= sentence_index[0] and item2['end'] <= sentence_index[1]:
                     spatial_roles.append(item2)
        for item3 in json_file['_views']['_InitialView']['Spatial_role_relation']:
                 if item3['begin'] >= sentence_index[0] and item3['end'] <= sentence_index[1]:
                     spatial_relations.append(item3)
        each_element['fss'] = fss
        each_element['spatial_roles'] = spatial_roles
        each_element['spatial_relations'] = spatial_relations
        sentence_token_dictionary.append(each_element)
    return sentence_token_dictionary

def tokenindex_to_text(dictionary, mathing_token):
    phrase = []
    for each_token_text in dictionary:
        if mathing_token[0] == each_token_text[1][0]:
            if  mathing_token[1] == each_token_text[1][1]:
                return each_token_text[0]
            else:
                for after_token_text in dictionary[dictionary.index(each_token_text):]:
                    phrase.append(after_token_text[0])
                    if mathing_token[1] == after_token_text[1][1]:
                        return " ".join(phrase)

def get_indicator(fss):
    spatial_indicator = []
    for fss in fss:
        if fss[1].get('spatial_indicator') == "spatial_indicator":
            spatial_indicator.append((fss[0],(fss[1]['begin'], fss[1]['end'])))
    return spatial_indicator

def get_property(spatial_roles):
    spatial_property_list = []
    for spatial_role in spatial_roles:
        for property in spatial_role["properties"]:
                spatial_property_list.append((property['target'], (property['role'],(spatial_role['begin'], spatial_role['end']))))
    return spatial_property_list

# return property type and text
def check_property(property_list, target_num, dictionary):
    each_property_list = []
    for property in property_list:
        if int(target_num) == property[0]:
            each_property_list.append((property[1][0], tokenindex_to_text(dictionary,property[1][1])))
    return each_property_list

def form_representation_generation(each_sentence):
    Configure = {}
    item_index = 1
    each_sentence_dictionary = each_sentence['token_text']
    indicator_list = get_indicator(each_sentence['fss'])
    property_list = get_property(each_sentence['spatial_roles'])
    relations  = each_sentence['spatial_relations']
    for each_indicator in indicator_list:
        trajector_and_entity = []
        Configure['config'+str(item_index)] = {}
        Configure['config'+str(item_index)]['Spatial_Entity'] = {}
        Configure['config'+str(item_index)]['Spatial_Entity']['SPT'+str(item_index)] = {}
        Configure['config'+str(item_index)]['Spatial_Entity']['SPL'+str(item_index)] = {}
        Configure['config'+str(item_index)]['Spatial_Entity']['SPI'+str(item_index)] = {}
        Configure['config' + str(item_index)]['Spatial_Entity']['SPI' + str(item_index)]['text'] = tokenindex_to_text(each_sentence_dictionary,(each_indicator[1][0],each_indicator[1][1]))
        for each_property in check_property(property_list, each_indicator[0], each_sentence_dictionary):
            Configure['config' + str(item_index)]['Spatial_Entity']['SPI' + str(item_index)][each_property[0]] = each_property[1]
        for fss in each_sentence['fss']:
            for role in fss[1]['spatial_entity']:
                if role.get('role') == 'trajector' and role.get('target') == int(each_indicator[0]):
                    trajector_and_entity.append(fss[0])
                    Configure['config' + str(item_index)]['Spatial_Entity']['SPT' + str(item_index)]['text'] = tokenindex_to_text(each_sentence_dictionary, (fss[1]['begin'], fss[1]['end']))
                    #maybe there are bugs for the entity of multipul configurations
                    for each_property in check_property(property_list, fss[0], each_sentence_dictionary):
                        Configure['config' + str(item_index)]['Spatial_Entity']['SPT' + str(item_index)][each_property[0]] = each_property[1]
                if role.get('role') == 'landmark' and role.get('target') == int(each_indicator[0]):
                    trajector_and_entity.append(fss[0])
                    Configure['config' + str(item_index)]['Spatial_Entity']['SPL' + str(item_index)]['text'] = tokenindex_to_text(each_sentence_dictionary, (fss[1]['begin'], fss[1]['end']))
                    for each_property in check_property(property_list, fss[0], each_sentence_dictionary):
                        Configure['config' + str(item_index)]['Spatial_Entity']['SPL' + str(item_index)][each_property[0]] = each_property[1]
        for rel in relations:
            #There should be more relations type, but those type maybe enough for NLVR
            if str(rel['Dependent']) in trajector_and_entity and str(rel['Governor']) in trajector_and_entity:
                if 'Topology' in rel.keys():
                    Configure['config' + str(item_index)]['Type'] = "TOP:" + rel['Topology']
                if 'Direction' in rel.keys():
                    Configure['config' + str(item_index)]['Type'] = "DIR:" + rel['Direction']
                if 'Distance' in rel.keys():
                    Configure['config' + str(item_index)]['Type'] = "DIS:" + rel['Direction']
        item_index+=1
    return Configure


if __name__ == '__main__':
    with open("../annotated_data/webanno_file/NLVR/NLVR4.json", 'r') as load_f:
        load_dict = json.load(load_f)
    with open("../annotated_data/formal_expression_for_NLVR/formal_expression4.json", "w") as f:
        for sentence in parsing(load_dict):
            print(sentence)
                  # f.write(json.dumps(form_representation_generation(sentence)))
                  # f.write(',')
                  # f.write('\n')








