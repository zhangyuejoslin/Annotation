import data_helper.data_preprocessing as data_pp
import property_and_triplet_checking.property_checking as pc
import property_and_triplet_checking.triplet_checking as tc

def check(src_data, img_data):
    correct_match_num = 0
    for form, base in zip(src_data, img_data):
        ## initial prediction and label
        # cur_label = 1 if base['label']=='true' else 0
        cur_pred = 0
        ## checking three pictures:
        final_correct = 0
        ### check all 3 image. As long as one of the image is correct, then end the base loop.
        for stru_rep in base['structured_rep']:

            rel_corrct = 1
            ### config_1 to config_n
            for config in form.keys():

                prop_check = pc.prop_check(form, config, stru_rep)
                rel_check = tc.rel_check(form, config, stru_rep, prop_check)


                if rel_check == False:
                    rel_corrct = 0
                    break
            if rel_corrct == 1:
                final_correct = 1
                break
        if final_correct == 1:
            print('Prediction: True ','Label: ', base['label'] )
        else:
            # print('False')
            print('Prediction: False ', 'Label: ', base['label'])

        # import sys
        # sys.exit()
    return 0


if __name__ == '__main__':
    src_data, img_data = data_pp.read_source_data('data/check_temp.json', 'data/check_image_feature.json')
    res = check(src_data, img_data)

