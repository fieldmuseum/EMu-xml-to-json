# Parse EMu XML to JSON
# 2021-Jun; FMNH
# based on:
#  https://docs.python.org/3/library/xml.etree.elementtree.html
#  https://stackoverflow.com/a/10231610 


from typing import Text
import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO
from glob import glob
import json
import pandas as pd
import numpy as np
from decouple import config
import sys


def xml_to_json(xml_input):

    # Read in EMu-h2i field mapping
    emu_map = pd.read_csv(config('MAP_PATH') + 'h2i_emu.csv', squeeze=True)

    # Read in EMu-h2i conditional mapping
    map_condition = pd.read_csv(config('MAP_PATH') + 'h2i_conditions.csv', squeeze=True, keep_default_na=False)


    # Prep h2i fields  
    atomic = emu_map.query('repeatable != "yes"')
    h2i_atomic = atomic['h2i_field'].values
    atom_temp = dict.fromkeys(tuple(h2i_atomic))

    repeatable = emu_map.query('repeatable == "yes"')
    h2i_rep = repeatable['h2i_field'].values
    rep_dict = dict.fromkeys(tuple(h2i_rep), [])

    h2i_con_fields = map_condition['h2i_field'].values
    # h2i_con_fields_1 = pd.DataFrame(h2i_con_fields) # h2i_con_fields[pd.notnull(h2i_con_fields)]
    # h2i_con_fields_2 = h2i_con_fields_1.ix['h2i_field' != "NULL"]
    # h2i_con_fields_2 = h2i_con_fields[pd.notnull(h2i_con_fields)]
    h2i_con_fields_2 = map_condition.query('h2i_field != "NULL"')['h2i_field'].values
    con_dict = dict.fromkeys(tuple(h2i_con_fields_2), [])


    # Prep input-xml
    tree1 = ET.parse(xml_input)   # ET.XML(prep_tree)
    # tree = ET.parse(xml_input)
    root1 = tree1.getroot()


    # Replace "table" "tag with table-name
    root1.tag = root1.get('name')
    root1.attrib = {}

    # Replace top-level "tuple" with "data" 
    for thing in root1:

        if thing.get('name') is None:
            if thing.tag == "tuple":
                thing.tag = "data"
            thing.set('name', thing.tag)

    # Turn EMu col-names into XML-tags instead of attributes:
    for child in root1.findall('.//*'):

        child.tag = child.get('name')
        child.attrib = {}

    tree1_string = ET.tostring(tree1.getroot())

    # 1 - import as lxml ElementTree
    tree_prep = etree.XML(tree1_string)
    print("tree_prep type :  " + str(type(tree1_string)))
    # root = tree_prep.getroot()

    # 2 - Find/Prep values with lxml.etree.xpath()

    get_cols = etree.XPath('.//data')
    # Turn EMu col-names into XML-tags instead of attributes:
    for column in get_cols(tree_prep): # .XPath('.//*'):

        if column.tag is not None:
            print(column.tag)
            # column.tag = column.get('name')
            # column.attrib = {}


            # # # # # # # # # # 
            # Clear redacted values
            for h2i_con_field_a in h2i_con_fields:
                    
                # tup_fields = tuple1.findall('.//*')  

                h2i_con_field = str(h2i_con_field_a)
                # print('h2i con field:  ' + str(h2i_con_field))

                emu_if_field = map_condition.query('h2i_field == @h2i_con_field')['if_field1'].values
                emu_if_value = map_condition.query('h2i_field == @h2i_con_field')['if_value1'].values
                emu_then_field = map_condition.query('h2i_field == @h2i_con_field')['then_field'].values
                h2i_con_value = map_condition.query('h2i_field == @h2i_con_field')['static_value'].values
                
                print("h2i field:  " + str(h2i_con_field))

                if h2i_con_field == "NULL":
                    print(h2i_con_field)

                    # 'NOT NULL' condition covered with 'if tup_field.text is not None'
                    emu_xpath = etree.XPath('./' + str(column.tag) + '[.="' + str(emu_if_value)[2:-2] + '"]/preceding-sibling::' + str(emu_then_field)[2:-2])
                    # emu_xpath_1 = './' + str(column.tag) + '[.="' + str(emu_if_value)[2:-2] + '"]/preceding-sibling::' + str(emu_then_field)[2:-2]
                    # print(emu_xpath_1)

                    print(str(type(emu_xpath(tree_prep))))  # .xpath(emu_xpath_1))))

                    # emu_xpath_2 = './/preceding-sibling::' + str(emu_then_field)[2:-2] + '["' + str(emu_then_field)[2:-2] + '"]'
                    # print("tup_find:  " + str(tuple1.findall(emu_xpath_1)))
                    print("tup xslt:  " + './' + str(emu_then_field)[2:-2])
                    emu_then_update = emu_xpath(tree_prep) 
                    print('emu_then_up:  ' + str(type(emu_then_update)))
                    if emu_then_update != []:
                        emu_then_update[0].text = ""
                    
                    # if the emu_if-field should also be updated, update it too:
                    column.text = ""
                    # tup_field[emu_then_field].text = ""
                    # print("tup_field_txt:  " + str(tup_field.findall(str(emu_then_field))))
                    # print(tup_field.tag + " -- " + tup_field.text)
                    # temp_dict_con.append(str(tup_field.text))


    # output updated xml to check
    et = ET.ElementTree(tree_prep)
    et.write(config('OUT_PATH') + 'check_prep.xml')  #, pretty_print=True)

    # Return updated xml as string

    prep_tree_string = etree.tostring(tree_prep).decode('utf-8')
    

    print("tree_prep type" + str(type(prep_tree_string)))

    # prep_tree = prep_xml(xml_input)

    # 3 - convert to xml ElementTree

    doc = ET.fromstring(prep_tree_string)  # ET.parse(prep_tree_string)   # 
    tree = ET.ElementTree(doc)
    # tree = ET.parse(xml_input)
    # root = tree.getroot()

    # Setup separate empty dict of h2i terms

    all_records = []

    tuples = tree.findall(".//data")

    for tuple1 in tuples:

        tup_fields = tuple1.findall('.//*') 

        # # # # # # # # # # # # # #

        # Get conditional h2i fields  
        h2i_records = []
        con_temp = con_dict

        for h2i_con_field_a in h2i_con_fields:
            
            # tup_fields = tuple1.findall('.//*')  

            h2i_con_field = str(h2i_con_field_a)
            # print('h2i con field:  ' + str(h2i_con_field))

            emu_if_field = map_condition.query('h2i_field == @h2i_con_field')['if_field1'].values
            emu_if_value = map_condition.query('h2i_field == @h2i_con_field')['if_value1'].values
            emu_then_field = map_condition.query('h2i_field == @h2i_con_field')['then_field'].values
            h2i_con_value = map_condition.query('h2i_field == @h2i_con_field')['static_value'].values
            # print("emu if:  " + str(emu_if_field))

            temp_dict_con = []  


            for tup_field in tup_fields:

                # print("test:  " +  str(pd.isnull(h2i_con_field)))
                if tup_field.text is not None and tup_field.tag in emu_if_field:

                    # # # # # # # # # # 
                    # Add static values
                    tup_field_tag = str(tup_field.tag)

                    if str(emu_if_value) == "NOT NULL" and tup_field.tag is not None:

                        # print(str(emu_if_value))
                        temp_dict_con.append(str(h2i_con_value))
                        # temp_dict_con.append(str(tup_field.text))
                    

                    # # # # # # # # # # # 
                    # # Other conditions placeholder
                    # tup_field_tag = str(tup_field.tag)

                    # if str(emu_if_value) == "NOT NULL": 
                                    
                    #     temp_dict_con.append(tup_field.text)

                    
                if str(h2i_con_field_a) not in ["nan", "NaN", ""]:  # and h2i_con_field is not None:
                    if h2i_con_value in h2i_con_fields_2:
                        con_temp[h2i_con_field_a] = temp_dict_con  # h2i_con_value
                        # print('h2i_con_field:  ' + str(temp_dict_con))
        
        h2i_records = con_temp
        # h2i_records.update(con_temp)
        # h2i_conditions.update(con_temp)
        # print('h2i_recs =  ' + str(h2i_records))  # OK


        # h2i_records = []
        tuple_temp = atom_temp

        for elem in tuple1:


            # # # # # # # # # # # # #

            # Get single/atomic EMu fields

            if elem.tag is not None and elem.tag in str(emu_map['emu'].values):
                elem_tag = elem.tag
                emu = emu_map.query('emu == @elem_tag')

                h2i = str(emu['h2i_field'].values)[2:-2]  # .to_string includes pd metadata/mess
                xslt_string =  str(emu['emu_xslt_search'].values)  # './/ColCollectionEventRef/ColSiteRef'


                if len(h2i) > 0:
                    tuple_temp[h2i] = elem.text 
                

            elems = elem.findall('.//*')  
                
            
            # # # # # # # # # # # # #

            # Get ref/table EMu fields (nested another level down inside a 'tuple' tag)

            for e in elems:

                if e.tag is not None and e.tag in str(emu_map['emu'].values):

                    e_tag = e.tag
                    # print(e_tag)
                    emu_tab = emu_map.query('emu == @e_tag')
                    h2i_tab = str(emu_tab['h2i_field'].values)[2:-2]
                    tuple_temp[h2i_tab] = e.text 
                    # print(h2i_tab + "  --- " + e.text)
                
        # h2i_records = tuple_temp
        h2i_records.update(tuple_temp)


        # # # # # # # # # # # # #

        # Get repeatable h2i fields 
         
        rep_temp = rep_dict

        # tup_fields = tuple1.findall('.//*') 

        for h2i_rep_field_a in h2i_rep:

            h2i_rep_field = str(h2i_rep_field_a)

            emu_rep_fields = repeatable.query('h2i_field == @h2i_rep_field')['emu'].values

            temp_dict = []  

            for tup_field in tup_fields:

                if tup_field.text is not None and tup_field.tag in emu_rep_fields:
                                    
                    temp_dict.append(tup_field.text) 
                
                rep_temp[h2i_rep_field] = temp_dict
                # print('rep_temp-sub:  ' + str(rep_temp[h2i_rep_field]))

        h2i_records.update(rep_temp)
        # print('h2i_recs =  ' + str(h2i_records))  # OK

        # all_records.append({"data": h2i_records.copy()})
        all_records.append(h2i_records.copy())

        
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