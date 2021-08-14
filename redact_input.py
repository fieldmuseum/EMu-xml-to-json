# Redact xml values for EMu fields mapped to "NULL" h2i field

# import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from glob import glob
import sys


def redact_input(input, map_conditions):

    h2i_null_fields = map_conditions.query('h2i_field == "NULL"')['h2i_field'].values

    get_cols = etree.XPath('.//*')

    for column in get_cols(input):

        if column.tag is not None:


            # # # # # # # # # # # #
            # Clear redacted values
            for h2i_null_field1 in h2i_null_fields:

                h2i_null_field = str(h2i_null_field1)

                emu_if_field = map_conditions.query('h2i_field == @h2i_null_field')['if_field1'].values
                emu_if_value = map_conditions.query('h2i_field == @h2i_null_field')['if_value1'].values
                emu_then_field = map_conditions.query('h2i_field == @h2i_null_field')['then_field'].values
                h2i_con_value = map_conditions.query('h2i_field == @h2i_null_field')['static_value'].values

                if str(column.tag) == str(emu_if_field)[2:-2]: # and column.text == str(emu_if_value): # "NULL":

                    emu_xpath_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/preceding-sibling::' + str(emu_then_field)[2:-2]
                    emu_xpath = etree.XPath(emu_xpath_string)
                    emu_then_update = emu_xpath(input) 
                                        
                    if emu_then_update != []:

                        emu_then_update[0].text = ""


                    # Also check for 'following-siblings'
                    emu_xpath2_string = './/tuple/' + str(emu_if_field)[2:-2] + '[.="' + str(emu_if_value)[2:-2] + '"]/following-sibling::' + str(emu_then_field)[2:-2]
                    emu_xpath2 = etree.XPath(emu_xpath2_string)
                    emu_then_update2 = emu_xpath2(input) 

                    if emu_then_update2 != []:

                        emu_then_update2[0].text = ""
                    
                    # if the emu_if-field should also be updated, update it too:
                    if str(column.text) == str(emu_if_value)[2:-2]:
                        column.text = ""

    return input

    # TO DO
    #  -- replace above with 'just remove the tuple'
    #  -- check that it works on atomic fields [not just table]


# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            redact_input(arg)