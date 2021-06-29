# EMu XML-to-JSON converter

## How to setup & use

1. Clone this repo

2. Set local environment variables by adding a text file named `.env` in the root of the repo. Open it and add the following:
    `INPUT_PATH='/path/to/xml-export'`
    `INPUT_XML='filename.xml'`
    `OUTPUT_PATH='/path/to/json-output'`

    (More [info here](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) if needed.)

3. Install [Python 3.9 or later](https://www.python.org/downloads/)

4. Install these python packages (with `pip` or `pip3`):
    `pip3 install json lxml pandas python-decouple xml xmltodict`

5. Run the script:
    `python3 emu_xml_to_json.py`

## Input
- An XML file containing records exported from EMu as XML

## Output
- `emu_to_json.json` = Records as JSON objects, with EMu-fields/data as key/value pairs.
- `emu_xml.xml` (optional) = XML with EMu column-names as xml-tags instead of xml-attributes
