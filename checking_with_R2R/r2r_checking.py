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

def next_motion(motion_type, start_id, end_id, direction):
    start_point = get_pose(start_id)
    end_point = get_pose(end_id)
    if direction == 1.5:
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
    elif direction == 3.0:
        if motion_type == "Motions:Forward":
         if end_point[1] < start_point[1] and abs(end_point[0] - start_point[0])<=0.5:
                return end_id
        elif motion_type == "Motions:Left":
            if end_point[1] < start_point[1] and end_point[0] > start_point[0] and abs(end_point[0] - start_point[0])>0.5:
                return end_id

def get_related_path(start_point):
    for image in image_data:
        if image["image_id"] == start_point:
            related_image = image['path']
    return  related_image

def object_text_image(text_object, image_object):
       if text_object in image_object:
           return True


def next_configuration(distance_type, text_object, type,direction, path):
    image_object = get_object(direction, path)
    if distance_type == "far":
        if text_object not in image_object:
            return True
    if distance_type == "close":
        if text_object in image_object:
            return True
        if type == "Motions:Right":
            direction+= 1.5
            image_object= get_object(direction,path)
            if text_object in image_object:
                return True


def get_object(direction, image_id):
        related_object = []
        for image in image_data:
            if image["image_id"] == image_id:
                for each_object in image['objects'].items():
                    if str(direction) in each_object[1]:
                        related_object.append(each_object[0])
        return related_object

def next_direction(direction, motion_type):
    if motion_type == "Motions:Forward":
            return direction
    elif  motion_type == "Motions:Right" or motion_type == "Motions:Turn Right":
            direction += 1.5
            return direction
    elif motion_type == "Motions:Left" or motion_type == "Motions:Turn Left":
            direction -= 1.5
            return direction

def second_viewer_for(direction, type, view_point, trajector):
    if type == "Direction:Right":
        direction += 1.5
    elif type == "Direction:Left":
        direction -= 1.5
    if trajector in get_object(direction, view_point):
        return True

def path_checking(start_point, start_direction, configure):
    next_point = start_point
    direction = start_direction
    direction_of_path = []
    path = []
    path.append(start_point)
    for config_num, config_content in configure.items():
        if config_content['type'] == "Motions:Stop":
            break

        if "Motions" not in config_content["type"]:
            if config_content.get("For") == "second":
                if second_viewer_for(direction,config_content["type"], next_point, config_content["spatial_entity"]["SPT" + config_num[6:]]["text"]):
                    continue
                else:
                    break
            else:
                continue

        while True:

            # if it is forward and you have seen the objective, then move,
            # if it is forward and you have not seen the objective, then don't move
            # if it is other direction and you have not seen the objective, then move
            # if you go forward , you must make sure that you can see something than you move
            # if you want to change direction,
            if 'SPL' + config_num[6:] not in config_content['spatial_entity'] \
                  or object_text_image(config_content['spatial_entity']['SPL' + config_num[6:]]['text'],get_object(direction, next_point)) or \
                     config_content['type'] != "Motions:Forward":
                for each_related_path in get_related_path(next_point):
                    next_motion_point = next_motion(config_content['type'], next_point, each_related_path, direction)

                    if next_motion_point is None:
                        continue
                    if next_motion_point != next_point:
                        next_point = each_related_path
                    direction_of_path.append(direction)
                    path.append(next_point)
                    break
            # if achieve the objective of the configuration
                if 'SPL' + config_num[6:] not in config_content['spatial_entity'] or \
                next_configuration(config_content['distance'],config_content['spatial_entity']['SPL'+config_num[6:]]['text'], config_content['type'], direction, each_related_path):
                    direction = next_direction(direction, config_content['type'])
                    break
            else:
                break

    direction_of_path.append(direction)
    print(direction_of_path)
    print(path)


if __name__ == '__main__':


     new_iamge_representation = []
     for configure in text_data:

        start_point = "10c252c90fa24ef3b698c6f54d984c5c"
        #start_point = "db145474a5fa476d95c2cc7f09e7c83a"
        # 0 is forward, 1 is right, 2 is left
        start_direction = 1.5
        path_checking(start_point, start_direction, configure)
        # break





