import data_helper.data_preprocessing as data_pp
import property_and_triplet_checking.property_checking as pc
import property_and_triplet_checking.triplet_checking as tc

def check(src_data, img_data):
    correct_match_num = 0
    for form, base in zip(src_data, img_data):
        ## initial prediction and label
        cur_label = 1 if base['label']=='true' else 0
        cur_pred = 0
        ## checking three pictures:
        prop_correct = 1
        rel_corrct = 1
        ### check all 3 image. As long as one of the image is correct, then end the base loop.
        for stru_rep in base['structured_rep']:
            ### config_1 to config_n
            for config in form.keys():
                prop_check = pc.prop_check(form, config, stru_rep)
                # print('prop check:', prop_check)
                # rel_check = tc.rel_check(form, config, stru_rep)
    return 0


if __name__ == '__main__':
    src_data, img_data = data_pp.read_source_data('data/tmp.json', 'data/image_representation.json')
    res = check(src_data, img_data)

