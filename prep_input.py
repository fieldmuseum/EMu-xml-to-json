# Prep input-XML
# 2021-Aug; FMNH


from typing import Text
import xml.etree.ElementTree as ET
from lxml import etree
from glob import glob
import json
import pandas as pd
import numpy as np
from decouple import config
import sys


def xml_prep(xml_in):


    # # # # # # # # # # #
    # Prep input-xml  # # 
    tree1 = ET.parse(xml_in)
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

        if child.tag == "tuple" and child.get('name') is None:
            child.set('name', 'tuple')
        child.tag = child.get('name')
        child.attrib = {}

    tree1_string = ET.tostring(tree1.getroot())

    return tree1_string


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            xml_prep(arg)
            