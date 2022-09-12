# Convert EMu XML to JSON

# import check_xml as chx
import utils.convert_xml as cvx
from decouple import config
from datetime import date, datetime
import os, glob, re, sys
import utils.notify as notify, utils.out_zip as out_zip


def emu_to_json(xml_in, logs):
    '''convert EMu xml to JSON'''

    # If xml_check is ok, convert XML to JSON:
    # Else output error/exception-log
    try:

        cvx.xml_to_json(xml_input=xml_in, emu_xml_out=True)
        
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

        
    else:
        # Update logs
        log_time = str(datetime.now())
        log_msg = "Finished at " + log_time + ' - Error: ' + str(sys.exc_info()) + '\n'


    print(log_msg)
    logs.write(log_msg)
    # logs.close()


def zip_output(log_date:str):
    ''''''

    # Zip output & cleanup
    files_to_zip = glob.glob(config('OUT_PATH') + '/emu*')  + glob.glob(config('LOG_PATH') + '/xml_log_' + log_date + '.txt')

    if len(files_to_zip) > 0:
        
        zipped_output = config('OUT_PATH') + "xml_json_" + re.sub(".* |:|\.", "", str(datetime.now())) + ".zip"
        out_zip.file_compress(files_to_zip, zipped_output)

        for emu_file in files_to_zip:
            os.remove(emu_file)

    else:
        zipped_output = ""

    return zipped_output


def send_notification(log_msg:str, log_date:str, log_start:str, zipped_output:str):
    '''Send log message as email-notification'''

    # if email == True:
    subject = "EMu xml-to-json results - " + log_date
    message = "Output from EMu-xml-to-json - Starter: " + log_start + " - log: \n" + log_msg
    notify.send_output(message, subject, zipped_output, config('TO_ADD1'))
    # notify.send_output_gmail(log_date, log_time, log_msg, zip_output, to=config('TO_ADD'), fro=config('FROM_ADD'))



def main():
    '''main function'''

    log_date = str(date.today())
    log_start = str(datetime.now())

    logs = open(config('LOG_PATH') + 'xml_log_' + log_date + '.txt', 'a')
    logs.write("\nStart time: " + log_start + "\n")

    print(sys.argv[0])
    # if sys.argv[0] != "emu_xml_to_json.py":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            for filename in glob.glob(arg):
                print(filename)
                emu_to_json(arg, logs)
    
    else:

        # If input is undefined, default to most recent EMu-export
        if len(glob.glob(os.path.join(config('IN_PATH'), '*/'))) > 0:
            # latest_sub = max(glob.glob(os.path.join(config('IN_PATH'), '*/'))) # , key=os.path.getmtime)

            subs_a = os.listdir(config('IN_PATH'))
            subs = [folder for folder in subs_a if folder[0].isdigit()]

            # get most recent folder by its date-name
            subs_conv = subs
            for idx, folder in enumerate(subs):
                subs_conv[idx] = datetime.strptime(folder, '%Y-%m-%d')

            latest_sub = config('IN_PATH') + str(datetime.strftime(max(subs_conv), '%Y-%-m-%-d')) + "/"

            print(latest_sub)

            if len(os.listdir(latest_sub)) > 0:
                xml_in = latest_sub + os.listdir(latest_sub)[0]

            else: 
                xml_in = "no xml file in " + latest_sub

        else: 
            xml_in = "no xml input in " + config('IN_PATH')


        emu_to_json(xml_in, logs)
    
    logs.close()
    log_msg_final = str(logs)

    zipped_output = zip_output(log_date)

    send_notification(log_msg_final, log_date, log_start, zipped_output)


# Run directly with:
#   python3 emu_xml_to_json.py file1 file2 etc
if __name__ == '__main__':
    main()
