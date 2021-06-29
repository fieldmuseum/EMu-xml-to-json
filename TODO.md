# EMu XML-to-JSON converter

## To do

1. Tie in EMu exports
    - Setup daily/weekly cron to run script; 
        - (if Export folder is not empty, get most recent export)
    - Or listen for notification email (sent after export runs)

2. Setup Python env 
    - paths to input & output files

3. Install Python on Boojum

4. Include step for XML-validation.
In meantime, validate XML outside of script -- e.g.:
- ['Scholarly XML' VSCode add-on](https://marketplace.visualstudio.com/items?itemName=raffazizzi.sxml)
- [Online XML validator](https://www.w3schools.com/xml/xml_validator.asp)
Warning -  avoid online-validators for sensitive data.