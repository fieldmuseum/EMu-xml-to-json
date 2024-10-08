# EMu XML-to-JSON converter for cultural data
A script to convert EMu XML exports to JSON for cultural data. Note - For record-sets > 1000, this can be slow.
It is based on a combination of standards: Darwin core, Latimer core, Audubon Core and the very draft H2I extension to ABCD.
We are currently testing it as a sustainable way to share data with partners from [Digital Benin](https://digital-benin.org/) and [Mapping Philippine Material Culture](https://philippinestudies.uk/mapping/)


## How to setup & use

### In EMu:
1. Export a set of records as XML.
    - See the list of exported EMu fields in the registry entries here: [H2I_emu_reports_eregistry.csv](data_in/H2I_emu_reports_eregistry.csv)
    - Catalog export of record data called: H2I_JSON_Export_DarwinCore
      - *Corresponding Registry entry for report called 'H2I_DwC_Export_Report'*
    - Catalog export of associated Multimedia called: H2I_JSON_Export_AudubonCore
      - *Corresponding Registry entry for report called 'H2I_AC_Export_Report'*

3. When possible, check that the XML output is well-formed.
    - ['Scholarly XML' VSCode add-on](https://marketplace.visualstudio.com/items?itemName=raffazizzi.sxml)
    - [xmllint](http://xmlsoft.org/xmllint.html#diagnostics) on Mac/Unix/Linux or [xsltproc](https://community.chocolatey.org/packages/xsltproc#individual) on Windows -- Try this in terminal/shell: 
        - `xmllint --noout file.xml && echo $?`
    - [Online XML validator](https://www.w3schools.com/xml/xml_validator.asp)
        Warning -  avoid online-validators for sensitive data.

4. Set up these two CSV's following [instructions/examples from the 'Input' section](#input):
    - **emu_fields.csv** - to map EMu-column-names to corresponding standard-term names. 
    - **emu_conditions.csv** - for EMu-fields and values that need conditional mapping or redaction.


### Not in EMu:
1. Clone this repo

2. Set local environment variables by adding a text file named **.env** in the root directory of this repo. Open it and follow the [**.env.example**](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/.env.example) file. More [info here](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) if needed.
    - `IN_PATH` = the path to your input XML file
    - `MAP_PATH` = the path to your emu_conditions.csv
    - `OUT_PATH` & `LOG_PATH` = the path where you want the output JSON and log files to go
    - `FROM_ADD` & `TO_ADD1` = the sender and recipient email addresses for notifications
    - other examples-variables are included for using `'mutt` to send notifications from a server

3. Install [Python 3.9 or later](https://www.python.org/downloads/). To send email notifications from a server, also install mutt. (e.g. [Ubuntu wiki](https://wiki.ubuntu.com/Mutt))

4. Install the python packages listed in [required.txt](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/required.txt) with `pip` or `pip3`:

    `pip3 install charset-normalizer json pandas python-decouple xml xmltodict`

5. Run the script:  `python3 emu_xml_to_json.py`

    - The newest file in your **.env** file's 'IN_PATH' is the default XML-input.
    - Alternatively, you can manually specify a different XML-input like so:

        `python3 emu_xml_to_json.py data_in/2021-08-08/sample.xml`

6. Output JSON, XML and log are zipped and emailed.
    See JSON output in **emu_to_json.json**, or check for errors in **xml_log_YYYYMMDD.txt**

## Input
### EMu XML Export
An XML file containing records exported from EMu as XML, with some or all EMu-fields listed in emu_fields.csv
- [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/2021-8-15/sample2.xml) of well-formed input
- [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/2021-8-8/sample_bad.xml) of input with a badly-encoded character

### emu_fields.csv ([example](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/mappings/h2i/emu_fields.csv))
A 5-column CSV that maps EMu-column-names to corresponding standard-term names, using the following columns:
- `emu` = EMu column-names
    - Exclude any "Ref" and "\_tab" suffixes here. (This should match the lowest-level tag name in the EMu XML.)
- `json_field` = corresponding h2i standard term names
- `repeatable` = blank or 'yes' to indicate if multiple values can be assigned to json_field
- `emu_group` = in the EMu export's 'Group' name, or the table or Reference column name 
    - Include the "Ref" and/or "\_tab" suffix (if any) for the corresponding `emu` field.
- `json_container` = the group name for a set of `json_fields` that should be nested together in the output JSON

### emu_conditions.csv ([example](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/mappings/h2i/emu_conditions.csv))
A 7-column CSV that defines logic for conditionally redacting or mapping rows in multi-value-tables to standard terms.
-  `if_field1` = the input EMu-field whose value defines a condition
-  `if_logic1` = the logical comparison for the condition (e.g. if the field "IS" or "IS NOT" equal to if_value1)
-  `if_value1` = the input value. 
    -  Use "NOT NULL" for "any non-blank input value"
-  `then_field` = the input EMu-field (if any) whose value should be transformed or redacted.
-  `json_field` = the output json_field that should be set (conditionally) to the value in `static_value`. 
    -  Use "NULL" to redact an output value from the `then_field`
-  `static_value` = the output value used if an input field matches conditions in the if_field1 & if_value1
-  `json_container` = the output field's group, if any

## Output
- [**emu_to_json.json**](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/sample_data_out/h2i_example_175440675964/data_out/emu_to_json_40672355.json) = Records as JSON objects, with EMu-fields/data as key/value pairs.
- [**emu_prepped.xml**](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/sample_data_out/h2i_example_175440675964/data_out/emu_prepped_40672355.xml) (optional) = XML with EMu column-names as xml-tags instead of xml-attributes
- [**xml_log_YYYY-MM-DD.txt**](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/sample_data_out/h2i_example_175440675964/log/xml_log_2022-09-12.txt) = Log of successful or failed output. 
- email notifications (currently requires mutt to send email, or gmail-only recipients)
    - Log-messages comprise the email-body
    - Output files are zipped and attached
