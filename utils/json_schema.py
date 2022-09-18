'''Utils for retrieving and validating against a JSON schema (e.g. for Latimer Core)'''

import json, jsonschema, requests

def get_json_schema(schema_url:str='https://raw.githubusercontent.com/tdwg/cd/review/standard/json-schema/record-level.json'):
    '''
    Given the URL for a schema (default being Latimer Core [draft] JSON schema, via its RecordLevel class), 
    return a JSON schema as a python dictionary
    '''

    url = requests.get(schema_url)

    if url.status_code == 200:
        schema = json.loads(url.text)

        if schema is not None:    
            return schema
        
        else: Exception(f'Error -- URL does not seem to return a valid JSON string -- Check {schema_url}')
    
    else: Exception(f'Error -- URL returned status code {url.status_code} -- Check {schema_url}')


def validate_json_schema(input_data, schema):
    '''Return "Valid" or error explaining invalidity input data against a given JSON schema'''

    validation_response = None

    validation_response = jsonschema.validate(instance=input_data, schema=schema)

    if validation_response is None:
        return 'Valid'
    
    else: return validation_response
