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
import cProfile  # , line_profiler
from timeit import default_timer as timer

# @profile
def xml_to_json(xml_input, emu_xml_out=False):

    start1 = timer()

    # # # # # # # # # # # # # # # # # # #
    # Import mappings for h2i field-types:
    emu_map = pd.read_csv(config('MAP_PATH') + 'emu_fields.csv', squeeze=True)
    map_condition = pd.read_csv(config('MAP_PATH') + 'emu_conditions.csv', squeeze=True, keep_default_na=False)

    # Single/atomic 
    emu_no_group = emu_map[emu_map['emu_group'].isnull()]['emu'].values
    emu_json_groups = emu_map[emu_map['json_container'].notnull()]['json_container'].values

    # # Redacted fields
    # json_null_fields = map_condition.query('json_field == "NULL"')['json_field'].values


    # # # # # # # # # # # #
    # Prep input-XML  # # # 
    
    time2 = timer()
    print(time2 - start1)
    # Turn EMu col-names into XML-tags:
    tree1_string = pi.xml_prep(xml_in = xml_input)
    time3 = timer()
    print("start + xml_prep [convert emu-attr's to tags] took:")
    print(time3 - time2)

    tree_prep = etree.XML(tree1_string)
    time4 = timer()
    print("tree_prep [string-to-xml] took:")
    print(time4 - time3)


    # Remove redacted values
    tree_prep = ri.redact_input(tree_prep, map_condition)
    time5 = timer()
    print("Remove redacted took:")
    print(time5 - time4)


    # Return updated xml as string to switch to lxml.etree
    prep_tree_string = etree.tostring(tree_prep).decode('utf-8')

    # 3 - convert back to xml ElementTree
    doc = ET.fromstring(prep_tree_string)  # ET.parse(prep_tree_string)   # 
    tree = ET.ElementTree(doc)
    time6 = timer()
    print("MAYBE SKIP? convert back to xml ET [for xml_prep_output / not for any h2i stuff]:")
    print(time6 - time5)

    # Setup separate empty dict of h2i terms
    all_records = []
    # append1 = all_records.append
    # copy1 = dict.copy

    get_tuples = etree.XPath(".//data")
    tuples = get_tuples(tree_prep)
    time7 = timer()
    print("get_tuples:")
    print(time7 - time6)


    # # # # # # # # # # #
    # Convert XML to JSON
    for tuple1 in tuples:
        time75 = timer()

        # # # # # # # # # # #
        # Prep dictionaries

        single_dict = po.prep_output_dict(emu_map, map_condition)

        group_all = single_dict

        get_tup_fields = etree.XPath('./*')
        tup_fields = get_tup_fields(tuple1) 

        time76 = timer()
        print("START loop:")
        print(time76 - time75)

        for tup_field in tup_fields:

            time76 = timer()

            # Get emu-xml-field's corresponding h2i field + info
            t_emu_field = emu_map.query('emu == @tup_field.tag')['emu'].values
            # t_emu_group = emu_map.query('emu == @tup_field.tag')['emu_group'].values
            t_json_field = emu_map.query('emu == @tup_field.tag')['json_field'].values
            t_json_group = emu_map.query('emu == @tup_field.tag')['json_container'].values

            t_emu_if_value = map_condition.query('if_field1 == @tup_field.tag')['if_value1'].values
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

                time77 = timer()
                print("--- FINISH a SINGLE field:")
                print(time77 - time76)


            # # # # # # #
            # EMu REF & TABLE fields  (where tup_field.tag is actually a value in emu_map['emu_group'])
            elif tup_field.tag in emu_map['emu_group'].values and tup_field.tag is not None:

                t_emu_field = emu_map.query('emu_group == @tup_field.tag')['emu'].values
                m_emu_group = emu_map.query('emu_group == @tup_field.tag')['emu_group'].values
                t_json_field = emu_map.query('emu_group == @tup_field.tag')['json_field'].values
                t_json_group = emu_map.query('emu_group == @tup_field.tag')['json_container'].values

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

                                e_json_field = emu_map.query('emu_group == @tup_field.tag')['json_field'].values
                                e_json_group = emu_map.query('emu_group == @tup_field.tag')['json_container'].values

                                group_temp_dict = dict.fromkeys(e_json_field)

                                if len(e_json_group) > 0:
                                    str_json_group = str(e_json_group[0])
                                # if len(e_json_con_group) > 0:
                                #     str_json_con_group = str(e_json_con_group[0])

                                for sib_key in tup_group_field:
                                    if sib_key.text != "" and sib_key.text is not None:
                                        sib_key_str = str(emu_map.query('emu == @sib_key.tag')['json_field'].values)[2:-2]
                                        if sib_key.tag in t_emu_field:
                                            group_temp_dict[sib_key_str] = str(sib_key.text)
                                
                                if str_json_group in emu_json_groups:

                                    group_all[str_json_group].append(group_temp_dict.copy())
                                
                                elif len(tup_group_field) == 1:

                                    group_all[str(e_json_field)[2:-2]] = tup_group_field[0].text


                # if NOT a tuple:
                else:
                    for group_field in tuple_group:
                            
                        if group_field.tag in t_emu_field:

                            e_json_field = emu_map.query('emu == @group_field.tag')['json_field'].values
                            e_json_group = emu_map.query('emu == @group_field.tag')['json_container'].values

                            e_emu_if_field = map_condition.query('if_field1 == @group_field.tag')['if_field1'].values
                            e_emu_if_value = map_condition.query('if_field1 == @group_field.tag')['if_value1'].values
                            # e_emu_then_field = map_condition.query('if_field1 == @group_field.tag')['then_field'].values
                            e_json_con_field = map_condition.query('if_field1 == @group_field.tag')['json_field'].values
                            e_json_con_value = map_condition.query('if_field1 == @group_field.tag')['static_value'].values
                            e_json_con_group = map_condition.query('if_field1 == @group_field.tag')['json_container'].values

                            group_temp_dict = {}

                            # if len(e_json_group) > 0:
                            #     str_json_group = str(e_json_group[0])
                            # if len(e_json_con_group) > 0:
                            #     str_json_con_group = str(e_json_con_group[0])


                            # # # # # # # REF/TABLE-to-1 -- withOUT conditional mapping
                            # e.g. ColCollectionEventRef.ColSiteRef.PolPD1 --> dwc:country
                            if group_field.tag not in e_emu_if_field: # and group_field.tag in single_dict.keys()

                                if e_json_group not in emu_json_groups:

                                    group_all[str(e_json_field)[2:-2]] = group_field.text  # # # # use += instead?                             

                            # # # # # # # REF/TABLE-to-1 -- WITH conditional mapping [all currently to multi-value h2i field]
                            # e.g. PriAccessionNumberRef.AccAccessionNo --> cd:identifier + cd:identifierType --> 'accession number'
                            # Conditions besides 'NOT NULL' + h2i-container would currently need separate 'elif' statements
                            elif e_emu_if_value == "NOT NULL":  # and str(e_json_con_group[0]) is not None:

                                group_temp_dict[str(e_json_field)[2:-2]] = str(group_field.text)

                                for key, val in zip(e_json_con_field, e_json_con_value):
                                    group_temp_dict[str(key)] = str(val)

                                group_all[str(e_json_con_group[0])].append(group_temp_dict.copy())

                            group_temp_dict.clear()

                time77 = timer()
                print("--- FINISH a REF/TABLE field:")
                print(time77 - time76)

        # time77 = timer()
        # print("END of loop:")
        # print(time77 - time76)


        all_records.append(group_all.copy())
        # append1(copy1(group_all))  # avoid dots?

        time8 = timer()
        print("APPEND group_all to all_records:")
        print(time8 - time77)


        group_all.clear()


    # # # # # # # # #
    # Output 

    # H2I-json
    f = open(config('OUT_PATH') + 'emu_to_json.json', 'w')
    f.write(json.dumps(all_records, indent=True))
    f.close()
    time9 = timer()
    print("output json:")
    print(time9 - time8)


    # Fixed EMu-XML
    if emu_xml_out == True:
        # Output compact xml -- e.g. <tag />
        tree.write(config('OUT_PATH') + "emu_prepped.xml")    

        # # Output 'canonic' xml -- e.g. <tag></tag>
        # # # Commented out until can fix with Ubuntu
        # with open(config('OUT_PATH') + "emu_raw_canonic.xml", mode='w', encoding='utf-8') as out_file:
        #     ET.canonicalize(xml_data=tree1_string, out=out_file)

    time10 = timer()
    print("finish output xml:")
    print(time10 - time9)


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            # xml_to_json(arg, emu_xml_out=False)
            cProfile.run('xml_to_json(arg, emu_xml_out=False)', sort = 'ncalls')
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    # for arg in sys.argv[1:]:
    #     for filename in glob(arg):
    #         xml_to_json(arg, emu_xml_out=False)
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.strip_dirs()
    # stats.dump_stats('stats.txt')
    # stats.print_stats()  