# Convert EMu XML to JSON

import check_xml as chx
import convert_xml as cvx
from decouple import config
from datetime import date, datetime
import os, glob

# If xml_check is ok, convert XML to JSON:
# Else output error/exception-log
try:

    # Get latest XML export (if any available)
    # # from https://stackoverflow.com/a/32093754
    if len(glob.glob(os.path.join(config('IN_PATH'), '*/'))) > 0:
        latest_sub = max(glob.glob(os.path.join(config('IN_PATH'), '*/')), key=os.path.getmtime)
        xml_in = latest_sub + os.listdir(latest_sub)[0]

    else: 
        xml_in = "no xml input in " + config('IN_PATH')

    cvx.xml_to_json(xml_in)

except Exception as e:
    logs = open(config('OUT_PATH') + 'xml_log_' + str(date.today()) + '.txt', 'a')
    logs.write(str(datetime.now()) + ' - File Input: ' + xml_in + ' : Error : ' + str(e) + '\n')
    logs.close()

    # Supposed to output 'fixed' xml.  Not working.
    chx.fix_xml_encode(xml_in)
    # cx.check_xml_encode(xml_in)
    # cx.check_xml_form(xml_in)
