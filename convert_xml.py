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
from io import BytesIO


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
    emu_h2i_groups = emu_map[emu_map['h2i_container'].notnull()]['h2i_container'].values
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



    # # # # # # # # # # # #
    # Prep input-XML  # # # 

    # Turn EMu col-names into XML-tags instead of attributes named 'name':
    tree1_string = pi.xml_prep(xml_in = xml_input)

    # 1 - import as lxml ElementTree
    tree_prep = etree.XML(tree1_string)

    # 2 - Find/Prep values
    get_cols = etree.XPath('.//*')

    for column in get_cols(tree_prep):

        if column.tag is not None:

            # # # # # # # # # # 
            
            # Clear redacted values

            for h2i_null_field1 in h2i_null_fields:

                h2i_null_field = str(h2i_null_field1)

                emu_if_field = map_condition.query('h2i_field == @h2i_null_field')['if_field1'].values
                emu_if_value = map_condition.query('h2i_field == @h2i_null_field')['if_value1'].values
                emu_then_field = map_condition.query('h2i_field == @h2i_null_field')['then_field'].values
                h2i_con_value = map_condition.query('h2i_field == @h2i_null_field')['static_value'].values

                if str(column.tag) == str(emu_if_field)[2:-2]: # and column.text == str(emu_if_value): # "NULL":

                    emu_xpath_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/preceding-sibling::' + str(emu_then_field)[2:-2]
                    emu_xpath = etree.XPath(emu_xpath_string)
                    emu_then_update = emu_xpath(tree_prep) 
                                        
                    if emu_then_update != []:

                        emu_then_update[0].text = ""


                    # Also check for 'following-siblings'
                    emu_xpath2_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/following-sibling::' + str(emu_then_field)[2:-2]
                    emu_xpath2 = etree.XPath(emu_xpath2_string)
                    emu_then_update2 = emu_xpath2(tree_prep) 

                    if emu_then_update2 != []:

                        emu_then_update2[0].text = ""
                    
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
    
    # # check input-xml again
    # tree.write(config('OUT_PATH') + "check_input_prep.xml")

    # Setup separate empty dict of h2i terms
    all_records = []

    get_tuples = etree.XPath(".//data")
    tuples = get_tuples(tree_prep)


    # # # # # # #
    for tuple1 in tuples:

        # # # # # # # # # # #
        # Prep dictionaries

        # Single (Un-grouped) h2i fields
        # Try filtering/appending fields into groups at end. Otherwise, include in each field-type loop [slow?]
        # TO DO: differentiate between data-types for repeatable [] and non-repeatable "" in schema; currently all repeatable []
        h2i_single_emu = emu_map[emu_map['h2i_container'].isnull()]['h2i_field'].values
        h2i_single_map = map_condition[map_condition['h2i_container'].isnull()]['h2i_field'].values

        single_dict = dict()
        for single_emu in h2i_single_emu:
            single_dict[single_emu] = []

        for single_map in h2i_single_map:
            single_dict[single_map] = []

        # Grouped h2i fields
        h2i_groups = emu_map[emu_map['h2i_container'].notnull()]['h2i_container'].values
        # h2i_con_groups = map_condition['h2i_container'].values  # Safe to assume all container-values show in emu_map?

        for group_key in h2i_groups:
            h2i_group_emu = emu_map.query('h2i_container == @group_key')['h2i_field'].values
            h2i_group_maps = map_condition.query('h2i_container == @group_key')['h2i_field'].values
            temp_group = dict()

            single_dict[group_key] = {}
            for group1_emu in h2i_group_emu:
                temp_group[str(group1_emu)] = None

            for group1_map in h2i_group_maps:
                temp_group[str(group1_map)] = None
            
            single_dict[group_key] = [temp_group]


        group_all = single_dict

        get_tup_fields = etree.XPath('.//*')
        tup_fields = get_tup_fields(tuple1) 

        # elif # field's parent != tuple:
        for tup_field in tup_fields:

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

            get_tuples = etree.XPath("./" + str(tup_field.tag) + "//*")
            tuple_group = get_tuples(tuple1)

            # # This might need to move to separate if/for loop
            # if "tuple" in tuple_group:
            #     get_sub_tuples = etree.XPath("./" + str(tuple_group) + "//*")
            #     tuple_group = [get_sub_tuples(tup_field)]

            # 1 - check if field is in emu_map & filter out emu_groups
            # if tup_field.tag is not None and tup_field.tag in t_emu_field: # in emu_map['emu']:

            
            # # # # # # # # # # # # # # # # 
            # add 1-to-1 emu-to-h2i fields (where tup_field.tag is a value in emu_map['emu'])
            if tup_field.tag in emu_no_group: # and tup_field.tag != "tuple":


                # # # # # # #
                # 1-to-1 -- withOUT conditional mapping
                if str(t_h2i_field)[2:-2] in single_dict.keys():

                    group_all[str(t_h2i_field[0])] = tup_field.text


                # # # # # # #
                # 1-to-Group -- WITH conditional mapping [all currently to multi-value h2i field]
                elif "NOT NULL" in t_emu_if_value and t_h2i_group is not None:
                        
                    # Setup dict of conditional grouped values for values with no 'emu_group'
                    str_h2i_con_group = str(t_h2i_con_group[0])
                    str_h2i_group = str(t_h2i_group[0])
                    group_temp_dict = {}

                    group_temp_dict[str(t_h2i_field)[2:-2]] = str(tup_field.text)

                    for key, val in zip(t_h2i_con_field, t_h2i_con_value):
                        group_temp_dict[str(key)] = str(val)

                    group_all[str_h2i_con_group].append(group_temp_dict.copy())

                    # This might need to wait until after REF/TABLE steps below / At end of a record
                    group_temp_dict.clear()


            # # # # # # #
            # EMu REF & TABLE fields (where tup_field.tag is actually a value in emu_map['emu_group'])
            elif tup_field.tag in emu_map['emu_group'].values and tup_field.tag is not None:

                t_emu_field = emu_map.query('emu_group == @tup_field.tag')['emu'].values
                m_emu_group = emu_map.query('emu_group == @tup_field.tag')['emu_group'].values
                t_h2i_field = emu_map.query('emu_group == @tup_field.tag')['h2i_field'].values
                t_h2i_group = emu_map.query('emu_group == @tup_field.tag')['h2i_container'].values

                str_emu_group = str(m_emu_group)

                # get_tuples = etree.XPath("./" + str(tup_field.tag) + "//*")
                # tuple_group = get_tuples(tuple1)

                check_tuples = etree.XPath("./tuple")
                has_tuples = check_tuples(tup_field)

                print("HAS TUPLES? - - - - " + str(len(has_tuples)))
                print(has_tuples)

                # # # # # # # # # # # # #
                # Handle tuples first/separately from other ref or table fields
                # (Need to iterate thru tuples, vs through non-tuple fields)
                if len(has_tuples) > 0:
                # if "tuple" in tuple_group:
                    for tuple1_1 in has_tuples:

                        print(tuple1_1)

                        get_sub_tuples = etree.XPath(".//*")
                        tuple_group = [get_sub_tuples(tuple1_1)]

                        # print("TUPLE GROUP: --- --- -- length == ==  " + str(len(tuple_group)))
                        # print(tuple_group)

                        # For EMu-nodes nested inside 'tuple' nodes:
                        # iterate through fields within an emu-group (is iterparse better?)

                        # get_tuples = etree.XPath("./*/tuple//*")
                        # # get_tuples = etree.XPath("./" + str(tup_field.tag) + "//*")
                        # tuple_group = get_tuples(tuple1)

                        print("TUPLE GROUP - - - ")
                        print(tuple_group)
                        print("TUP GROUP FIELD [out of loop]:  " + str(tuple_group[0]))

                        # For EMu-nodes nested inside 'tuple' nodes:
                        # iterate through fields within an emu-group (is iterparse better?)
                        # if len(tuple_group) > 1 or "tuple" in tuple_group:
                        # for tuple in tup_field:
                        for tup_group_field in tuple_group:
                            # TO DO -- include a check for map_conditions here; currently none needed?

                            print("TUP PARENT")
                            print(tup_field.tag)
                            print(emu_map['emu_group'].values)

                            print("TUP GROUP FIELD --- - - - " + str(tup_group_field))
                                
                            if tup_field.tag in m_emu_group: # emu_map['emu_group'].values:
                            #if tup_group_field.tag in t_emu_field:  # not in ["tuple", None]:  # != "tuple": and tup_group_field.text != "":
                                print ("FIRST tuple_group:  " + str(tuple_group))
                                print("TUP GROUP FIELD --- - - - " + str(tup_group_field))

                                e_h2i_field = emu_map.query('emu_group == @tup_field.tag')['h2i_field'].values
                                e_h2i_group = emu_map.query('emu_group == @tup_field.tag')['h2i_container'].values

                                group_temp_dict = dict.fromkeys(e_h2i_field) # {}
                                print("---- - --- --- CHECK KEYS in group_temp_dict below:")
                                print(group_temp_dict)

                                if len(e_h2i_group) > 0:
                                    str_h2i_group = str(e_h2i_group[0])
                                if len(e_h2i_con_group) > 0:
                                    str_h2i_con_group = str(e_h2i_con_group[0])
                                
                                
                                print("BEFORE -- GROUP TEMP DICT: : : : : : : : : ")
                                print(group_temp_dict)

                                sib_e_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['emu'].values
                                sib_h_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['h2i_field'].values

                                # e_emu_if_field = map_condition.query('if_field1 == @tup_group_field.tag')['if_field1'].values
                                # e_emu_if_value = map_condition.query('if_field1 == @tup_group_field.tag')['if_value1'].values
                                # e_emu_then_field = map_condition.query('if_field1 == @tup_group_field.tag')['then_field'].values
                                # e_h2i_con_field = map_condition.query('if_field1 == @tup_group_field.tag')['h2i_field'].values
                                # e_h2i_con_value = map_condition.query('if_field1 == @tup_group_field.tag')['static_value'].values
                                # e_h2i_con_group = map_condition.query('if_field1 == @tup_group_field.tag')['h2i_container'].values

                                # for tup_field1 in tup_group_field:
                                #     print("TUP FIELD:  - - - - " + tup_field1.tag + " === " + tup_field1.text)
                                #     tup_keys = {}
                                #     str_tup_field1 = [str(tup_field1.tag)]
                                #     tup_keys += str_tup_field1                                

                                # tup_temp = dict.fromkeys(tup_keys) # tup_vals = {}
                                # tup_temp = {}
                                # print(tup_temp)

                                # for tup_val in tup_group_field:
                                # # tup_keys = {}
                                #     print("TUP VALUE: - - - - == " + str(tup_value1.text))
                                #     if tup_value1.text is not None: 
                                #         # tup_vals = str(tup_field1.text)
                                #         # tup_keys = str(emu_map.query('emu == @tup_field1.tag')['h2i_field'].values)[2:-2]
                                #         tup_temp[tup_keys] = str(tup_field1.text)

                                for sib_key in tup_group_field:
                                    print("TUP VALUE: - - - - == " + str(sib_key.text))
                                    print(sib_key.text)
                                    if sib_key.text != "":
                                        # sib_vals = []
                                        # sib_vals.append(str(sib_key.text))
                                        # sib_keys = []
                                        # sib_keys.append(str(emu_map.query('emu == @sib_key.tag')['h2i_field'].values)[2:-2])
                                        sib_key_str = str(emu_map.query('emu == @sib_key.tag')['h2i_field'].values)[2:-2]
                                        group_temp_dict[sib_key_str] = str(sib_key.text)
                                        # group_temp_dict.update({sib_key_str = str(sib_key.text)}
                                
                                print("SEE APPENDED group_temp_dict (prior to group_all appending below:")

                                print(group_temp_dict)

                                # for key, val in zip(sib_keys, sib_vals): # zip(e_h2i_field, e_h2i_con_value):
                                #     group_temp_dict[key] = val

                                print("GROUP is..........")
                                print(str_h2i_group)
                                print("tup_group_field is " + str(len(tup_group_field)) + " -- -- -- -- ")
                                print(tup_group_field)

                                if str_h2i_group in emu_h2i_groups:

                                    # group_all[str_h2i_group].append(group_temp_dict.copy())  # = t_h2i_con_value
                                    group_all[str_h2i_group].append(group_temp_dict.copy())
                                
                                elif len(tup_group_field) == 1:

                                    print("Single Field: - : - : - :")

                                    # group_all[sib_keys[0]] = sib_vals[0]
                                    # group_all[tup_group_field[0].tag] = tup_group_field[0].text
                                    group_all[str(e_h2i_field)[2:-2]] = tup_group_field[0].text

                                    print(group_all[str(e_h2i_field)[2:-2]])
                                    # group_temp_dict[str(e_h2i_field)[2:-2]] = str(tup_group_field.text)


                                # # # # # # # - # e.g. DesUseClassification_tab.DesUseClassification --> h2i:culturalArtefactFunction
                                # # ref/table-to-1 -- withOUT conditional mapping
                                # if tup_group_field.tag not in e_emu_if_field: # and tup_group_field.tag in single_dict.keys()

                                #     # print("H2I CONTAINER + len =  " + str(len(e_h2i_group))  +  " == === == ")
                                #     # print(emu_h2i_groups)
                                #     # print(e_h2i_group not in emu_h2i_groups)
                                #     # print(tuple_group)

                                #     if e_h2i_group not in emu_h2i_groups:

                                #         group_all[str(e_h2i_field)[2:-2]] = tup_group_field.text  # # # # use += instead?

                                #     # # # # # # # - # e.g. DesUseClassification_tab.DesUseClassification --> h2i:culturalArtefactFunction
                                #     # ref/table-to-Group -- withOUT conditional mapping
                                        
                                #     elif tup_group_field.text != "":  #  if "tuple" in tuple_group.tag == "tuple"  # if e_h2i_group in emu_h2i_groups:

                                #         # print("tup_group_field stuff --- " + str(tup_group_field.tag) + " (" + str(tup_group_field.text + ")"))

                                #         group_temp_dict[str(e_h2i_field)[2:-2]] = str(tup_group_field.text)

                                        # print("BEFORE -- GROUP TEMP DICT: : : : : : : : : ")
                                        # print(group_temp_dict)

                                        # sib_e_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['emu'].values
                                        # sib_h_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['h2i_field'].values

                                        # # for sib_field in sib_fields:
                                        # sib_val_xslt = etree.XPath("//" + tup_group_field.tag + '[.="' + tup_group_field.text + '"]/../*')
                                        # sib_val = sib_val_xslt(tup_field)

                                        # print(len(sib_val))

                                        # # Line up EMu-tuple-siblings with h2i-group-fields

                                        # for sib_key in sib_val:
                                        #     print(sib_key.text)
                                        #     sib_vals = []
                                        #     sib_vals.append(str(sib_key.text))
                                        #     sib_keys = []
                                        #     sib_keys.append(str(emu_map.query('emu == @sib_key.tag')['h2i_field'].values)[2:-2])

                                        # print(sib_vals)
                                        # print(sib_keys)

                                        # for key, val in zip(sib_keys, sib_vals): # zip(e_h2i_field, e_h2i_con_value):
                                        #     group_temp_dict[key] = val

                                        # print("AFTER -- GROUP TEMP DICT : : : : : : : : : ")

                                        # print(group_temp_dict)

                                        # group_all[str_h2i_group].append(group_temp_dict.copy())  # = t_h2i_con_value




                # if len(tuple_group) > 1 or "tuple" in tuple_group:
                else:
                    for tup_group_field in tuple_group:
                            
                        if tup_group_field.tag in t_emu_field:  # not in ["tuple", None]:  # != "tuple": and tup_group_field.text != "":

                            e_h2i_field = emu_map.query('emu == @tup_group_field.tag')['h2i_field'].values
                            e_h2i_group = emu_map.query('emu == @tup_group_field.tag')['h2i_container'].values

                            e_emu_if_field = map_condition.query('if_field1 == @tup_group_field.tag')['if_field1'].values
                            e_emu_if_value = map_condition.query('if_field1 == @tup_group_field.tag')['if_value1'].values
                            e_emu_then_field = map_condition.query('if_field1 == @tup_group_field.tag')['then_field'].values
                            e_h2i_con_field = map_condition.query('if_field1 == @tup_group_field.tag')['h2i_field'].values
                            e_h2i_con_value = map_condition.query('if_field1 == @tup_group_field.tag')['static_value'].values
                            e_h2i_con_group = map_condition.query('if_field1 == @tup_group_field.tag')['h2i_container'].values

                            group_temp_dict = {}

                            if len(e_h2i_group) > 0:
                                str_h2i_group = str(e_h2i_group[0])
                            if len(e_h2i_con_group) > 0:
                                str_h2i_con_group = str(e_h2i_con_group[0])


                            # # # # # # # - # e.g. DesUseClassification_tab.DesUseClassification --> h2i:culturalArtefactFunction
                            # ref/table-to-1 -- withOUT conditional mapping
                            if tup_group_field.tag not in e_emu_if_field: # and tup_group_field.tag in single_dict.keys()

                                # print("H2I CONTAINER + len =  " + str(len(e_h2i_group))  +  " == === == ")
                                # print(emu_h2i_groups)
                                # print(e_h2i_group not in emu_h2i_groups)
                                # print(tuple_group)

                                if e_h2i_group not in emu_h2i_groups:

                                    group_all[str(e_h2i_field)[2:-2]] = tup_group_field.text  # # # # use += instead?

                                # # # # # # # - # e.g. DesUseClassification_tab.DesUseClassification --> h2i:culturalArtefactFunction
                                # ref/table-to-Group -- withOUT conditional mapping
                                    
                                elif tup_group_field.text != "":  #  if "tuple" in tuple_group.tag == "tuple"  # if e_h2i_group in emu_h2i_groups:

                                    # print("tup_group_field stuff --- " + str(tup_group_field.tag) + " (" + str(tup_group_field.text + ")"))

                                    group_temp_dict[str(e_h2i_field)[2:-2]] = str(tup_group_field.text)

                                    sib_e_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['emu'].values
                                    sib_h_fields = emu_map.query('h2i_container == @e_h2i_group[0]')['h2i_field'].values

                                    # for sib_field in sib_fields:
                                    sib_val_xslt = etree.XPath("//" + tup_group_field.tag + '[.="' + tup_group_field.text + '"]/../*')
                                    sib_val = sib_val_xslt(tup_field)

                                    # Line up EMu-tuple-siblings with h2i-group-fields

                                    print("THIS MIGHT BE PROBLEMS")

                                    for sib_key in sib_val:
                                        print(sib_key.text)
                                        sib_vals = []
                                        sib_vals.append(str(sib_key.text))
                                        sib_keys = []
                                        sib_keys.append(str(emu_map.query('emu == @sib_key.tag')['h2i_field'].values)[2:-2])

                                    # print(sib_vals)
                                    # print(sib_keys)

                                    for key, val in zip(sib_keys, sib_vals): # zip(e_h2i_field, e_h2i_con_value):
                                        group_temp_dict[key] = val

                                    # print(group_temp_dict)

                                    group_all[str_h2i_group].append(group_temp_dict.copy())  # = t_h2i_con_value

                            # # # # # # #  -  # e.g. PriAccessionNumberRef.AccAccessionNo --> cd:identifier + cd:identifierType --> 'accession number'
                            # ref/table-to-1 -- WITH conditional mapping [all currently to multi-value h2i field]
                            # Conditions besides 'not null' + h2i-container would currently need separate 'elif' statements
                            elif e_emu_if_value == "NOT NULL":  # and str_h2i_con_group is not None:

                                group_temp_dict[str(e_h2i_field)[2:-2]] = str(tup_group_field.text)

                                for key, val in zip(e_h2i_con_field, e_h2i_con_value): # t_h2i_con_field1 in t_h2i_con_field:
                                    group_temp_dict[str(key)] = str(val)

                                group_all[str_h2i_con_group].append(group_temp_dict.copy())  # = t_h2i_con_value
                            
                            group_temp_dict.clear()


        all_records.append(group_all.copy())

        group_all.clear()

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
        
    # Output slightly-more-compact xml -- e.g. <tag />
    tree.write(config('OUT_PATH') + "emu_xml.xml")
    


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_to_json(arg)