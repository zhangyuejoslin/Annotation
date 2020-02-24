import json
import os

with open("../annotated_data/formal_expression_for_r2r/r2r_form1.json") as f1:
    text_data = json.load(f1)

with open("../annotated_data/image_feature/R2R_image_feature/image_representation1.json") as f2:
    image_data = json.load(f2)

def get_pose(image_id):
        for image in image_data:
            if image['image_id'] == image_id:
                return image['pose']

def next_motion(motion_type, start_point, end_point):
    if motion_type == "Motions:Forward":
        if end_point[0] > start_point[0] and abs(end_point[1] - start_point[1])<=0.3:
            return end_point
    if motion_type == "Motions:Right":
        if end_point[0] > start_point[0] and abs(end_point[1] - start_point[1])<=0.3:
            return end_point

def get_related_path(start_point):
    for image in image_data:
        if image["image_id"] == start_point:
            related_image = image['path']
    return  related_image

def object_detection(distance_type, text_object, image_object):
   if distance_type == "close":
       if text_object in image_object:
           return True

def get_object(image_id):
    for image in image_data:
        if image["image_id"] == image_id:
            related_objects = image['objects']
    return  related_objects


def path_checking(start_point, configure):
    next_point = start_point
    path = []
    path.append(start_point)
    for config_num, config_content in configure.items():
        while True:
            # one step
            for each_related_image in get_related_path(next_point):
                if next_motion(config_content['type'], get_pose(next_point), get_pose(each_related_image)):
                    print(config_num)
                    next_point = each_related_image
                    path.append(next_point)
                    print(path)
                    break

            # if achieve the objective of the configuration
            if not object_detection(config_content['distance'],config_content['spatial_entity']['SPL'+config_num[6:]]['text'],get_object(each_related_image)):
                break
    print(path)

if __name__ == '__main__':


     new_iamge_representation = []
     for configure in text_data:
        start_point = "10c252c90fa24ef3b698c6f54d984c5c"
        path_checking(start_point, configure)
        break