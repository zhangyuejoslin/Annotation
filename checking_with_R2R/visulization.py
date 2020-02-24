import json
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

with open("checking_data/graph_scenary_with_NEWID.json") as f_in:
    graph = json.load(f_in)


image_dic = {}
all_location = {}
new_image_representation = []
for image in graph:
    each_image_representation = {}
    temp_list = []
    #location = (image['pose'][3], image['pose'][7], image['pose'][11])
    location = (image['pose'][3], image['pose'][7])
    for num, link in enumerate(image['unobstructed']):
        if link == True:
            temp_list.append(graph[num]['NEW_ID'])
    image_dic[image['NEW_ID']] = temp_list
    all_location[image['NEW_ID']] = location
    # each_image_representation['new_id'] = image['NEW_ID']
    # each_image_representation['pose'] = location
    # each_image_representation['path'] = temp_list
    # each_image_representation['image_id'] = image['image_id']
    # each_image_representation['objects'] = ['something1', "something2"]
    # new_image_representation.append(each_image_representation)

# with open("../annotated_data/image_feature/R2R_image_feature/image_representation1.json", 'w') as fout:
#     json.dump(new_image_representation,fout, indent=4)


num = 0
for pic_key, pic_value in image_dic.items():
    plt.text(*all_location[pic_key], pic_key)
    for each_pic_value in pic_value:
            data = np.array([list(all_location[pic_key]), list(all_location[each_pic_value])])
            plt.plot(data[:, 0], data[:, 1], color='skyblue', label='y1')

plt.title('room path')
plt.xlabel('x')
plt.ylabel('y')
plt.show()







