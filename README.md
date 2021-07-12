# EMu XML-to-JSON converter

## How to setup & use

### In EMu:
1. Export a set of records as XML.  (See [TODO.md](https://github.com/magpiedin/EMu-xml-to-json/blob/main/TODO.md) for xml-validation tips)

2. Setup a CSV named "abcd_h2i_emu.csv" with EMu-column-names in the 1st column, and corresponding standard-term names in the 2nd column.  [See example in 'Input' section](#input)


### Not in EMu:

1. Clone this repo

2. Set local environment variables by adding a text file named `.env` in the root of the repo. Open it and add variables following the [`.env.example`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/.env.example) file.

(More [info here](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) if needed.)

3. Install [Python 3.9 or later](https://www.python.org/downloads/)

4. Install the python packages listed in [`required.txt`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/required.txt) (with `pip` or `pip3`):

    `pip3 install charset-normalizer json pandas python-decouple xml xmltodict`

5. Run the script:

    `python3 emu_xml_to_json.py`

6. See JSON output in `emu_to_json.json`, or error log in `xml_log_YYYYMMDD.txt`

## Input
- EMu XML Export - An XML file containing records exported from EMu as XML
    - [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/sample.xml)
- `abcd_h2i_emu.csv` EMu/Standards mapping doc - A 2-column CSV listing EMu column-names in the 1st column and corresponding standard terms in the 2nd column.
    - [example here](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_in/abcd_h2i_emu.csv)

## Output
- [`emu_to_json.json`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_out/emu_to_json.json) = Records as JSON objects, with EMu-fields/data as key/value pairs.
- [`emu_xml.xml`](https://github.com/fieldmuseum/EMu-xml-to-json/blob/main/data_out/emu_xml.xml) (optional) = XML with EMu column-names as xml-tags instead of xml-attributes
