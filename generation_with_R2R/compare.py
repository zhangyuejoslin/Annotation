import json

with open("generation_data/automatic_generation.json") as f_automatic:
    automatic = json.load(f_automatic)

with open('generation_data/ground_truth.json') as f_ground_truth:
    ground_truth = json.load(f_ground_truth)

identity = 1
for each_automatic, each_ground_truth in zip(automatic, ground_truth):
  # if identity == 1:
    each_automatic_list = []
    each_ground_truth_list = []
    for e_a in each_automatic['Config']:
        each_automatic_list.append(e_a['type'])
       # each_automatic_list.append((e_a['type'], e_a['distance'], e_a['spatial_entity']['SPL']))
    for e_g in each_ground_truth['config']:
        if "Motion" in e_g['type']:
            each_ground_truth_list.append(e_g['type'])
            #if "SPL" in e_g['spatial_entity']:
               # each_ground_truth_list.append(e_g['type'])
                #each_ground_truth_list.append((e_g['type'], e_g['distance'], e_g["spatial_entity"]['SPL']['text']))
           #else:

                #each_ground_truth_list.append((e_g['type'], e_g['distance'], None))
    print(each_automatic_list)
    print(each_ground_truth_list)
    if each_automatic_list == each_ground_truth_list:
        print('True')
    else:
        print('False')
    print('$$$$$$$')
  # identity += 1



  # identity += 1
  #       verify_spm = 0
  #       verify_spi = 0
  #       verify_spl = 0
  #       for e_g_t in each_ground_truth['config']:
  #           if "SPM" in e_a['spatial_entity'] and "SPM" in e_g_t['spatial_entity'] and e_a ['spatial_entity']['SPM'] == e_g_t['spatial_entity']["SPM"]['text'].lower():
  #               verify_spm = 1
  #           if "SPI" in e_a['spatial_entity'] and 'SPI' in e_g_t['spatial_entity'] and e_a ['spatial_entity']['SPI'] == e_g_t['spatial_entity']['SPI']['text'].lower():
  #               verify_spi = 1
  #           if "SPL" in e_a['spatial_entity'] and 'SPL' in e_g_t['spatial_entity'] and e_a ['spatial_entity']['SPL'] == e_g_t['spatial_entity']['SPL']['text'].lower():
  #               verify_spl = 1
  #       if verify_spm ==1 and verify_spi == 1 and verify_spl == 1:
  #           print('True')
  #       else:
  #           print(e_a)
  # identity +=1

