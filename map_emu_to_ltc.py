'''Map an EMu XML record-set to Latimer Core'''

'''Parse an XML export of EMu Accession records to generate Latimer Core records'''
import argparse, csv, datetime, json, os, re, sys, time
import glom as glom
from bs4 import BeautifulSoup
from inspect import getmembers, isfunction
import utils.xml_parse as xml_parse
import utils.ltc_class_specs as ltc_classes
import utils.ltc_scheme as ltc_scheme



def get_ltc_values(ltc_node: dict, soup: BeautifulSoup) -> dict:
    '''Scrape Drupal Staff page and return a Dato 'ltc' model'''
    record = None

    # Get the LTC scheme 
    ltc_record = ltc_scheme.ltc_record_v2()

    # Get the class specs for that LTC scheme
    class_function_list = []
    class_names_list = []
    for class_function in getmembers(ltc_classes):
        if isfunction(class_function[1]):
            class_function_list.append(class_function[0])
            class_names_list.append(class_function[1])


    # Fill in terms for each class in the LTC scheme / more dynamically
    if ltc_record['ObjectGroup'] is not None:
        for term in ltc_record['ObjectGroup'][0]:
            
            if term in class_names_list:
                term = class_function_list[class_names_list.index(term)]
                # ltc_record['ObjectGroup'][0][object_group] = classes[0][1]


    # Map EMu values to ltc-fields
    
    # run emu_sml_parse here?

    # &/or try glom 
    # glom.assign(ltc_record, 'ObjectGroup.' + ltc_classes., None)


    # # Dato Item-type for page
    # NOTE - exclude for updates (vs inserts)
    # ltc = dato_fields.assign_model_block_item_type_info(ltc, "ltcion")

    # Drupal URL
    canonical_link = xml_parse.get_attrib_value_from_soup(soup, 'link[rel="canonical"]', 'href')
    print(canonical_link)
    if canonical_link is not None and canonical_link != "https://www.fieldmuseum.org/ltcions":
        glom.assign(ltc, "attributes.drupal_url", canonical_link)
    else:
        print("Missing Canonical URL - " + ltc_node['Nid'])


    tag_list = []

    # Research Area
    research_area = ltc_node['ResearchArea']

    if research_area is not None and len(research_area) > 0:

        # clean Drupal's 'First valueSecond value' bad export format to ['First value', 'Second value']
        research_area = re.sub(r'([a-z]{1})([A-Z]{1})+', r'\1|\2', research_area)
        research_area = research_area.split(sep = "|")   

        for area in research_area:

            res_prepped = ""  # datoapi.dato_api_get_record_by_field_value(
            #     "tag", 
            #     area, # ltc_node['Science Focus'],
            #     "tag"
            # )

            if res_prepped is not None and len(res_prepped['data']) > 0:
                tag_list.append(res_prepped['data'][0]['id'])
            else:
                print('No matching tags for Research Area: ' + area)

    glom.assign(ltc, 'attributes.drupal_research_area', ' | '.join(research_area))
    

    # Science Focus
    sci_focus = ltc_node['ScienceFocus'] 

    if sci_focus is not None and len(sci_focus) > 0:

        # sci_focus_tag_list = []

        # clean Drupal's 'First valueSecond value' bad export format to ['First value', 'Second value']
        sci_focus = re.sub(r'([a-z]{1})([A-Z]{1})+', r'\1|\2', sci_focus)
        sci_focus = sci_focus.split(sep = "|")   

        for focus in sci_focus:

            sci_prepped = "" # datoapi.dato_api_get_record_by_field_value(
            #     "tag", 
            #     focus, # ltc_node['Science Focus'],
            #     "tag"
            # )

            if sci_prepped is not None and len(sci_prepped['data']) > 0:
                tag_list.append(sci_prepped['data'][0]['id'])
            else:
                print('No matching tags for Science Focus: ' + focus)

    glom.assign(ltc, 'attributes.drupal_science_focus', ' | '.join(sci_focus))


    # Topic
    topics = ltc_node['Topic']

    if topics is not None and len(topics) > 0:

        # topics_tag_list = []

        # clean Drupal's 'First valueSecond value' bad export format to ['First value', 'Second value']
        topics = re.sub(r'([a-z]{1})([A-Z]{1})+', r'\1|\2', topics)
        topics = topics.split(sep = "|")  

        for topic in topics:

            topic_prepped = ""  # datoapi.dato_api_get_record_by_field_value(
            #     "tag", 
            #     topic,
            #     "tag"
            # )

            if topic_prepped is not None and len(topic_prepped['data']) > 0:
                tag_list.append(topic_prepped['data'][0]['id'])
            else:
                print('No matching tags for Topic: ' + topic)

    
    glom.assign(ltc, 'attributes.drupal_topics', ' | '.join(topics))


    if len(tag_list) > 0:
        glom.assign(ltc, "attributes.tags", tag_list)


    # Set up record with the basic attributes
    record = {}
    record['data'] = ltc

    return record


