## [Darwin Core properties](https://dwc.tdwg.org/list/)
| emu | json_field | uri_iri | description |
|---|---|---|---|
| irn | dwc:recordNumber | 	http://rs.tdwg.org/dwc/terms/recordNumber | |
| esites_irn | dwc:locationID | http://rs.tdwg.org/dwc/terms/locationID | |
| PolContinent | dwc:continent | http://rs.tdwg.org/dwc/terms/continent | |
| PolPD1 | dwc:country |	http://rs.tdwg.org/dwc/terms/country | |
| PolPD2 | dwc:stateProvince | http://rs.tdwg.org/dwc/terms/stateProvince | |
| PolPD3 | dwc:county |	http://rs.tdwg.org/dwc/terms/county | |
| DarGlobalUniqueIdentifier | dwc:occurrenceID | http://rs.tdwg.org/dwc/terms/occurrenceID | |
| AccLocality | dwc:locality | http://rs.tdwg.org/dwc/terms/locality | |
| ColCollectionMethods_tab | dwc:samplingProtocol | http://rs.tdwg.org/dwc/iri/samplingProtocol | |
| AccCollectorRef_tab_NamFullName | dwc:recordedBy | http://rs.tdwg.org/dwc/iri/recordedBy | For most collections items this is the collector. |

## [Audubon Core properties](https://ac.tdwg.org/termlist/)
| emu | json_field | uri_iri | description |
|---|---|---|---|
| AudAccessURI | ac:accessURI | https://ac.tdwg.org/termlist/#ac_accessURI |

## [Dublin Core properties](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
| emu | json_field | uri_iri | description |
|---|---|---|---|
| AudIdentifier | dc:identifier | http://purl.org/dc/terms/identifier |
| NamExternalReferences_tab | dc:identifier | http://purl.org/dc/terms/identifier |
| AccAccessionDescription | dc:description | http://purl.org/dc/terms/description |

## [Latimer Core properties](https://github.com/tdwg/cd/issues)
| emu | json_field | uri_iri | description |
|---|---|---|---|
| AccCount | ltc:measurementValue | https://github.com/tdwg/cd/issues/292 |
| NamFullName | abltc:fullName | https://github.com/tdwg/cd/issues/308 |
| AccDateAccessioned | ltc:temporalCoverageStartDate | https://github.com/tdwg/cd/issues/68 |
| AccAccessionNo | ltc:identifier | https://github.com/tdwg/cd/issues/129 |
| AccCatalogueNo | ltc:identifier | https://github.com/tdwg/cd/issues/129 |
| DesEthnicGroupSubgroup | ltc:culturalAffiliation | https://github.com/tdwg/cd/issues/71 |
| AttPeriod | ltc:period | https://github.com/tdwg/cd/issues/259 |
| PolPopn | ltc:municipality | https://github.com/tdwg/cd/issues/143 |
| ColDateVisitedFrom | ltc:temporalCoverageStartDate | https://github.com/tdwg/cd/issues/68 |
| ColDateVisitedTo | ltc:temporalCoverageEndDate | https://github.com/tdwg/cd/issues/69 |
| AccCatalogue | ltc:organisationalUnitName | https://github.com/tdwg/cd/issues/198 |

## fmnh specific properties
| emu | json_field | uri_iri | description |
|---|---|---|---|
| ebiblio_irn | fmnh:referenceID | | Bibliographic reference id in FMNH collections management system |
| ebiblio_SummaryData | fmnh:reference | | Bibliographic reference summary. |
| AudCitation | fmnh:citation | | Preferred multimedia asset citation string |
| LocExhibitLocationRef_irn | fmnh:onExhibitOnSite fmnh:onExhibitOnSiteID | | A numeric ID or "True" value in these fields indicates that the item is on display at FMNH |
| LocTemporaryLocationRef_irn | fmnh:onExhibitOffSite fmnh:onExhibitOffSiteID | | A numeric ID or "True" value in these fields indicates that the item is on display but NOT at FMNH |
