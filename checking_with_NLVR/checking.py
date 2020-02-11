import data_helper.data_preprocessing as data_pp
import property_and_triplet_checking.property_checking as pc
import property_and_triplet_checking.triplet_checking as tc
from property_and_triplet_checking import property_and_triplet_vocab
from collections import Counter


def check(src_data, img_data):
    correct_match_num = 0
    for form, base in zip(src_data, img_data):
        ## initial prediction and label
        # cur_label = 1 if base['label']=='true' else 0
        cur_pred = 0
        ## checking_with_NLVR three pictures:
        final_correct = []

        ### check all 3 image. As long as one of the image is correct, then end the base loop.
        for config in form.keys():
            rel_correct = []
            quantity_for_box = 0
            for stru_rep in base['structured_rep']:
                tr = form[config]['Spatial_Entity']['SPT' + str(config[-1])]
                lm = form[config]['Spatial_Entity']['SPL' + str(config[-1])]
                if tr['text'] in property_and_triplet_vocab.mixed_words and tr['quantity'] != 'None' and "exactly" in tr['compare']:
                    quantity_for_box = tr['quantity']

                prop_check = pc.prop_check(form, tr, lm , stru_rep)
                rel_check =tc.rel_check(form, config, stru_rep,prop_check)
                rel_correct.append(rel_check)

            #print(quantity_for_box)
            #print(rel_correct)

            rel_correct = Counter(rel_correct)

            if rel_correct[False] == 3:

                final_correct.append(False)

            elif rel_correct[True] == 3:

                final_correct.append(True)
            elif quantity_for_box>0  and quantity_for_box != rel_correct[True]:
                final_correct.append(False)


            else:
                final_correct.append(True)

        if len(set(final_correct)) == 1 and final_correct[0] == True:
            print('Prediction: True ', 'Label: ', base['label'])
        else:
            print('Prediction: False', 'Label: ', base['label'])
        # else:
        #     print(final_correct)
        # correct_match_num +
        # print(correct_match_num)

        # for stru_rep in base['structured_rep']:
        #     ### config_1 to config_n
        #     for config in form.keys():
        #         prop_check = pc.prop_check(form, config, stru_rep)
        #         rel_check = tc.rel_check(form, config, stru_rep, prop_check, rel_correct)
        # print(rel_check)

            #     if rel_check == True:
            #         rel_corrct += 1
            # print(rel_corrct)



            #     if rel_check == False:
            #         rel_corrct = 0
            #         break
            # if rel_corrct == 1:
            #     final_correct = 1
            #     break

        # if final_correct == 1:
        #     print('Prediction: True ','Label: ', base['label'] )
        # else:
        #     # print('False')
        #     print('Prediction: False ', 'Label: ', base['label'])




if __name__ == '__main__':
    src_data, img_data = data_pp.read_source_data('checked_data/check_temp.json', 'checked_data/check_image_feature.json')
    #src_data, img_data = data_pp.read_source_data('checked_data/tmp.json', 'checked_data/image_representation.json')
    #src_data, img_data = data_pp.read_source_data('checked_data/1_formal.json', 'checked_data/2_image.json')
    res = check(src_data, img_data)

