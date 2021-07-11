# Convert EMu XML to JSON

import check_xml as chx
import convert_xml as cvx
from decouple import config
from datetime import date, datetime
import os

# Get latest XML export
all_subdirs = [d for d in os.listdir(config('INPUT_PATH')) if os.path.isdir(d)]
latest_sub = max(all_subdirs, key=os.path.getmtime)
xml_in = os.path.join(latest_subdir, os.listdir(latest_sub)[0])
# xml_in = config('INPUT_PATH') + config('INPUT_XML')

# If xml_check is ok, Read in XML file:
# Else output error/exception-log
try:
    cvx.xml_to_json(xml_in)

except Exception as e:
    logs = open(config('OUTPUT_PATH') + 'xml_log_' + str(date.today()) + '.txt', 'a')
    logs.write(str(datetime.now()) + ' - File Input: ' + xml_in + ' : Error : ' + str(e) + '\n')
    logs.close()

    # Supposed to output 'fixed' xml.  Not working.
    chx.fix_xml_encode(xml_in)
    # cx.check_xml_encode(xml_in)
    # cx.check_xml_form(xml_in)
