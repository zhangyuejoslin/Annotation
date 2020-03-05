import stanfordnlp
import json

with open("generation_data/generation_file1.txt") as f_text:
    sentence = f_text.read().split('\n')
with open("generation_data/dictionary.txt") as f_dict:
    dictionary = f_dict.read().split('\n')
with open("generation_data/stop_word.txt") as f_stop_word:
    stopword = f_stop_word.read().split('\n')

stanfordnlp.download('en')
nlp = stanfordnlp.Pipeline()
left_vocabulary = ["turn left"]
right_vocabulary = ["turn right"]
close_distance = ['to', "into"]
far_distance = ['pass', "past"]

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
            elif "xcomp" in tag_list and tag_list[tag_list.index(each_tag)+1] == "xcomp":
                motion_indicator = text_list[tag_list.index(each_tag)] + " " + text_list[tag_list.index(each_tag) + 1]
            else:
                motion_indicator = text_list[tag_list.index(each_tag)]
        elif "case" in each_tag and each_tag == "case":
            spatial_indicator = text_list[tag_list.index(each_tag)]
        elif "det" in each_tag and each_tag == "det":
            landmark = " ".join(text_list[tag_list.index(each_tag)+1:])
    return motion_indicator, spatial_indicator, landmark

def form_expression(motion_indicator, spatial_indicator, landmark, config_index):
    each_configuration ={}
    each_configuration["spatial_entity"] = {}
    if motion_indicator:
        each_configuration["spatial_entity"]["SPM"] = {}
        each_configuration["spatial_entity"]["SPM"]= motion_indicator
    if spatial_indicator:
        each_configuration["spatial_entity"]["SPI"] = spatial_indicator
    if landmark:
        each_configuration["spatial_entity"]["SPL"] = landmark

    each_configuration["id"] = str(config_index)
    return each_configuration

if __name__ == '__main__':
    all_configurations = []
    for each_sentence in sentence:
        configuration = get_configuration(each_sentence)
        config_index = 1
        config_list = []
        config = {}
        for each_configuration in configuration:
            token_list, tag_list= get_dependency(each_configuration)
            motion_indicator, spatial_indicator, landmark = get_motion_spatial_indicator(token_list,tag_list)
            format_expression = form_expression(motion_indicator, spatial_indicator, landmark, config_index)
            config_list.append(format_expression)
            config["Config"] = config_list
            config_index += 1
        all_configurations.append(config)
    with open("generation_data/automatic_generation.json", "w") as f:
        for item in all_configurations:
                f.write(json.dumps(item))
                f.write(',')
                f.write('\n')