def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="CSV with Drupal ltcion node IDs, and Science/Research/Topics data")
    parser.add_argument("output_path", help="Output path (with trailing '/') for output JSON & logs")
    parser.add_argument("publish", help="Publish updated Dato records? Yes/No")
    args = parser.parse_args()    


    # Import the staff-export CSV
    emu_xml = args.input_csv # 'data/sidebar/d7_exports/drupal-main-menu-export.csv'
    
    # # # # # IMPORT EMu XML file: # # # #
    # ltc_export = utils_csv.rows(emu_xml)


    # Test with smaller subset
    # ltc_export = ltc_export[0:10]


    # Scrape ltc records
    exh_records = []
    import_log = []

 
    for ltc_node in ltc_export:

        # Parse dato-fields from text row
        exh_nid = str(ltc_node['Nid'])
        exh_title = str(ltc_node['Title'])

        if ltc_node['Published status'] == 'No':

            import_message = [f'Skipping unpublished Drupal record for Nid: {exh_nid} | Title: {exh_title}']
        
        else:

            time.sleep(2)

            # soup = xml_scrape.get_page_soup(url = "https://www.fieldmuseum.org/node/" + exh_nid)
            soup = xml_parse.get_soup_from_xml()

            record = get_ltc_values(ltc_node, soup)

            if record is None or len(exh_nid) < 1:
                import_message = [f'Missing Nid or Empty record | Nid: {exh_nid} | Title: {exh_title}']
            
            else:
                exh_records.append(record)

                record_in_dato = ""  # datoapi.dato_api_get_record_matching_nid(
                    # exh_nid,
                    # headers=None,
                    # record_type="ltcion",
                    # record_field="nid",
                    # record_version = "current"
                    # )
                
                if not record_in_dato["data"] or len(record_in_dato["data"]) == 0:
                    import_message = [f'No Dato record found for Nid: {exh_nid} | Title: {exh_title}']
                    # # If there's no record, do a new insert
                    # datoapi.dato_api_create_record(record)
                    # import_message = [f"Added record | Nid: {exh_nid} | Title: {exh_title}"]
                
                else:
                    page_id = record_in_dato['data'][0]['id']

                    record['data']['id'] = page_id
                    # glom.delete(record, "data.relationships")
                    
                    # datoapi.dato_api_update_record(record, page_id)                
                    # import_message = [f"Updated existing record in Dato -- page-id: {page_id} | Nid: {exh_nid} | Title: {exh_title}"]

                    # if args.publish == 'Yes':
                    #     datoapi.dato_api_publish_record(page_id)

        print(import_message)
        import_log.append(import_message)
  
        
        time.sleep(1)


    # Export scraped ltc records
    if len(exh_records) > 0:

        output_path = args.output_path # "data/ltc/dato_scraped
        today = datetime.date.today().strftime("%Y%m%d")
        
        # Check if dir exists, and if not, make it
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        json_filename = 'exh_tags_parsed_' + today + '.json'
        with open(output_path + json_filename, 'w') as file_output:
            json.dump(exh_records, file_output, indent=True, ensure_ascii=False)


    # Write import_log to csv
    if len(import_log) > 0:

        input_file = re.sub(r".*/|\..*", "", args.input_csv)
        log_output_file = input_file + "_" + today + "_import.log"

        with open(output_path + log_output_file, encoding='utf-8', mode='w') as log_output:
            write = csv.writer(log_output)
            write.writerows(import_log)


if __name__ == '__main__':
    main()
