# Convert EMu XML to JSON

import check_xml as chx
import convert_xml as cvx
from decouple import config
from datetime import date, datetime
import os, glob
import notify

log_date = str(date.today())
log_start = str(datetime.now())

logs = open(config('OUT_PATH') + 'xml_log_' + log_date + '.txt', 'a')
logs.write("\nStart time: " + log_start + "\n")

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
    
    # Update logs
    log_time = str(datetime.now())
    log_msg = "Run-time: " + log_start + " to " + log_time + " - JSON output OK \n"

except Exception as e:

    # Update logs
    log_time = str(datetime.now())
    log_msg = "Run-time: " + log_start + " to " + log_time + ' - File Input Error: ' + xml_in + ' : ' + str(e) + '\n'

    # Supposed to output 'fixed' xml.  Not working.
    chx.fix_xml_encode(xml_in)
    # cx.check_xml_encode(xml_in)
    # cx.check_xml_form(xml_in)

logs.write(log_msg)
logs.close()

# Send notification
notify.send_output(log_date, log_time, log_msg)

