# import json
#
# num=0
# image_feature = []
# new_sentence = {}
# with open("data/image_feature/image_feature.json", 'r') as load_f:
#     for line in load_f:
#         image_feature.append(line)
# with open("data/image_feature/new_image_feature.json", "w") as f:
#         for sentence in image_feature:
#             each_sentence = json.loads(sentence)
#             each_sentence['Sentence_ID'] =str(num)
#            # new_sentence['Sentence_ID'] = str(num)
#            #  new_sentence['Text'] = each_sentence['sentence']
#             f.write(json.dumps(each_sentence))
#             f.write(',')
#             f.write('\n')
#             num+=1
            # import sys
            # sys.exit()



# with open("data/raw_text.json", "r") as f:
#         for sentence in f:
#             sentence1 = sentence.strip().replace("\"},","").split(':')
#             sentence1[-1] = sentence1[-1].split(' ')
#
#             # if "with" not in sentence and  "box" not in sentence and  "edge" not in sentence and "wall" not in sentence and "tower" not in sentence \
#             #        and  "contains" not in sentence and "corner" not in sentence and "base" not in sentence and len(sentence1[-1])>=7 and "no" not in sentence\
#             #        and "grey square" not in sentence and "side" not in sentence and "block" not in sentence:
#             #                   print(sentence, end='')
#             if "touching" in sentence and "box" not in sentence and "wall" not in sentence and 'edge' not in sentence and "corner" not in sentence and 'base' not in sentence:                print(sentence, end='')


list1 = ['a','a']
print(len(set(list1)))