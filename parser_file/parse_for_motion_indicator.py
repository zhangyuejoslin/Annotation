import json

#parsing the json_file into sentence units
#in some situation that one line contains more than one period
def parsing(json_file):
    sentence_index = []
    token_index = []
    token_text = []
    find_sentence = []
    #sentence_token_dictionary = []
    sentence_text = []
    sentence = json_file['_referenced_fss']['12']['sofaString']+"\n"

    for each_sentence in json_file['_views']['_InitialView']['Sentence']:
        if "begin" not in list(each_sentence.keys()):
            each_sentence['begin'] = 0
        find_sentence.append(each_sentence['begin'])
        if sentence[each_sentence['end']] == '\n':
            sentence_index.append((find_sentence[0], each_sentence['end']))
            sentence_text.append(sentence[find_sentence[0]:each_sentence['end']])
            find_sentence = []
    for each_token in json_file['_views']['_InitialView']['Token']:
        if "begin" not in list(each_token.keys()):
            each_token['begin'] = 0
        token_index.append((each_token["begin"], each_token['end']))
        token_text.append(sentence[each_token["begin"]:each_token['end']])
    new_sentence_list = zip(sentence_text, sentence_index)
    new_token_list = zip(token_text, token_index)

    for sentence_text, sentence_index in new_sentence_list:
       each_token_text = []
       spatial_roles = []
       spatial_relations = []
       fss = {}
       each_element = {}
       for token_text, token_index in new_token_list:
           if token_index[0] >= sentence_index[0]:
               each_token_text.append((token_text, token_index))
               if token_index[1] >= sentence_index[1]:
                   break
       for item1 in json_file['_referenced_fss'].items():
                if item1[0] != "12":
                     if 'begin' not in item1[1].keys():
                         item1[1]['begin'] = 0
                     if item1[1]['begin'] >= sentence_index[0] and item1[1]['end'] <= sentence_index[1]:
                         fss[item1[0]] = item1[1]
       for item2 in json_file['_views']['_InitialView']['Spatial_roles']:
                if type(item2) != int:
                     if 'begin' not in item2.keys():
                         item2['begin'] = 0
                     if item2['begin'] >= sentence_index[0] and item2['end'] <= sentence_index[1]:
                          spatial_roles.append(item2)
       for item3 in json_file['_views']['_InitialView']['Spatial_role_relation']:
              if 'begin' not in item3.keys():
                  item3['begin'] = 0
              if item3['begin'] >= sentence_index[0] and item3['end'] <= sentence_index[1]:
                  spatial_relations.append(item3)
       yield sentence_index, sentence_text, each_token_text, fss, spatial_roles, spatial_relations


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
    spatial_and_motion_indicator = []
    for fs in fss:
        if fs[1].get('spatial_indicator') == "spatial_indicator":
            spatial_and_motion_indicator.append((fs[0],(fs[1]['begin'], fs[1]['end'])))
        if fs[1].get('motion_indicator') == "motion_indicator":
            spatial_and_motion_indicator.append((fs[0],(fs[1]['begin'], fs[1]['end'])))
    return spatial_and_motion_indicator


def get_property(search_id, spatial_roles, token_dictionary):
    property_dict = {}
    for spatial_role in spatial_roles:
        for property in spatial_role["properties"]:
            if property['target'] == search_id:
                property_dict[property['role']] = tokenindex_to_text(token_dictionary, (spatial_role['begin'], spatial_role['end']))
    if property_dict:
        return property_dict
    else:
        return {}
#                 spatial_property_list.append((property['target'], (property['role'],(spatial_role['begin'], spatial_role['end']))))
#     return spatial_property_list

# return property type and text
def check_property(property_list, target_num, dictionary):
    each_property_list = []
    for property in property_list:
        if int(target_num) == property[0]:
            each_property_list.append((property[1][0], tokenindex_to_text(dictionary,property[1][1])))
    return each_property_list

def get_configuration_type(relation):
    if "Motions" in relation.keys():
        return "Motions:"+relation['Motions']
    elif "Topology" in relation.keys():
        return "Topology:" + relation['Topology']
    elif "Distance" in relation.keys():
        return "Distance:" + relation['Distance']
    elif "Direction" in relation.keys():
        return "Direction:" + relation['Direction']


def format_representation(motion_indicator, spatial_indicator, trajector, landmark, config_index, relation, steps):
    each_configuration ={}
    each_configuration['spatial_entity'] = {}
    if motion_indicator:
        each_configuration['spatial_entity']['SPM'] = motion_indicator
    if trajector:
        each_configuration['spatial_entity']['SPT'] = trajector
        each_configuration['spatial_entity']['SPI'] = spatial_indicator
        each_configuration['spatial_entity']['SPL'] = landmark
    each_configuration['id'] = str(config_index)
    each_configuration['type'] = relation
    each_configuration['distance'] = "close"
    each_configuration['step'] = steps
    return each_configuration

