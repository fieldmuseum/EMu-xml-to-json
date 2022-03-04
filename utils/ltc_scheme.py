'''
Setup Glom Specs for Latimer Core records
'''

def ltc_emu_accession() -> dict:
    '''
    Returns the Spec for Latimer Core terms in an EMu Accession record
    https://github.com/tdwg/cd/issues?q=is%3Aissue+label%3AClass%3AAddress+
    '''

    ltc_accession = {
        "CollectionDescriptionScheme": {
            "schemeName":None

        },
        "ObjectGroup": [
            {
                "collectionManagementSystem": None,
                "collectionName": None,
                "conditionsOfAccess": None,
                "currentStatus": None,
                "degreeOfEstablishment": None,

                "description": None,
                "discipline": None,
                "knownToContainTypes": None,
                "material": None,
                "objetType": None,
                "baseTypeOfCollection": None,
                "typeOfCollection": None,

                "period": None,                

                "preparationType": None,
                "preservationMethod": None,
                "preservationMode": None,

                "RecordLevel": {
                    "license": None,  # "https://creativecommons.org/publicdomain/zero/1.0/",
                    "PersonRoles": [
                        {
                            "Person": [
                                {
                                    "fullName": None,
                                    "Identifiers": [
                                        {
                                            "identifierType": "ORCID ID",
                                            "identifier": None
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "Address": {
                    "addressCountry": None,
                    "addressLocality": None,
                    "addressRegion": None,
                    "addressType": None,
                    "postalCode": None,
                    "postOfficeBoxNumber": None,
                    "streetAddress": None
                }
            }

            ]
        }

    return ltc_accession


def ltc_record_v1() -> dict:
    '''
    Returns the Spec for draft-1 standard terms in a Latimer Core record
    - nested Classes include Class-name AND Class-terms
    '''

    ltc_record = {
        "ObjectGroup": [
            {
                "collectionStartDate": None,
                # "thematicFocus": None,  # FKA "collectionStrength"
                
                "collectionManagementSystem": None,
                "collectionName": None,
                "conditionsOfAccess": None,
                "currentStatus": None,
                "degreeOfEstablishment": None,

                "description": None,
                "discipline": None,
                "knownToContainTypes": None,
                "material": None,
                "objetType": None,
                "baseTypeOfCollection": None,
                "typeOfCollection": None,

                "period": None,                

                "preparationType": None,
                "preservationMethod": None,
                "preservationMode": None,


                "CollectionDescriptionScheme": { # non-repeatable?
                    # "basisOfScheme": None,
                    # "distinctObjects": True,
                    "schemeName": None,
                    "SchemeMetric": [
                        {
                            "metricName": None,  # "ObjectQuantity"
                            "isMandatoryMetric": False
                        }
                    ],
                    "SchemeDimension": [
                        {
                            "dimensionName": None,  # "ObjectClassification"
                            "isMandatoryDimension": False,
                            "isRepeatable": True
                        }
                    ]
                },
                "OrganisationalUnit": { # non-repeatable?
                    "organisationalUnitAlternativeName": None,
                    "organisationalUnitDescription": None,
                    "organisationalUnitImmediateParentID": None,  # urn:uuid:a7f6e7ad-aa9d-457c-9f80-3521b975a2c5
                    "organisationalUnitName": None,
                    "organisationalUnitParentInstitutionID": None, # http://biocol.org/urn:lsid:biocol.org:col:34795
                    "organisationalUnitType": None,

                    "Address": {
                        "addressCountry": None,
                        "addressLocality": None,
                        "addressRegion": None,
                        "addressType": None,
                        "postalCode": None,
                        "postOfficeBoxNumber": None,
                        "streetAddress": None
                    }
                },

                "ObjectClassification": {
                    "objectClassificationLevel": None,
                    "objectClassificationName": None,
                    "objectClassificationParent": None
                },

                "RecordLevel": {
                    "collectionDescriptionPID": None,
                    "derivedCollection": None,
                    "license": None,  # "https://creativecommons.org/publicdomain/zero/1.0/",
                    "rightsHolder": None,
                    "recordRights": None,

                    "PersonRoles": [
                        {
                            "Person": [
                                {
                                    "additionalName": None,
                                    "familyName": None,
                                    "fullName": None,
                                    "givenName": None,

                                    "Identifiers": [
                                        {
                                            "identifier": None,
                                            "identifierSource": None,  # "ORCID",
                                            "identifierType": None  # "ORCID ID"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },

                "Taxon": [
                    {
                        "kingdom": None,
                        "phylum": None,
                        "class": None,
                        "genus": None,
                        "scientificName": None,
                        "taxonRank": None
                    }
                ],

                "GeographicOrigin": [
                    {
                        "continent": None,
                        "locality": None,
                        "region": None,
                        "salinityType": None,
                        "waterBody": None,
                        "waterBodyType": None,
                        "MeasurementOrFact": [
                            {
                                "measurementType": None, # ObjectQuantity
                                "measurementValue": None,
                                "measurementUnit": None
                            }
                        ]
                    }
                ],
                "GeologicalContext": [
                    {
                        "bed": None,
                        "earliestAgeOrLowestStage": None,
                        "earliestEonOrLowestEonothem": None,
                        "earliestEpochOrLowestSeries": None,
                        "earliestEraOrLowestErathem": None,
                        "earliestPeriodOrLowestSystem": None,
                        "formation": None,
                        "group": None,
                        "latestAgeOrLowestStage": None,
                        "latestEonOrLowestEonothem": None,
                        "latestEpochOrLowestSeries": None,
                        "latestEraOrLowestErathem": None,
                        "latestPeriodOrLowestSystem": None,
                        "MeasurementOrFact": [
                            {
                                "measurementType": None,
                                "measurementValue": None,
                                "measurementUnit": None
                            }
                        ]
                    }
                ],

                "TemporalCoverage": [
                    {
                        "temporalCoverageEndDate": None,
                        "temporalCoverageStartDate": None,
                        "temporalCoverageType": None
                    }
                ],

                "MeasurementOrFact": [
                    {
                        "measurementAccuracy": None,
                        "measurementDerivation": None,
                        "measurementDeterminedDate": None,
                        "measurementFactText": None,
                        "measurementMethod": None,
                        "measurementRemarks": None,
                        "measurementType": None, # ObjectQuantity
                        "measurementUnit": None,
                        "measurementValue": None
                    }
                ],

                "Reference": [
                    {
                        "referenceDetails": None,
                        "referenceText": None,
                        "referenceType": None,
                        "resourceURI": None
                    }
                ],

                "StorageLocation": [

                ]
            }

        ]
    }

    return ltc_record


def ltc_record_v2() -> dict:
    '''
    Returns the Spec for draft-1 standard terms in a Latimer Core record
    - Nested Classes only include Class-name, NOT Class-terms
    - This might handle LTC changes better over time.
    '''

    ltc_record = {
        "ObjectGroup": [
            {

                "CollectionDescriptionScheme": { # non-repeatable?
                    "SchemeMetric": None,
                    "SchemeDimension": None
                },

                "OrganisationalUnit": { # non-repeatable?
                    "Address": None
                },

                "ObjectClassification": None,
                "RecordLevel": {
                    "PersonRoles": [
                        {
                            "Person": [
                                {
                                    "Identifiers": None
                                }
                            ]
                        }
                    ]
                },

                "Taxon": None,

                "GeographicOrigin": [
                    {
                        "MeasurementOrFact": None
                    }
                ],
                "GeologicalContext": [
                    {
                        "MeasurementOrFact": None
                    }
                ],

                "TemporalCoverage": [
                    {
                        "MesurementOrFact": None
                    }
                ],

                "MeasurementOrFact": None,

                "Reference": None,

                "StorageLocation": None

                
            }

        ]
    }

    return ltc_record