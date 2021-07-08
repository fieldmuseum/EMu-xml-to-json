# Check XML files
# 2021-jul
# Checks XML encoding and syntax/well-formedness
# (Technically not validation as in "does it conform to a schema?")

# from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch12s02.html
import xml.etree.ElementTree as ET
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
import sys
from datetime import date, datetime
from decouple import config
import re


# Check XML encoding for mangled characters
def check_xml_encode(filename):
    logs = open(config('OUTPUT_PATH') + 'xml_log_' + str(date.today()) + '.txt', 'a')

    try:
        ET.parse(filename) # config('INPUT_PATH') + config('INPUT_XML'))
        logs.write(str(datetime.now()) + ' - File Input: ' + filename + ' is well-formed. \n')
        logs.close()

    except Exception as e:
        logs.write(str(datetime.now()) + ' - File Input: ' + filename + ' : Error : ' + str(e) + '\n')
        logs.close()


# def filter_non_printable(s):
#     return ''.join(c for c in s if not unicodedata.category(c).startswith('C'))

# # #  Not working:
# Fix or normalize XML to handle mangled characters
def fix_xml_encode(filename):
        orig = open(filename, "r")
        fixed = open('fixed_' + filename, "w")

        for line in orig.readlines():
            # line = line.encode("utf-8", 'ignore').decode("utf-8")  # still broken
            # line = re.sub(r'<0x0b>', "X", line)  # didn't find/replace
            # line = re.sub(f'[^{re.escape(line.printable)}]', 'X', line)  # didn't find/replace
            # line = re.sub(f'[^\x00-\x7F]+','X', line)  # didn't find/replace
            # line = filter_non_printable(line)  # strips linebreaks among other things
            line = re.sub('(<0x\w*>)',"", line)
            fixed.write(line)

        orig.close()
        fixed.close()


# Check XML syntax/form (e.g. all open-tags have closing-tags)
def parsefile(file):
    parser = make_parser(  )
    parser.setContentHandler(ContentHandler(  ))
    parser.parse(file)

def check_xml_form(filename):
    logs = open(config('OUTPUT_PATH') + 'xml_log_' + str(date.today()) + '.txt', 'a')
    try:
        parsefile(filename)
        # log_form = (filename + " is well-formed")
        logs.write(str(datetime.now()) + ' - File Input: ' + filename + ' : Well-formed \n')
        logs.close()
    except Exception as e:
        # log_form = (filename + " is badly formed: " + str(e))
        logs.write(str(datetime.now()) + ' - File Input: ' + filename + ' : Badly formed : ' + str(e) + '\n')
        logs.close()


# To run check_xml.py directly, run:
#   python3 check_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            check_xml_encode(arg)
            check_xml_form(arg)
            fix_xml_encode(arg)
