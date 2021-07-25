# Convert EMu XML to JSON

import check_xml as chx
import convert_xml as cvx
from decouple import config
from datetime import date, datetime
import os, glob, re, sys
import notify, out_zip

log_date = str(date.today())
log_start = str(datetime.now())

logs = open(config('LOG_PATH') + 'xml_log_' + log_date + '.txt', 'a')
logs.write("\nStart time: " + log_start + "\n")

# If xml_check is ok, convert XML to JSON:
# Else output error/exception-log
try:

    # Get latest XML export (if any available)
    # # from https://stackoverflow.com/a/32093754
    if len(glob.glob(os.path.join(config('IN_PATH'), '*/'))) > 0:
        latest_sub = max(glob.glob(os.path.join(config('IN_PATH'), '*/')), key=os.path.getmtime)
    
        if len(os.listdir(latest_sub)) > 0:
            xml_in = latest_sub + os.listdir(latest_sub)[0]

        else: 
            xml_in = "no xml file in " + latest_sub

    else: 
        xml_in = "no xml input in " + config('IN_PATH')

    cvx.xml_to_json(xml_in, fix_xml=True)
    
    # Update logs
    log_time = str(datetime.now())
    log_msg = "Finished at " + log_time + " - JSON output OK \n"


except (NameError, IndexError, FileNotFoundError) as err:
    # Update logs
    log_time = str(datetime.now())
    log_msg = "Finished at " + log_time + ' - Error: ' + xml_in + ' : ' + str(err) + '\n'

except Exception as e:

    # Update logs
    log_time = str(datetime.now())
    log_msg = "Finished at " + log_time + ' - File Input Error: ' + xml_in + ' : ' + str(e) + '\n'

    # Output 'fixed' xml (but check log + fixed.xml manually)
    chx.fix_xml_encode(xml_in)
    # cx.check_xml_encode(xml_in)
    # cx.check_xml_form(xml_in)
    
else:
    # Update logs
    log_time = str(datetime.now())
    log_msg = "Finished at " + log_time + ' - Unexpected Error: ' + sys.exc_info()[0] + '\n'


logs.write(log_msg)
logs.close()

# Zip output & cleanup
files_to_zip = glob.glob(config('OUT_PATH') + '/emu*')

if len(files_to_zip) > 0:
    
    zip_output = config('OUT_PATH') + "xml_json_" + re.sub(".* |:|\.", "", str(datetime.now())) + ".zip"
    out_zip.file_compress(files_to_zip, zip_output)

    for emu_file in files_to_zip:
        os.remove(emu_file)

else:
    zip_output = ""

# Send notification
notify.send_output(log_date, log_time, log_msg, zip_output)
