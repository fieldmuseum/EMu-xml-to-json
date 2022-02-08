# Parse EMu XML to JSON
# 2021-Aug; FMNH

import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from glob import glob
from decouple import config
import json, sys
import prep_input as pi, prep_output as po
import redact_input as ri

def get_group_tuple(tup_field, tup_group_field, emu_map, map_condition, group_all):
    
    emu_json_groups = emu_map[emu_map['json_container'].notnull()]['json_container'].values

    t_emu_field = emu_map.query('emu_group == @tup_field.tag')['emu'].values
    m_emu_group = emu_map.query('emu_group == @tup_field.tag')['emu_group'].values
    # t_json_field = emu_map.query('emu_group == @tup_field.tag')['json_field'].values
    # t_json_group = emu_map.query('emu_group == @tup_field.tag')['json_container'].values

    # TO DO -- include a check for map_conditions here; currently none needed?
    t_g_json_field = emu_map.query('emu_group == @tup_field.tag')['json_field'].values

    t_emu_if_field = map_condition.query('if_field1 == @tup_field.tag')['if_field1'].values
    t_emu_if_value = map_condition.query('if_field1 == @tup_field.tag')['if_value1'].values
    # t_emu_then_field = map_condition.query('if_field1 == @tup_field.tag')['then_field'].values
    # t_json_con_field = map_condition.query('if_field1 == @tup_field.tag')['json_field'].values
    # t_json_con_value = map_condition.query('if_field1 == @tup_field.tag')['static_value'].values
    t_json_con_group = map_condition.query('if_field1 == @tup_field.tag')['json_container'].values

    group_temp_dict = {}


    if len(t_json_con_group) > 0:
        
        str_t_json_con_group = str(t_json_con_group[0])
    
    else:

        str_t_json_con_group = str(t_json_con_group)


    if tup_field.tag in m_emu_group:

        e_json_field = emu_map.query('emu_group == @tup_field.tag')['json_field'].values
        e_json_group = emu_map.query('emu_group == @tup_field.tag')['json_container'].values
        e_t_json_con_group = map_condition.query('if_field1 == @tup_field.tag')['json_container'].values

        group_temp_dict = dict.fromkeys(e_json_field)

        if len(e_json_group) > 0:
            str_json_group = str(e_json_group[0])
        # if len(e_json_con_group) > 0:
        #     str_json_con_group = str(e_json_con_group[0])

        for sib_key in tup_group_field:

            # Check for map-conditions:
            if sib_key.tag in t_emu_if_field and sib_key.text in t_emu_if_value: 

                group_temp_dict[str(t_g_json_field)[2:-2]] = str(sib_key.text)



            elif sib_key.text not in ["",[], None]:
                sib_key_str = str(emu_map.query('emu == @sib_key.tag')['json_field'].values)[2:-2]
                if sib_key.tag in t_emu_field:
                    group_temp_dict[sib_key_str] = str(sib_key.text)
                # else:
                #     group_temp_dict[sib_key_str] = None

        if len(t_json_con_group) > 0:
            # e_json_con_group = map_condition.query('if_field1 == @group_field.tag')['json_container'].values
            str_t_json_con_group = str(e_t_json_con_group[0])


        if str_json_group in str_t_json_con_group:

            group_all[str_t_json_con_group].append(group_temp_dict.copy())

            # return group_all

        elif str_json_group in emu_json_groups:

            group_all[str_json_group].append(group_temp_dict.copy())

            # return group_all
        
        elif len(tup_group_field) == 1:

            group_all[str(e_json_field)[2:-2]] = tup_group_field[0].text
        
    group_temp_dict.clear()

    return group_all


def get_group_nontuple(tuple_group, tup_field, emu_map, map_condition, group_all):

    emu_json_groups = emu_map[emu_map['json_container'].notnull()]['json_container'].values
    t_emu_field = emu_map.query('emu_group == @tup_field.tag')['emu'].values

    for group_field in tuple_group:
            
        if group_field.tag in t_emu_field:

            e_json_field = emu_map.query('emu == @group_field.tag')['json_field'].values
            e_json_group = emu_map.query('emu == @group_field.tag')['json_container'].values

            e_emu_if_field = map_condition.query('if_field1 == @group_field.tag')['if_field1'].values
            e_emu_if_value = map_condition.query('if_field1 == @group_field.tag')['if_value1'].values
            e_emu_then_field = map_condition.query('if_field1 == @group_field.tag')['then_field'].values
            e_json_con_field = map_condition.query('if_field1 == @group_field.tag')['json_field'].values
            e_json_con_value = map_condition.query('if_field1 == @group_field.tag')['static_value'].values
            e_json_con_group = map_condition.query('if_field1 == @group_field.tag')['json_container'].values

            group_temp_dict = {}

            if len(e_json_group) > 0:
                str_json_group = str(e_json_group[0])
            if len(e_json_con_group) > 0:
                str_json_con_group = str(e_json_con_group[0])


            # # # # # # # REF/TABLE-to-1 -- withOUT conditional mapping
            # e.g. ColCollectionEventRef.ColSiteRef.PolPD1 --> dwc:country
            if group_field.tag not in e_emu_if_field: # and group_field.tag in single_dict.keys()

                if e_json_group not in emu_json_groups:

                    group_all[str(e_json_field)[2:-2]] = group_field.text  # # # # use += instead?                             

            # # # # # # # REF/TABLE-to-1 -- WITH conditional mapping [all currently to multi-value h2i field]
            # e.g. PriAccessionNumberRef.AccAccessionNo --> cd:identifier + cd:identifierType --> 'accession number'
            elif e_emu_if_value == "NOT NULL":  # and str_json_con_group is not None:

                group_temp_dict[str(e_json_field)[2:-2]] = str(group_field.text)
                group_temp_dict[str(e_json_con_field)[2:-2]] = str(group_field.text)

                for key, val in zip(e_json_con_field, e_json_con_value):
                    group_temp_dict[str(key)] = str(val)

                group_all[str_json_con_group].append(group_temp_dict.copy())
            
            group_temp_dict.clear()

            return group_all


