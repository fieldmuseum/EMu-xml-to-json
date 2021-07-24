# Parse EMu XML to JSON
# 2021-Jun; FMNH
# based on:
#  https://docs.python.org/3/library/xml.etree.elementtree.html
#  https://stackoverflow.com/a/10231610 


import xml.etree.ElementTree as ET
from glob import glob
import json, xmltodict
import pandas as pd
from decouple import config
import sys


def xml_to_json(xml_in, fix_xml=False):
    tree = ET.parse(xml_in) # config('INPUT_PATH') + config('INPUT_XML'))
    root = tree.getroot()

    # Read in EMu-abcd-h2i field mapping
    emu_map = pd.read_csv(config('IN_PATH') + 'abcd_h2i_emu.csv', squeeze=True, index_col=0).to_dict()

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

        # Use EMu-abcd-h2i field-map here:
        if child.tag in emu_map.keys():
            child.tag = emu_map[child.tag]


    # Convert fixed EMu-XML to JSON
    treestring = ET.tostring(root)
    emu_json_out = xmltodict.parse(ET.canonicalize(treestring))


    # Output EMu-json
    f = open(config('OUT_PATH') + 'emu_to_json.json', 'w')
    f.write(json.dumps(emu_json_out, indent=True))
    f.close()


    ######
    # Optional section below to also:
    # Output fixed EMu-XML
    
    if fix_xml == True:

        with open(config('OUT_PATH') + "emu_canonic.xml", mode='w', encoding='utf-8') as out_file:
            ET.canonicalize(xml_data=treestring, out=out_file)
        
        tree.write(config('OUT_PATH') + "emu_xml.xml")
    
    ######

# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_to_json(arg, fix_xml=True)