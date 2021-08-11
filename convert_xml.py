# Parse EMu XML to JSON
# 2021-Jun; FMNH
# based on:
#  https://docs.python.org/3/library/xml.etree.elementtree.html
#  https://stackoverflow.com/a/10231610 


import xml.etree.ElementTree as ET
from lxml import etree
from glob import glob
import json
import pandas as pd
from decouple import config
import sys, prep_input as pi


def xml_to_json(xml_input):

    # # # # # # # # # # # # # # # # # # 
    # Prep dictionaries for h2i field-types:

    # Read in EMu-h2i field mapping
    emu_map = pd.read_csv(config('MAP_PATH') + 'h2i_emu.csv', squeeze=True)

    # Read in EMu-h2i conditional mapping
    map_condition = pd.read_csv(config('MAP_PATH') + 'h2i_conditions.csv', squeeze=True, keep_default_na=False)

    # Non-conditional   # # #

    # Single/atomic 
    atomic = emu_map.query('repeatable != "yes"')
    h2i_atomic = atomic['h2i_field'].values
    emu_no_group = emu_map[emu_map['emu_group'].isnull()]['emu'].values
    atom_dict = dict.fromkeys(tuple(h2i_atomic))

    # Multi/repeatable 
    repeatable = emu_map.query('repeatable == "yes"')
    h2i_rep = repeatable['h2i_field'].values
    rep_dict = dict.fromkeys(tuple(h2i_rep), [])


    # Conditional       # # # 

    # Redacted fields
    h2i_null_fields = map_condition.query('h2i_field == "NULL"')['h2i_field'].values

    # Other conditions
    h2i_con_fields = map_condition['h2i_field'].values
    h2i_con_fields_2 = map_condition.query('h2i_field != "NULL"')['h2i_field'].values
    con_dict = dict.fromkeys(tuple(h2i_con_fields_2), [])


    # # # # # # # # # # #
    # Prep dictionaries

    # Single (Un-grouped) h2i fields
    # Try filtering/appending fields into groups at end. Otherwise, include in each field-type loop [slow?]
    h2i_single_emu = emu_map[emu_map['h2i_container'].isnull()]['h2i_field'].values
    h2i_single_map = map_condition[map_condition['h2i_container'].isnull()]['h2i_field'].values

    single_dict = dict()
    for single_emu in h2i_single_emu:
        single_dict[single_emu] = []

    for single_map in h2i_single_map:
        single_dict[single_map] = []


    # Grouped h2i fields
    # Try filtering/appending fields into groups at end. Otherwise, include in each field-type loop [slow?]
    h2i_groups = emu_map[emu_map['h2i_container'].notnull()]['h2i_container'].values
    # h2i_con_groups = map_condition['h2i_container'].values  # Safe to assume all container-values show in emu_map?
    # group_dict = dict.fromkeys(tuple(h2i_groups), {})

    for group_key in h2i_groups:
        h2i_group_emu = emu_map.query('h2i_container == @group_key')['h2i_field'].values
        h2i_group_maps = map_condition.query('h2i_container == @group_key')['h2i_field'].values
        # single_dict[group_key] = [dict.fromkeys(tuple(h2i_group_emu), "")]
        temp_group = dict()

        single_dict[group_key] = {}
        for group1_emu in h2i_group_emu:
            # single_dict[group_key][group1_emu] = ""
            temp_group[str(group1_emu)] = ""

        for group1_map in h2i_group_maps:
            temp_group[str(group1_map)] = ""
        
        single_dict[group_key] = [temp_group]

    #     print("single_dict keys: ")
    #     print(single_dict['identifiers'].keys)  # ['identifiers']))


    # # Full h2i dictionary
    full_dict = [{"data": single_dict}]
    # full_dict.update
    # print("full_dict:")
    # print("id1:  " + str(full_dict['data']['identifiers'][0]['cd:identifier']))
    # print("id1:  " + str(type(single_dict['identifiers'][0])))


    # # Output EMu-json
    # f = open(config('OUT_PATH') + 'json_TEST_FULL.json', 'w')
    # f.write(json.dumps(full_dict, indent=True))
    # f.close()


    # # # # # # # # # # # #
    # Prep input-XML  # # # 

    tree1_string = pi.xml_prep(xml_in = xml_input)

    # 1 - import as lxml ElementTree
    tree_prep = etree.XML(tree1_string)
    # root = tree_prep.getroot()

    # 2 - Find/Prep values with lxml.etree.xpath()

    get_cols = etree.XPath('.//*')
    # Turn EMu col-names into XML-tags instead of attributes:

    print("num_of_treePrepCols:  " + str(len(get_cols(tree_prep))))

    for column in get_cols(tree_prep): # .XPath('.//*'):

        if column.tag is not None:
            # print('col tag:  ' + str(column.tag))


            # # # # # # # # # # 
            
            # Clear redacted values

            for h2i_null_field1 in h2i_null_fields:
                    
                # tup_fields = tuple1.findall('.//*')  

                h2i_null_field = str(h2i_null_field1)

                emu_if_field = map_condition.query('h2i_field == @h2i_null_field')['if_field1'].values
                emu_if_value = map_condition.query('h2i_field == @h2i_null_field')['if_value1'].values
                emu_then_field = map_condition.query('h2i_field == @h2i_null_field')['then_field'].values
                h2i_con_value = map_condition.query('h2i_field == @h2i_null_field')['static_value'].values

                if str(column.tag) == str(emu_if_field)[2:-2]: # and column.text == str(emu_if_value): # "NULL":

                    emu_xpath_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/preceding-sibling::' + str(emu_then_field)[2:-2]
                    # print('xpath_str:  '  + str(emu_xpath_string))

                    emu_xpath = etree.XPath(emu_xpath_string)
                    # print("tup xslt:  " + './' + str(emu_then_field)[2:-2])

                    emu_then_update = emu_xpath(tree_prep) 
                    # print('emu_then result --- ' + str(emu_then_update))
                    
                    if emu_then_update != []:
                        # print('emu_then_up 1:  ' + str(emu_then_update[0].tag) + ' -- ' + str(emu_then_update[0].text) )
                        emu_then_update[0].text = ""
                        # print('emu_then_up 2:  ' + str(emu_then_update[0].tag) + ' -- ' + str(emu_then_update[0].text) )


                    # Also check for 'following-siblings'
                    emu_xpath2_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/following-sibling::' + str(emu_then_field)[2:-2]
                    # print('xpath_str:  '  + str(emu_xpath_string))
                    emu_xpath2 = etree.XPath(emu_xpath2_string)

                    # print("tup xslt:  " + './' + str(emu_then_field)[2:-2])
                    emu_then_update2 = emu_xpath2(tree_prep) 

                    if emu_then_update2 != []:
                        # print('emu_then_up 1:  ' + str(emu_then_update[0].tag) + ' -- ' + str(emu_then_update[0].text) )
                        emu_then_update2[0].text = ""
                        # print('emu_then_up 2:  ' + str(emu_then_update[0].tag) + ' -- ' + str(emu_then_update[0].text) )

                    
                    # if the emu_if-field should also be updated, update it too:
                    if str(column.text) == str(emu_if_value)[2:-2]:
                        column.text = ""

                    # TO DO
                    #  -- replace above with 'just remove the tuple'
                    #  -- check that it works on atomic fields [not just table]


    # Return updated xml as string
    prep_tree_string = etree.tostring(tree_prep).decode('utf-8')


    # 3 - convert back to xml ElementTree
    doc = ET.fromstring(prep_tree_string)  # ET.parse(prep_tree_string)   # 
    tree = ET.ElementTree(doc)

    # Setup separate empty dict of h2i terms


    all_records = [] # full_dict # []
    group_all = single_dict

    group_all_test = single_dict


    def recursive_items(dictionary):
        for key, value in dictionary.items():
            if type(value) is dict:
                yield (key, value)
                yield from recursive_items(value)
            else:
                yield (key, value)

    get_tuples = etree.XPath(".//data")
    tuples = get_tuples(tree_prep)
    # tuples = tree.findall(".//data")       


    for tuple1 in tuples:

        get_tup_fields = etree.XPath('.//*')
        tup_fields = get_tup_fields(tuple1) 
        # tup_fields = tuple1.findall('.//*') 

        for tup_field in tup_fields:
            # print(tup_field.tag)
            # if tup_field.tag == "tuple":
            #     print("tuple")
            #     for elems_temp in tup_fields.getiterator("child"):
            #         print("child:  " + str(etree.SubElement(elems_temp)))
            
            # 0 - get emu-xml-field's corresponding h2i field + info
            t_emu_field = emu_map.query('emu == @tup_field.tag')['emu'].values
            t_emu_group = emu_map.query('emu == @tup_field.tag')['emu_group'].values
            t_h2i_field = emu_map.query('emu == @tup_field.tag')['h2i_field'].values
            t_h2i_group = emu_map.query('emu == @tup_field.tag')['h2i_container'].values

            t_emu_if_field = map_condition.query('if_field1 == @tup_field.tag')['if_field1'].values
            t_emu_if_value = map_condition.query('if_field1 == @tup_field.tag')['if_value1'].values
            t_emu_then_field = map_condition.query('if_field1 == @tup_field.tag')['then_field'].values
            t_h2i_con_field = map_condition.query('if_field1 == @tup_field.tag')['h2i_field'].values
            t_h2i_con_value = map_condition.query('if_field1 == @tup_field.tag')['static_value'].values
            t_h2i_con_group = map_condition.query('if_field1 == @tup_field.tag')['h2i_container'].values

            # 1 - check if field is in emu_map & filter out groups
            # if tup_field.tag is not None and tup_field.tag in t_emu_field: # in emu_map['emu']:
            
            if tup_field.tag != "tuple" and tup_field.tag in emu_no_group: # in emu_map['emu']:

                print(str(tup_field.tag) + " -- " + str(t_emu_group) + ' -- ' + str(len(t_emu_group)))

                # print(str(t_h2i_field)[2:-2])
                # print(single_dict.keys())

                if str(t_h2i_field)[2:-2] in single_dict.keys():

                    group_all[str(t_h2i_field)[2:-2]] = tup_field.text
                    # print("group_all:")
                    # print(group_all)

                # 2 - if so, also check for map_condition
                # if "NOT NULL" in t_emu_if_value:
                # # if tup_field.text == t_emu_if_value[0] and tup_field.tag is not None:
                # # if tup_field.tag == t_emu_if_field:  # in map_condition['if_field1']:
                #     # if tup_field.text == t_emu_if_value[0]:
                    
                #     # Setup dict of conditional grouped values for values with no 'emu_group'
                #     if t_h2i_group is not None and len(single_dict[t_h2i_group[0]]) > 0:

                #         str_h2i_group = str(t_h2i_group[0])
                #         # print("group:  " + str_h2i_group)
                #         # print("len:  " + str(len(single_dict[t_h2i_group[0]])))
                #         # print(single_dict[t_h2i_group[0]])
                        
                #         group_temp_dict = single_dict[t_h2i_group[0]]
                #         # print(group_temp_dict)

                #         group_temp_dict.append(dict.fromkeys(tup_field.tag, tup_field.text))
                #         # print(group_temp_dict)

                #         group_fields = map_condition.query('h2i_container == @str_h2i_group')['h2i_field'].values
                #         group_values = map_condition.query('h2i_container == @str_h2i_group')['static_value'].values

                #         group_temp_dict.append(dict.fromkeys(group_fields, group_values))

                #         # group_temp_dict.append(zip(group_fields, group_values))
                        
                #         # for key, val in group_temp_dict: # t_h2i_con_field1 in t_h2i_con_field:
                            
                #             # str_h2i_con_field = str(t_h2i_con_field)[2:-2]
                #             # group_temp_dict[str_h2i_group][0][str_h2i_field] = t_h2i_


                #         group_all[str_h2i_group].append(group_temp_dict)  # = t_h2i_con_value

                # 3 - if h2i_field in recursive_items(group_all) [or group_all.key], add value group_all @ key = 

                # if tup_field.tag in recursive_items(group_all)
            

                # for h2i in recursive_items(group_all):


        all_records.append(group_all.copy())

        
    # # Convert fixed EMu-XML to JSON
    # treestring = ET.tostring(root, encoding='utf-8', method='xml')
    # emu_json_out = xmltodict.parse(treestring)
    # # emu_json_out = xmltodict.parse(ET.canonicalize(treestring))


    # Output EMu-json
    f = open(config('OUT_PATH') + 'emu_to_json.json', 'w')
    f.write(json.dumps(all_records, indent=True))
    f.close()


    ######
    # Optional section below to also:
    # Output fixed EMu-XML
    
    # if fix_xml == True:

        # # ET.canonicalize throws errors; skip for now [2021-jul-30]
        # # Output 'canonic' xml -- e.g. <tag></tag>
        # with open(config('OUT_PATH') + "emu_canonic.xml", mode='w', encoding='utf-8') as out_file:
        #     ET.canonicalize(xml_data=treestring, out=out_file)
        
        # Also output slightly-more-compact xml -- e.g. <tag />
    tree.write(config('OUT_PATH') + "emu_xml.xml")
    


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_to_json(arg)