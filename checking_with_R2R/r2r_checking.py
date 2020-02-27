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

def next_motion(motion_type, start_id, end_id):
    start_point = get_pose(start_id)
    end_point = get_pose(end_id)

    if motion_type == "Motions:Forward":
        if end_point[0] > start_point[0] and abs(end_point[1] - start_point[1])<=0.5:
            return end_id
    elif motion_type == "Motions:Right":
        if end_point[0] > start_point[0] and end_point[1] < start_point[1] and abs(end_point[1] - start_point[1])>0.5:
            return end_id
    elif motion_type == "Motions:Left":
        if end_point[0] > start_point[0] and end_point[1] > start_point[1] and abs(end_point[1] - start_point[1]) > 0.5:
            return end_id
    elif motion_type == "Motions:Turn Right":
        return start_id
    else:
        return None

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

def next_direction(direction, motion_type):
    # 0 is north, 90 is east, 180 is south, and 270 is west.
    if motion_type == "Motions:Forward":
            return direction
    elif motion_type == "Motions:Right" or "Motions:Turn Right":
            direction += 30
            return direction
    elif motion_type == "Motions:Left" or "Motions:Turn Right":
            direction -= 30
            return direction

def path_checking(start_point, start_direction, configure):
    next_point = start_point
    direction = start_direction
    direction_of_path = []
    path = []
    path.append(start_point)
    direction_of_path.append(direction)
    for config_num, config_content in configure.items():

        if config_content['type'] == "Motions:Stop":
            break

        if "Motions" not in config_content['type']:
            continue

        while True:

            # if it is forward and you have seen the objective, then move,
            # if it is forward and you have not seen the objective, then don't move
            # if it is other direction and you have not seen the objective, then move

            # turn right to the hallway and if you go forward , you must make sure that you can see something than you move
            if 'SPL' + config_num[6:] not in config_content['spatial_entity'] \
                  or object_text_image(config_content['spatial_entity']['SPL' + config_num[6:]]['text'],get_object(next_point)) \
                  or config_content['type']!= "Motions:Forward":

                for each_related_path in get_related_path(next_point):
                    next_motion_point = next_motion(config_content['type'], next_point, each_related_path)
                    if next_motion_point is None:
                        continue
                    if next_motion_point != next_point:
                        next_point = each_related_path
                    direction = next_direction(direction, config_content['type'])
                    direction_of_path.append(direction)
                    path.append(next_point)
                    #print(config_num+"$$$")

                    break
            # if achieve the objective of the configuration
                if 'SPL' + config_num[6:] not in config_content['spatial_entity'] or \
                next_configuration(config_content['distance'],config_content['spatial_entity']['SPL'+config_num[6:]]['text'],get_object(each_related_path)):
                    break
            else:
                break
    print(direction_of_path)
    print(path)


if __name__ == '__main__':


     new_iamge_representation = []
     for configure in text_data:

        start_point = "10c252c90fa24ef3b698c6f54d984c5c"
        # 0 is forward, 1 is right, 2 is left
        start_direction = 90
        path_checking(start_point, start_direction, configure)
