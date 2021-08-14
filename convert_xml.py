# Parse EMu XML to JSON
# 2021-Aug; FMNH

import xml.etree.ElementTree as ET
from lxml import etree
from glob import glob
import json
import pandas as pd
from decouple import config
import sys, prep_input as pi


def xml_to_json(xml_input):

    # # # # # # # # # # # # # # # # # # #
    # Import mappings for h2i field-types:
    emu_map = pd.read_csv(config('MAP_PATH') + 'h2i_emu.csv', squeeze=True)
    map_condition = pd.read_csv(config('MAP_PATH') + 'h2i_conditions.csv', squeeze=True, keep_default_na=False)

    # Single/atomic 
    emu_no_group = emu_map[emu_map['emu_group'].isnull()]['emu'].values
    emu_h2i_groups = emu_map[emu_map['h2i_container'].notnull()]['h2i_container'].values

    # Redacted fields
    h2i_null_fields = map_condition.query('h2i_field == "NULL"')['h2i_field'].values


    # # # # # # # # # # # #
    # Prep input-XML  # # # 

    # Turn EMu col-names into XML-tags:
    tree1_string = pi.xml_prep(xml_in = xml_input)
    tree_prep = etree.XML(tree1_string)
    get_cols = etree.XPath('.//*')


    for column in get_cols(tree_prep):

        if column.tag is not None:


            # # # # # # # # # # # #
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

        for tup_field in tup_fields:

            # Get emu-xml-field's corresponding h2i field + info
            t_emu_field = emu_map.query('emu == @tup_field.tag')['emu'].values
            t_emu_group = emu_map.query('emu == @tup_field.tag')['emu_group'].values
            t_h2i_field = emu_map.query('emu == @tup_field.tag')['h2i_field'].values
            t_h2i_group = emu_map.query('emu == @tup_field.tag')['h2i_container'].values

            t_emu_if_value = map_condition.query('if_field1 == @tup_field.tag')['if_value1'].values
            t_h2i_con_field = map_condition.query('if_field1 == @tup_field.tag')['h2i_field'].values
            t_h2i_con_value = map_condition.query('if_field1 == @tup_field.tag')['static_value'].values
            t_h2i_con_group = map_condition.query('if_field1 == @tup_field.tag')['h2i_container'].values

            get_tuples = etree.XPath("./" + str(tup_field.tag) + "//*")
            tuple_group = get_tuples(tuple1)

            
            # # # # # # # # # # # # # # # # 
            # EMu SINGLE fields  (where tup_field.tag is a value in emu_map['emu'])
            if tup_field.tag in emu_no_group: # and tup_field.tag != "tuple":


                # # # # # # #
                # 1-to-1 -- withOUT conditional mapping
                if str(t_h2i_field)[2:-2] in single_dict.keys():

                    group_all[str(t_h2i_field[0])] = tup_field.text


                # # # # # # #
                # 1-to-Group -- WITH conditional mapping [all currently to multi-value h2i field]
                elif "NOT NULL" in t_emu_if_value and t_h2i_group is not None:

                    str_h2i_con_group = str(t_h2i_con_group[0])
                    str_h2i_group = str(t_h2i_group[0])
                    group_temp_dict = {}

                    group_temp_dict[str(t_h2i_field)[2:-2]] = str(tup_field.text)

                    for key, val in zip(t_h2i_con_field, t_h2i_con_value):
                        group_temp_dict[str(key)] = str(val)

                    group_all[str_h2i_con_group].append(group_temp_dict.copy())

                    group_temp_dict.clear()


            # # # # # # #
            # EMu REF & TABLE fields  (where tup_field.tag is actually a value in emu_map['emu_group'])
            elif tup_field.tag in emu_map['emu_group'].values and tup_field.tag is not None:

                t_emu_field = emu_map.query('emu_group == @tup_field.tag')['emu'].values
                m_emu_group = emu_map.query('emu_group == @tup_field.tag')['emu_group'].values
                t_h2i_field = emu_map.query('emu_group == @tup_field.tag')['h2i_field'].values
                t_h2i_group = emu_map.query('emu_group == @tup_field.tag')['h2i_container'].values

                # str_emu_group = str(m_emu_group)

                check_tuples = etree.XPath("./tuple")
                has_tuples = check_tuples(tup_field)

                # # # # # # # # # # # # #
                # TUPLES - handle these first 
                # [separately from Ref or Table fields withOUT tuples/grouped EMu-fields]
                if len(has_tuples) > 0:

                    for tuple1_1 in has_tuples:

                        get_sub_tuples = etree.XPath(".//*")
                        tuple_group = [get_sub_tuples(tuple1_1)]

                        for tup_group_field in tuple_group:
                            # TO DO -- include a check for map_conditions here; currently none needed?
                                
                            if tup_field.tag in m_emu_group:

                                e_h2i_field = emu_map.query('emu_group == @tup_field.tag')['h2i_field'].values
                                e_h2i_group = emu_map.query('emu_group == @tup_field.tag')['h2i_container'].values

                                group_temp_dict = dict.fromkeys(e_h2i_field)

                                if len(e_h2i_group) > 0:
                                    str_h2i_group = str(e_h2i_group[0])
                                if len(e_h2i_con_group) > 0:
                                    str_h2i_con_group = str(e_h2i_con_group[0])

                                for sib_key in tup_group_field:
                                    if sib_key.text != "" and sib_key.text is not None:
                                        sib_key_str = str(emu_map.query('emu == @sib_key.tag')['h2i_field'].values)[2:-2]
                                        group_temp_dict[sib_key_str] = str(sib_key.text)
                                
                                if str_h2i_group in emu_h2i_groups:

                                    group_all[str_h2i_group].append(group_temp_dict.copy())
                                
                                elif len(tup_group_field) == 1:

                                    group_all[str(e_h2i_field)[2:-2]] = tup_group_field[0].text


                # if NOT a tuple:
                else:
                    for group_field in tuple_group:
                            
                        if group_field.tag in t_emu_field:

                            e_h2i_field = emu_map.query('emu == @group_field.tag')['h2i_field'].values
                            e_h2i_group = emu_map.query('emu == @group_field.tag')['h2i_container'].values

                            e_emu_if_field = map_condition.query('if_field1 == @group_field.tag')['if_field1'].values
                            e_emu_if_value = map_condition.query('if_field1 == @group_field.tag')['if_value1'].values
                            e_emu_then_field = map_condition.query('if_field1 == @group_field.tag')['then_field'].values
                            e_h2i_con_field = map_condition.query('if_field1 == @group_field.tag')['h2i_field'].values
                            e_h2i_con_value = map_condition.query('if_field1 == @group_field.tag')['static_value'].values
                            e_h2i_con_group = map_condition.query('if_field1 == @group_field.tag')['h2i_container'].values

                            group_temp_dict = {}

                            if len(e_h2i_group) > 0:
                                str_h2i_group = str(e_h2i_group[0])
                            if len(e_h2i_con_group) > 0:
                                str_h2i_con_group = str(e_h2i_con_group[0])


                            # # # # # # # -- e.g. ColCollectionEventRef.ColSiteRef.PolPD1 --> dwc:country
                            # ref/table-to-1 -- withOUT conditional mapping
                            if group_field.tag not in e_emu_if_field: # and group_field.tag in single_dict.keys()

                                if e_h2i_group not in emu_h2i_groups:

                                    group_all[str(e_h2i_field)[2:-2]] = group_field.text  # # # # use += instead?                             

                            # # # # # # #  -- e.g. PriAccessionNumberRef.AccAccessionNo --> cd:identifier + cd:identifierType --> 'accession number'
                            # ref/table-to-1 -- WITH conditional mapping [all currently to multi-value h2i field]
                            # Conditions besides 'not null' + h2i-container would currently need separate 'elif' statements
                            elif e_emu_if_value == "NOT NULL":  # and str_h2i_con_group is not None:

                                group_temp_dict[str(e_h2i_field)[2:-2]] = str(group_field.text)

                                for key, val in zip(e_h2i_con_field, e_h2i_con_value):
                                    group_temp_dict[str(key)] = str(val)

                                group_all[str_h2i_con_group].append(group_temp_dict.copy())

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

    # # ET.canonicalize throws errors; skip for now [2021-jul-30]
    # # Output 'canonic' xml -- e.g. <tag></tag>
    with open(config('OUT_PATH') + "emu_raw_canonic.xml", mode='w', encoding='utf-8') as out_file:
        ET.canonicalize(xml_data=tree1_string, out=out_file)
        
    # Output slightly-more-compact xml -- e.g. <tag />
    tree.write(config('OUT_PATH') + "emu_prepped.xml")    


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_to_json(arg)