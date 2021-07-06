# [Copy &] Check XML files
# 2021-jul
# Checks XML encoding and syntax/well-formedness
# (Technically not validation as in "does it conform to a schema?")

# from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch12s02.html
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
import sys

from charset_normalizer import normalize

# Check XML's encoding for mangled characters
def check_xml_encode(filename):
    # for arg in sys.argv[1:]:
    #     for filename in glob(arg):
            # try:
            #     parsefile(filename)
            #     test = (filename + " is properly encoded")
            # except Exception as e:
            #     test = (filename + " is badly encoded: " + str(e))
            try:
                normalize(filename) # should write to disk filename-***.ext
                print('see normalized file: ' + filename)
            except IOError as e:
                print('error - cannot perform charset normalization: ', str(e))


# Check XML's syntax/form
def parsefile(file):
    parser = make_parser(  )
    parser.setContentHandler(ContentHandler(  ))
    parser.parse(file)

def check_xml_form(filename):
    # for arg in sys.argv[1:]:
    #     for filename in glob(arg):
            try:
                parsefile(filename)
                test = (filename + " is well-formed")
            except Exception as e:
                test = (filename + " is badly formed: " + str(e))

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            check_xml_encode(arg)
            check_xml_form(arg)

