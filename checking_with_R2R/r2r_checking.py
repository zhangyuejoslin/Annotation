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
        if end_point[0] > start_point[0] and end_point[1] < start_point[1] and abs(end_point[1] - start_point[1])>0.3:
            return end_point

def get_related_path(start_point):
    for image in image_data:
        if image["image_id"] == start_point:
            related_image = image['path']
    return  related_image

def object_text_image(text_object, image_object):
       if text_object in image_object:
           return True

def next_configuration(distance_type, text_object, image_object):
    if distance_type == "far":
        if text_object not in image_object:
            return True
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
        if config_content['type'] == "Motions:Stop":
            break

        while True:

            # if it is forward and you have seen the objective, then move,
            # if it is forward and you have not seen the objective, then don't move
            # if it is other direction and you have not seen the objective, then move
          if config_content['type']!= "Motions:Forward" or object_text_image(config_content['spatial_entity']['SPL' + config_num[6:]]['text'],get_object(next_point)):
            for each_related_path in get_related_path(next_point):
                    if next_motion(config_content['type'], get_pose(next_point), get_pose(each_related_path)):
                        next_point = each_related_path
                        path.append(next_point)
                        break

            # if achieve the objective of the configuration
            if next_configuration(config_content['distance'],config_content['spatial_entity']['SPL'+config_num[6:]]['text'],get_object(each_related_path)):

                break
          else:
              break
    print(path)


if __name__ == '__main__':


     new_iamge_representation = []
     for configure in text_data:

        start_point = "10c252c90fa24ef3b698c6f54d984c5c"
        path_checking(start_point, configure)
        break