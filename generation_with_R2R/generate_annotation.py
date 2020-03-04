import stanfordnlp

with open("generation_data/generation_file1.txt") as f_text:
    sentence = f_text.read().split('\n')
with open("generation_data/dictionary.txt") as f_dict:
    dictionary = f_dict.read().split('\n')
with open("generation_data/stop_word.txt") as f_stop_word:
    stopword = f_stop_word.read().split('\n')

stanfordnlp.download('en')
nlp = stanfordnlp.Pipeline()

def post_processing_sentence(sentence_list):
    def func(sl):
        sl = sl.strip()
        sl = sl.strip(".")
        for sw in stopword:
            if sl.endswith(" %s"%sw):
                sl = sl[:-(len(sw)+1)]
        return sl
    sentence_list = list(map(func, sentence_list))
    return sentence_list

def get_configuration(each_sentence):
    sentence_list = []
    each_sentence = each_sentence.lower()
    sentence_list.append(each_sentence)
    for each_word in dictionary:
        for sl in sentence_list:
            if each_word in sl:
                index = sentence_list.index(sl)
                sentence_list.remove(sl)
                temp = sl.split(each_word)
                temp = [tt if temp.index(tt)== 0 else each_word+tt for tt in temp]
                for tt in temp:
                    if tt:
                        sentence_list.insert(index,tt)
                        index +=1
    sentence_list = post_processing_sentence(sentence_list)
    return sentence_list

def get_dependency(sentence):
    doc = nlp(sentence)
    temp = doc.sentences[0]
    token_list =[]
    tag_list = []
    for i in temp.dependencies:
        token_list.append(i[2].text)
        tag_list.append(i[1])
    return token_list,tag_list

def get_motion_spatial_indicator(text_list, tag_list):
    motion_indicator = ""
    spatial_indicator = ""
    landmark = ""
    for each_tag in tag_list:
        if each_tag == "root":
            if "advmod" in tag_list and tag_list[tag_list.index(each_tag)+1] == "advmod":
                motion_indicator = text_list[tag_list.index(each_tag)] + " " + text_list[tag_list.index(each_tag)+1]
            else:
                motion_indicator = text_list[tag_list.index(each_tag)]
        elif "case" in each_tag and each_tag == "case":
            spatial_indicator = text_list[tag_list.index(each_tag)]
        elif "det" in each_tag and each_tag == "det":
            landmark = " ".join(text_list[tag_list.index(each_tag)+1:])
    return motion_indicator, spatial_indicator, landmark

def form_expression(motion_indicator, spatial_indicator, landmark, index):
    Configure = {}
    Configure['Config'+str(index)] = {}
    Configure['Config' + str(index)]['spatial_entity']= {}
    if motion_indicator:
        Configure['Config' + str(index)]['spatial_entity']['SPM'+ str(index)] = motion_indicator
    if spatial_indicator:
        Configure['Config' + str(index)]['spatial_entity']['SPI'+ str(index)] = spatial_indicator
    if landmark:
        Configure['Config' + str(index)]['spatial_entity']['SPL'+ str(index)] = landmark
    return Configure


if __name__ == '__main__':
    for each_sentence in sentence:
        configuration = get_configuration(each_sentence)
        index = 1
        new_config = []
        for each_configuration in configuration:
            token_list, tag_list= get_dependency(each_configuration)
            motion_indicator, spatial_indicator, landmark = get_motion_spatial_indicator(token_list,tag_list)
            format_expression = form_expression(motion_indicator, spatial_indicator, landmark, index)
            new_config.append(format_expression)
            index += 1
        print(new_config)








