import json
import math

with open("../annotated_data/formal_expression_for_r2r/r2r_form2.json") as f1:
    text_data = json.load(f1)

with open("../annotated_data/image_feature/R2R_image_feature/image_representation1.json") as f2:
    image_data = json.load(f2)

def  get_pose(image_id):
        for image in image_data:
            if image['image_id'] == image_id:
                return image['pose']

def next_motion(motion_type, start_id, end_id, direction):
    if motion_type == "Motions:Forward":
            if  -(math.radians(30)) < next_direction(start_id, end_id) - direction < math.radians(30):
                return  end_id
    elif motion_type == "Motions:Left":
            if next_direction(start_id,end_id) - direction < -(math.radians(30)):
                return end_id
    elif motion_type == "Motions:Right":
            if next_direction(start_id,end_id) - direction > math.radians(30):
                return end_id
    elif motion_type == "Motions:Turn Right":
        return start_id
    elif motion_type == "Motions:Turn Left":
        return start_id

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

def next_direction(start_point, end_point):
    radins = 0.0;
    x1 = get_pose(start_point)[0]
    y1 = get_pose(start_point)[1]
    x2 = get_pose(end_point)[0]
    y2 = get_pose(end_point)[1]
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        radins = math.pi / 2.0
        if y2 == y1:
            radins = 0.0
        elif y2 < y1:
            radins = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        radins = math.atan(dx / dy)
    elif x2 > x1 and y2 < y1:
        radins = math.pi / 2 + math.atan(-dy / dx)
    elif x2 < x1 and y2 < y1:
        radins = math.pi + math.atan(dx / dy)
    elif x2 < x1 and y2 > y1:
        radins = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return round(radins, 2)


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
    direction_of_path.append(direction)
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
                related_path = get_related_path(next_point)
                for each_related_path in related_path:
                    next_motion_point = next_motion(config_content['type'], next_point, each_related_path, direction)
                    if next_motion_point is None:
                        continue
                    else:
                        if config_content['type'] == "Motions:Turn Right":
                            direction = round((next_direction(next_point, next_motion_point) + math.radians(30)), 2)
                        elif config_content['type'] == "Motions:Turn Right":
                            direction = round((next_direction(next_point, next_motion_point) - math.radians(30)), 2)
                        else:
                            direction = next_direction(next_point, next_motion_point)
                    if next_motion_point != next_point:
                        next_point = each_related_path
                    direction_of_path.append(direction)
                    path.append(next_point)
                    break
                if next_motion_point is None:
                    break
            # if achieve the objective of the configuration
                if 'SPL' + config_num[6:] not in config_content['spatial_entity'] or \
                next_configuration(config_content['distance'],config_content['spatial_entity']['SPL'+config_num[6:]]['text'], config_content['type'], direction, each_related_path):
                    break

            else:
                break

    print(direction_of_path)
    print(path)


if __name__ == '__main__':


     new_iamge_representation = []
     for configure in text_data:

        start_point = "ee59d6b5e5da4def9fe85a8ba94ecf25"
        #start_point = "db145474a5fa476d95c2cc7f09e7c83a"
        #start_point = "10c252c90fa24ef3b698c6f54d984c5c"
        # 0 is forward, 1 is right, 2 is left
        start_direction =5.5
        #first 1.5, second 3.0, third 5.5
        path_checking(start_point, start_direction, configure)







