# Convert EMu XML to JSON

import check_xml as chx
import convert_xml as cvx
from decouple import config
from datetime import date, datetime

# If xml_check is ok, Read in XML file
# try test.find("is well-formed") > -1:
xml_in = config('INPUT_PATH') + config('INPUT_XML')

try:
    cvx.xml_to_json(xml_in)

except Exception as e:
    # log_encode = 'error - cannot perform charset normalization: ' + str(e)
    logs = open(config('OUTPUT_PATH') + 'xml_log_' + str(date.today()) + '.txt', 'a')
    logs.write(str(datetime.now()) + ' - File Input: ' + xml_in + ' : Error : ' + str(e) + '\n')
    logs.close()

    # Supposed to output 'fixed' xml.  Not working.
    chx.fix_xml_encode(xml_in)
    # cx.check_xml_encode(xml_in)
    # cx.check_xml_form(xml_in)
    