def form_representation_generation(each_element):
    all_configurations = []
    for sentence_index, sentence_text, token_dictionary, fss, spatial_roles, spatial_relations in each_element:
        Configuration = {}
        configure_list = []
        element_index = 1
        for relation in spatial_relations:
             SPI = []
             SPL = []
             SPM = {}
             SPT = {}
             seem_SPI = []
             # get SPM
             if fss[str(relation['Governor'])].get('motion_indicator') == "motion_indicator":
                 SPM = get_property(relation['Governor'],spatial_roles,token_dictionary)
                 SPM['text'] = tokenindex_to_text(token_dictionary,(fss[str(relation['Governor'])]["begin"],fss[str(relation['Governor'])]["end"]))
                 SPM['index'] = (fss[str(relation['Governor'])]["begin"],fss[str(relation['Governor'])]["end"])
             # get SPL
             if fss[str(relation['Dependent'])].get("spatial_entity"):
                     for spatial_entity in fss[str(relation['Dependent'])].get("spatial_entity"):
                         if spatial_entity['role'] == "landmark":
                             each_landmark = get_property(relation['Dependent'], spatial_roles, token_dictionary)
                             each_landmark["text"] = tokenindex_to_text(token_dictionary,(fss[str(relation['Dependent'])]["begin"],fss[str(relation['Dependent'])]["end"]))
                             each_landmark['index'] = (fss[str(relation['Dependent'])]["begin"],fss[str(relation['Dependent'])]["end"])
                             if each_landmark not in SPL:
                                SPL.append(each_landmark)
                         if spatial_entity['target'] != relation['Governor']:
                              seem_SPI.append(spatial_entity['target'])
             #get SPT
             if fss[str(relation['Governor'])].get('spatial_entity'):
                 for spatial_entity in fss[str(relation['Governor'])].get("spatial_entity"):
                     if spatial_entity['role'] == "trajector":
                         SPT = get_property(relation['Governor'], spatial_roles, token_dictionary)
                         SPT["text"] = tokenindex_to_text(token_dictionary, (fss[str(relation['Governor'])]["begin"], fss[str(relation['Governor'])]["end"]))
                         SPT['index'] = (fss[str(relation['Governor'])]["begin"], fss[str(relation['Governor'])]["end"])
             # get SPI
             for spi in seem_SPI:
                     if fss[str(spi)].get('spatial_indicator') == "spatial_indicator":
                         temp_spi = get_property(spi, spatial_roles, token_dictionary)
                         temp_spi['text'] = tokenindex_to_text(token_dictionary,(fss[str(spi)]["begin"],fss[str(spi)]["end"]))
                         temp_spi['index'] = (fss[str(spi)]["begin"],fss[str(spi)]["end"])
                         SPI.append(temp_spi)
             # writhe formal representation
             each_configuration = {}
             each_configuration['spatial_entity'] = {}
             each_configuration['type'] = get_configuration_type(relation)
             each_configuration['distance'] = "close"
             each_configuration['step'] = relation.get('Steps')
             each_configuration['id'] = str(element_index)
             if SPM:
                each_configuration['spatial_entity']['SPM'] = SPM
             if SPT:
                each_configuration['spatial_entity']['SPT'] = SPT
             if len(SPI) == 1:
                each_configuration['spatial_entity']['SPI'] = SPI[0]
             if len(SPL) == 1:
                each_configuration['spatial_entity']['SPL'] = SPL[0]
             configure_list.append(each_configuration)
             element_index += 1
        Configuration['config'] = configure_list
        all_configurations.append(Configuration)
    return all_configurations

        #      Configuration['Config'+str(element_index)] = {}
        #      Configuration['Config'+str(element_index)]['spatial_entity'] = {}
        #      Configuration['Config'+str(element_index)]['type'] = get_configuration_type(relation)
        #      Configuration['Config' + str(element_index)]['distance'] = "close"
        #      Configuration['Config'+str(element_index)]['step'] = relation.get('Steps')
        #      if SPM:
        #         Configuration['Config'+str(element_index)]['spatial_entity']['SPM' + str(element_index)] = SPM
        #      if SPT:
        #         Configuration['Config'+str(element_index)]['spatial_entity']['SPT' + str(element_index)] = SPT
        #      if len(SPI) == 1:
        #          Configuration['Config'+str(element_index)]['spatial_entity']['SPI'+str(element_index)] = SPI[0]
        #      if len(SPL) == 1:
        #          Configuration['Config'+str(element_index)]['spatial_entity']['SPL'+str(element_index)] = SPL[0]
        #      element_index += 1
        # all_configurations.append(Configuration)
    # return all_configurations


if __name__ == '__main__':
        with open("../annotated_data/webanno_file/R2R/r_r_9.json", 'r') as load_f:
            load_dict = json.load(load_f)

        with open("../annotated_data/formal_expression_for_r2r_test/r2r_form9.json", "w") as f:
            for item in form_representation_generation(parsing(load_dict)):
                f.write(json.dumps(item))
                f.write(',')
                f.write('\n')