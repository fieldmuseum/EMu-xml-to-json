# EMu XML-to-JSON converter

## How to setup & use

### In EMu:
1. Export a set of records as XML.  

2. When possible, check that the XML output is well-formed.
    - ['Scholarly XML' VSCode add-on](https://marketplace.visualstudio.com/items?itemName=raffazizzi.sxml)
    - [xmllint](http://xmlsoft.org/xmllint.html#diagnostics) on Mac/Unix/Linux or [xsltproc](https://community.chocolatey.org/packages/xsltproc#individual) on Windows -- Try this in terminal/shell: 
        - `xmllint --noout file.xml && echo $?`
    - [Online XML validator](https://www.w3schools.com/xml/xml_validator.asp)
        Warning -  avoid online-validators for sensitive data.

3. Setup a CSV named "abcd_h2i_emu.csv" with EMu-column-names in the 1st column, and corresponding standard-term names in the 2nd column.  [See example in 'Input' section](#input)


### Not in EMu:

1. Clone this repo

2. Set local environment variables by adding a text file named `.env` in the root of the repo. Open it and add variables following the [`.env.example`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/.env.example) file. More [info here](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) if needed.

3. Install [Python 3.9 or later](https://www.python.org/downloads/)

4. Install the python packages listed in [required.txt](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/required.txt) with `pip` or `pip3`:

    `pip3 install charset-normalizer json pandas python-decouple xml xmltodict`

5. Run the script -- e.g.:

    Use `.env` to specify the data_input folder where the newest file is the XML-input:
    `python3 emu_xml_to_json.py`

    Or manually specify an XML-input in the command to run the script:
    `python3 emu_xml_to_json.py data_in/2021-08-08/sample.xml`

6. Output JSON, XML and log are zipped and emailed.
    See JSON output in `emu_to_json.json`, or error log in `xml_log_YYYYMMDD.txt`

## Input
- EMu XML Export - An XML file containing records exported from EMu as XML
    - [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/2021-08-09/sample.xml)
    - example of input with badly-encoded character [here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/2021-08-08/sample_bad.xml)
- `abcd_h2i_emu.csv` EMu/Standards mapping doc - A 2-column CSV listing EMu column-names in the 1st column and corresponding standard terms in the 2nd column.
    - [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/mappings/abcd_h2i_emu.csv)
- [DRAFT] `abcd_h2i_conditions.csv` - Conditional logic doc - A 4-column CSV to document conditional mapping logic for multi-value-tables where rows are conditionally parsed to separate standard terms.
    - [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/mappings/abcd_h2i_conditions.csv)

## Output
- [`emu_to_json.json`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/sample_data_out/emu_to_json.json) = Records as JSON objects, with EMu-fields/data as key/value pairs.
- [`emu_xml.xml`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/sample_data_out/emu_xml.xml) (optional) = XML with EMu column-names as xml-tags instead of xml-attributes
- [xml_log_YYYY-MM-DD.txt](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/log/xml_log_2021-07-24.txt) = Log of successful or failed output. 
- email notifications (currently requires mutt to send email, or gmail-only recipients)
    - Log-messages comprise the email-body
    - Output files are zipped and attached
