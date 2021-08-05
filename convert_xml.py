# Parse EMu XML to JSON
# 2021-Jun; FMNH
# based on:
#  https://docs.python.org/3/library/xml.etree.elementtree.html
#  https://stackoverflow.com/a/10231610 


import xml.etree.ElementTree as ET
from glob import glob
import json
import pandas as pd
from decouple import config
import sys


def xml_to_json(xml_input):

    # Read in EMu-h2i field mapping
    emu_map = pd.read_csv(config('MAP_PATH') + 'h2i_emu.csv', squeeze=True)

    # Read in EMu-h2i conditional mapping
    map_condition = pd.read_csv(config('MAP_PATH') + 'h2i_conditions.csv', squeeze=True)


    # Prep h2i fields  
    atomic = emu_map.query('repeatable != "yes"')
    h2i_atomic = atomic['h2i_field'].values
    atom_temp = dict.fromkeys(tuple(h2i_atomic))  # ""


    repeatable = emu_map.query('repeatable == "yes"')
    h2i_rep = repeatable['h2i_field'].values
    rep_dict = dict.fromkeys(tuple(h2i_rep), [])  # {} 


    # Setup xml
    tree = ET.parse(xml_input)
    root = tree.getroot()

    # Replace "table" "tag with table-name
    root.tag = root.get('name')
    root.attrib = {}

    # Replace top-level "tuple" with "data" 
    for thing in root:

        if thing.get('name') is None:
            if thing.tag == "tuple":
                thing.tag = "data"
            thing.set('name', thing.tag)

    # Turn EMu col-names into XML-tags instead of attributes:
    for child in root.findall('.//*'):

        child.tag = child.get('name')
        child.attrib = {}


    # Setup separate empty xml-tree of h2i terms

    all_records = []

    tuples = tree.findall(".//data")

    for tuple1 in tuples:

        h2i_records = []
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

            # Get ref/table EMu fields

            for e in elems:

                if e.tag is not None and e.tag in str(emu_map['emu'].values):

                    e_tag = e.tag
                    # print(e_tag)
                    emu_tab = emu_map.query('emu == @e_tag')
                    h2i_tab = str(emu_tab['h2i_field'].values)[2:-2]
                    tuple_temp[h2i_tab] = e.text 
                    # print(h2i_tab + "  --- " + e.text)
                
        h2i_records = tuple_temp


        # # # # # # # # # # # # #

        # Get repeatable h2i fields  
        rep_temp = rep_dict

        for h2i_rep_field_a in h2i_rep:  #  repeatable['emu'].values[2:-2]:  # str(emu_map['repeatable'].values) == 'yes':
            
            tup_fields = tuple1.findall('.//*')  

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