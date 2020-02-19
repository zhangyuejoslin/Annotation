import json

with open("checking_data/R2R_train.json") as f_in:
    graph = json.load(f_in)

new_graph = []
for each_data in graph:
    if each_data['scan'] == "17DRP5sb8fy":
        new_graph.append(each_data)

with open("checking_data/R2R_part_of_data.json",'w') as f_out:
    graph = json.dump(new_graph,f_out, indent=4)