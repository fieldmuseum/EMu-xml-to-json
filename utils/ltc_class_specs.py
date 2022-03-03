'''
Setup Glom Specs for Latimer Core Classes
-- Manual copies from the Class Index '1st draft properties worksheet' tab for now:
https://docs.google.com/spreadsheets/d/1w8DMgUwl7tf-9AXQOpT6IRQeMuUbxUZlJwQinrtUvAs/edit#gid=478678659

TODO - Reference the classes/terms/versions more dynamically
'''

def ltc_address() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the Address Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AAddress+
    '''
    class_name = "Address"

    class_terms = {
        "addressCountry": None,
        "addressLocality": None,
        "addressRegion": None,
        "addressType": None,
        "postalCode": None,
        "postOfficeBoxNumber": None,
        "streetAddress": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_chronometric_age() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the ChronometricAge Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AChronometricAge+
    '''
    class_name = "ChronometricAge"

    class_terms = {
        "chronometricAgeProtocol": None,
        "chronometricAgeRemarks": None,
        "chronometricAgeUncertaintyInYears": None,
        "earliestChronometricAge": None,
        "earliestChronometricAgeReferenceSystem": None,
        "latestChronometricAge": None,
        "latestChronometricAgeReferenceSystem": None,
        "verbatimChronometricAge": None

    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_collection_description_scheme() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the CollectionDescriptionScheme Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3ACollectionDescriptionScheme+
    '''

    class_name = "CollectionDescriptionScheme"

    class_terms = {
        "schemeName": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_collection_history() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the CollectionHistory Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3ACollectionHistory+
    '''
    class_name = "CollectionHistory"

    class_terms = {
        "status": None,
        "statusChangeReason": None,
        "statusEndDate": None,
        "statusStartDate": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_contact_detail() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the ContactDetail Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AContactDetail+
    '''

    class_name = "ContactDetail"

    class_terms = {
        "contactDetailCategory": None,
        "contactDetailType": None,
        "contactDetailValue": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_geographic_origin() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the GeographicOrigin Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AGeographicOrigin+
    '''
    class_name = "ContactDetail"
    
    class_terms = {
        "continent": None,
        "locality": None,
        "region": None,
        "salinityType": None,
        "waterBody": None,
        "waterBodyType": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_geologic_context() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the GeologicContext Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AGeographicOrigin+
    '''

    class_name = "GeologicContext"

    class_terms = {
        "bed": None,
        "earliestAgeOrLowestStage": None,
        "earliestEonOrLowestEonothem": None,
        "earliestEpochOrLowestSeries": None,
        "earliestEraOrLowestErathem": None,
        "earliestPeriodOrLowestSystem": None,
        "formation": None,
        "group": None,
        "latestAgeOrHighestStage": None,
        "latestEonOrHighestEonothem": None,
        "latestEpochOrHighestSeries": None,
        "latestEraOrHighestErathem": None,
        "latestPeriodOrHighestSystem": None,
        "member": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_identifier() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the Identifier Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AIdentifier+
    '''

    class_name = "Identifier"

    class_terms = {
        "identifier": None,
        "identifierSource": None,
        "identifierType": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_measurement_or_fact() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the MeasurementOrFact Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AMeasurementOrFact+
    '''

    class_name = "MeasurementOrFact"

    class_terms = {
        "measurementAccuracy": None,
        "measurementDerivation": None,
        "measurementDeterminedDate": None,
        "measurementFactText": None,
        "measurementMethod": None,
        "measurementRemarks": None,
        "measurementType": None,
        "measurementUnit": None,
        "measurementValue": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_object_classification() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the ObjectClassification Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AObjectClassification+
    '''

    class_name = "ObjectClassification"

    class_terms = {
        "objectClassificationLevel": None,
        "objectClassificationName": None,
        "objectClassificationParent": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_object_group() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the ObjectGroup Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AObjectGroup+
    '''

    class_name = "ObjectGroup"

    class_terms = {
        "collectionManagementSystem": None,
        "collectionName": None,
        "conditionsOfAccess": None,
        "currentStatus": None,
        "degreeOfEstablishment": None,
        "description": None,
        "discipline": None,
        "knownToContainTypes": None,
        "material": None,
        "objectType": None,
        "baseTypeOfCollection": None,
        "period": None,
        "preparationType": None,
        "preservationMethod": None,
        "preservationMode": None,
        "typeOfCollection": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_organisational_unit() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the OrganisationalUnit Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AOrganisationalUnit+
    '''

    class_name = "OrganisationalUnit"

    class_terms = {
        "organisationalUnitName": None,
        "organisationalUnitType": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_person() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the Person Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3APerson+
    '''

    class_name = "Person"

    class_terms = {
        "additionalName": None,
        "familyName": None,
        "fullName": None,
        "givenName": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_person_role() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the PersonRole Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3APersonRole+
    '''

    class_name = "PersonRoles"

    class_terms = {
        "endedAtTime": None,
        "role": None,
        "startedAtTime": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_record_level() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the RecordLevel Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3ARecordLevel+
    '''

    class_name = "RecordLevel"

    class_terms = {
        "derivedCollection": None,
        "license": None,
        "PID": None,
        "recordRights": None,
        "rightsHolder": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_reference() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the Reference Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AReference+
    '''

    class_name = "Reference"

    class_terms = {
        "referenceDetails": None,
        "referenceText": None,
        "referenceType": None,
        "resourceURI": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_resource_relationship() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the ResourceRelationship Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AResourceRelationship+
    '''

    class_name = "ResourceRelationship"

    class_terms = {
        "relatedResourceID": None,
        "relatedResourceName": None,
        "relationshipAccordingTo": None,
        "relationshipEstablishedDate": None,
        "relationshipOfResource": None,
        "relationshipRemarks": None,
        "resourceID": None,
        "resourceRelationshipID": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_storage_location() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the StorageLocation Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AStorageLocation+
    '''

    class_name = "StorageLocation"

    class_terms = {
        "locationName": None,
        "locationType": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_taxon() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the Taxon Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3ATaxon+
    '''

    class_name = "StorageLocation"

    class_terms = {
        "genus": None,
        "kingdom": None,
        "scientificName": None,
        "taxonRank": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}


def ltc_temporal_coverage() -> dict:
    '''
    Returns the Spec for Latimer Core terms in the TemporalCoverage Class
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3ATemporalCoverage+
    '''

    class_name = "TemporalCoverage"

    class_terms = {
        "temporalCoverageEndDate": None,
        "temporalCoverageStartDate": None,
        "temporalCoverageType": None
    }

    return {'class_name':class_name, 'class_terms':class_terms}