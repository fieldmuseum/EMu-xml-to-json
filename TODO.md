# EMu XML-to-JSON converter

## TO DO
1. Tests
2. Dynamically ref & load external schema (e.g. [LtC JSON schema](https://github.com/tdwg/cd/tree/review/standard/json-schema/))
3. Figure out other more complex fields in EMu/H2I mapping
    - many:1 repeatable nested-table fields
    - other conditional logic

## DONE

1. Tie in EMu exports 
    - Setup daily/weekly cron to run script; 
        - (if Export folder is not empty, get most recent export)
    - Or listen for notification email (sent after export runs)

2. Setup Python env 
    - paths to input & output files
    - OR allow input from cli (better for cron?)

3. Installed Python on Boojum 

4. Included step for XML-checks.
    - check_xml.py logs errors (with xml-error-line in 'out_path/xml_log_YYYYMMDD.txt') if XML is badly-formed or if other exceptions occur.

5. Figured out notification/email with postfix/mail/mutt (+ appropriate smtp ports for local testing)
    Considered:
    - https://realpython.com/python-send-email/ 
    - #4 in https://stackoverflow.com/questions/50695188/what-is-the-proper-way-to-actually-send-mail-from-python-code 

6. Tested basic EMu/H2I mapping for 1:1 fields

7. Figure out more complex fields in EMu/H2I mapping
    - conditional logic
    - conditional static values