# Redact xml values for EMu fields mapped to "NULL" h2i field

# import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from glob import glob
import sys


def redact_input(input, map_conditions):  # , emu_mapping):

    # h2i_null_fields = map_conditions.query('h2i_field == "NULL"')['h2i_field'].values
    m_emu_if_fields = map_conditions.query('h2i_field == "NULL"')['if_field1'].values

    get_cols = etree.XPath('.//*')

    for column in get_cols(input):

        if column.tag is not None and column.tag in m_emu_if_fields:

            # # # # # # # # # # # #
            # Clear redacted values
            # for h2i_null_field1 in h2i_null_fields:
            for m_emu_if_field in m_emu_if_fields:

                m_emu_if_is_value = map_conditions.query('if_field1 == @column.tag & if_logic1 == "IS" & h2i_field == "NULL"')['if_value1'].values
                m_emu_if_isnt_value = map_conditions.query('if_field1 == @column.tag & if_logic1 == "IS NOT" & h2i_field == "NULL"')['if_value1'].values

                m_emu_then_field = map_conditions.query('if_field1 == @column.tag & h2i_field == "NULL"')['then_field'].values

                print("redactable value:  " + str(column.text))
                print("if IS value:  " + str(m_emu_if_is_value) + "  & NOT value:  " + str(m_emu_if_isnt_value))


                # Redact values where 'if_logic' + 'if_value' criteria are met
                if str(column.text) in m_emu_if_is_value or (str(column.text) not in m_emu_if_isnt_value and len(m_emu_if_isnt_value) > 0): # "NULL":

                    print("REDACTED value:  " + str(column.text))

                    for emu_then_field in m_emu_then_field:

                        emu_xpath_string = './/tuple/' + column.tag + '[.="' + column.text + '"]/preceding-sibling::' + emu_then_field
                        emu_xpath = etree.XPath(emu_xpath_string)
                        emu_then_update = emu_xpath(input) 
                                            
                        if emu_then_update != []:

                            emu_then_update[0].text = ""


                        # Also check for 'following-siblings'
                        emu_xpath2_string = './/tuple/' + column.tag + '[.="' + column.text + '"]/following-sibling::' + emu_then_field
                        emu_xpath2 = etree.XPath(emu_xpath2_string)
                        emu_then_update2 = emu_xpath2(input) 

                        if emu_then_update2 != []:

                            emu_then_update2[0].text = ""

                        
                    # update the emu_if-field, too:
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