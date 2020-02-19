import json
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

with open("checking_data/graph_scenary_with_NEWID.json") as f_in:
    graph = json.load(f_in)


image_dic = {}
all_location = {}
for image in graph:
    temp_list = []
    #location = (image['pose'][3], image['pose'][7], image['pose'][11])
    location = (image['pose'][3], image['pose'][7])
    for num, link in enumerate(image['unobstructed']):
        if link == True:
            temp_list.append(graph[num]['NEW_ID'])
    image_dic[image['NEW_ID']] = temp_list
    all_location[image['NEW_ID']] = location

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







