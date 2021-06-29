# Parse EMu XML to JSON
# 2021-Jun; FMNH
# based on:
#  https://docs.python.org/3/library/xml.etree.elementtree.html
#  https://stackoverflow.com/a/10231610 


import xml.etree.ElementTree as ET
import json, xmltodict
import pandas as pd
from lxml.etree import fromstring, tostring
from decouple import config


# Read in XML file
tree = ET.parse(config('INPUT_PATH') + config('INPUT_XML'))
root = tree.getroot()

# Read in EMu-ABCDEFGHHI field mapping
emu_map = pd.read_csv(config('INPUT_PATH') + 'abcd_emu.csv', squeeze=True, index_col=0).to_dict()


# Turn EMu col-names into XML-tags instead of attributes:

# Add placeholder-attrib "name" = "tuple" for <tuple> nodes
# (maybe not necessary)
for thing in root:

    if thing.get('name') is None:
        thing.set('name', thing.tag)


# Simplify EMu xml-tags to EMu column-names
for child in root.findall('.//*'):

    child.tag = child.get('name')
    child.attrib = {}

    # Use EMu-ABCDEFGHHI field-map here:
    if child.tag in emu_map.keys():
        child.tag = emu_map[child.tag]


# Convert fixed EMu-XML to JSON
treestring = ET.tostring(root)
emu_json_out = xmltodict.parse(ET.canonicalize(treestring))


# Output EMu-json
f = open(config('OUTPUT_PATH') + 'emu_to_json.json', 'w')
f.write(json.dumps(emu_json_out))
f.close()


#######
# # Uncomment section below to also:
# # Output fixed EMu-XML
#
# with open("emu_canonic.xml", mode='w', encoding='utf-8') as out_file:
#     ET.canonicalize(xml_data=treestring, out=out_file)
#
# tree.write("emu_xml.xml")
# 
#######
