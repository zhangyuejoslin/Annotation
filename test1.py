import json

num=0
image_feature = []
new_sentence = {}
with open("data/image_feature/image_feature.json", 'r') as load_f:
    for line in load_f:
        image_feature.append(line)
with open("data/raw_text.json", "w") as f:
        for sentence in image_feature:
            each_sentence = json.loads(sentence)
            new_sentence['Sentence_ID'] = str(num)
            new_sentence['Text'] = each_sentence['sentence']
            f.write(json.dumps(new_sentence))
            f.write(',')
            f.write('\n')
            num+=1
            # import sys
            # sys.exit()