def xml_to_json(xml_input, emu_xml_out=False):

    # # # # # # # # # # # # # # # # # # #
    # Import mappings for h2i field-types:
    emu_map = pd.read_csv(config('MAP_PATH') + 'emu_fields.csv', squeeze=True)
    map_condition = pd.read_csv(config('MAP_PATH') + 'emu_conditions.csv', squeeze=True, keep_default_na=False)

    # Single/atomic 
    emu_no_group = emu_map[emu_map['emu_group'].isnull()]['emu'].values
    emu_json_groups = emu_map[emu_map['json_container'].notnull()]['json_container'].values


    # # # # # # # # # # # #
    # Prep input-XML  # # # 
    
    # Turn EMu col-names into XML-tags:
    tree1_string = pi.xml_prep(xml_in = xml_input)
    tree_prep = etree.XML(tree1_string)

    # Remove redacted values
    tree_prep = ri.redact_input(tree_prep, map_condition, emu_map)

    # Return updated xml as string to switch to lxml.etree
    prep_tree_string = etree.tostring(tree_prep).decode('utf-8')

    # Convert back to xml ElementTree
    doc = ET.fromstring(prep_tree_string)
    tree = ET.ElementTree(doc)

    # Setup separate empty dict of h2i terms
    all_records = []

    get_tuples = etree.XPath(".//data")
    tuples = get_tuples(tree_prep)


    # # # # # # # # # # #
    # Convert XML to JSON
    for tuple1 in tuples:

        # # # # # # # # # # #
        # Prep dictionaries

        single_dict = po.prep_output_dict(emu_map, map_condition)

        group_all = single_dict

        get_tup_fields = etree.XPath('./*')
        tup_fields = get_tup_fields(tuple1) 

        for tup_field in tup_fields:

            # Get emu-xml-field's corresponding h2i field + info
            t_emu_field = emu_map.query('emu == @tup_field.tag')['emu'].values
            t_emu_group = emu_map.query('emu == @tup_field.tag')['emu_group'].values
            t_json_field = emu_map.query('emu == @tup_field.tag')['json_field'].values
            t_json_group = emu_map.query('emu == @tup_field.tag')['json_container'].values

            t_emu_if_value = map_condition.query('if_field1 == @tup_field.tag')['if_value1'].values
            # t_emu_then_field = map_condition.query('if_field1 == @tup_field.tag')['then_field'].values
            t_json_con_field = map_condition.query('if_field1 == @tup_field.tag')['json_field'].values
            t_json_con_value = map_condition.query('if_field1 == @tup_field.tag')['static_value'].values
            t_json_con_group = map_condition.query('if_field1 == @tup_field.tag')['json_container'].values

            get_tuples = etree.XPath("./" + str(tup_field.tag) + "//*")
            tuple_group = get_tuples(tuple1)

            
            # # # # # # # # # # # # # # # # 
            # EMu SINGLE fields  (where tup_field.tag is a value in emu_map['emu'])
            if tup_field.tag in emu_no_group: # and tup_field.tag != "tuple":


                # # # # # # #
                # 1-to-1 -- withOUT conditional mapping
                if str(t_json_field)[2:-2] in single_dict.keys():

                    group_all[str(t_json_field[0])] = tup_field.text


                # # # # # # #
                # 1-to-Group -- WITH conditional mapping [all currently to multi-value h2i field]
                elif "NOT NULL" in t_emu_if_value and t_json_group is not None:

                    str_json_con_group = str(t_json_con_group[0])
                    str_json_group = str(t_json_group[0])
                    group_temp_dict = {}

                    group_temp_dict[str(t_json_field)[2:-2]] = str(tup_field.text)

                    for key, val in zip(t_json_con_field, t_json_con_value):
                        group_temp_dict[str(key)] = str(val)

                    group_all[str_json_con_group].append(group_temp_dict.copy())

                    group_temp_dict.clear()


            # # # # # # #
            # EMu REF & TABLE fields  (where tup_field.tag is actually a value in emu_map['emu_group'])
            elif tup_field.tag in emu_map['emu_group'].values and tup_field.tag is not None:

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

                            group_all = get_group_tuple(tup_field, tup_group_field, emu_map, map_condition, group_all)

                # if NOT a tuple:
                else:

                    group_all = get_group_nontuple(tuple_group, tup_field, emu_map, map_condition, group_all)


        for item in group_all.keys():
            if group_all[item] == []:
                group_all[item] = None


        all_records.append(group_all.copy())

        group_all.clear()


    # # # # # # # # #
    # Output 

    # H2I-json
    f = open(config('OUT_PATH') + 'emu_to_json.json', 'w', encoding='utf-8')
    f.write(json.dumps(all_records, indent=True, ensure_ascii=False))
    f.close()


    # Fixed EMu-XML
    if emu_xml_out == True:
        # Output compact xml -- e.g. <tag />
        tree.write(config('OUT_PATH') + "emu_prepped.xml", encoding='utf-8')    

        # # Output 'canonic' xml -- e.g. <tag></tag>
        # # # Commented out until can fix with Ubuntu
        # with open(config('OUT_PATH') + "emu_raw_canonic.xml", mode='w', encoding='utf-8') as out_file:
        #     ET.canonicalize(xml_data=tree1_string, out=out_file)


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_to_json(arg, emu_xml_out=False)