'''Utility functions for parsing or scraping XML'''
import requests, os, re, glom
from bs4 import BeautifulSoup


def get_soup_from_xml(xml_file: str, encoding='UTF8') -> BeautifulSoup:
    '''Returns BeautifulSoup for an XML file'''
    # r = requests.get(url)
    # encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    # parser = 'html.parser'
    # soup = BeautifulSoup(r.content, parser, from_encoding=encoding)
    with open(xml_file, "r") as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        soup = BeautifulSoup(content, "lxml", from_encoding=encoding)
    
    return soup

def get_html_from_soup(soup: BeautifulSoup, selector: str) -> list:
    '''Returns a list of HTML tags given a particular CSS selector pattern'''
    html = soup.select(selector)
    return html

def get_text_from_soup(soup: BeautifulSoup, selector: str) -> str:
    '''Returns a text string, given a particular CSS selector pattern'''
    html = soup.select(selector)
    if len(html) > 0:
        return html[0].get_text()

def get_multi_text_from_soup(soup: BeautifulSoup, selector: str) -> list:
    '''Returns a text string, given a particular CSS selector pattern'''
    html = soup.select(selector)
    html_set = []
    for row in html:
        html_set.append(row.get_text().strip())
    return html_set

def get_attrib_value_from_soup(soup: BeautifulSoup, selector: str, attribute: str) -> str:
    '''Returns a string for a particular HTML attribute'''
    # if dom.xpath(xpath):
    if soup.select(selector):
        attribute_value = soup.select_one(selector)[attribute]
        return attribute_value.strip()

def get_nested_fields(dom: str, nested_fields_xpath: dict) -> str:
    '''Returns nested fields from the dom, in original order'''

    # TODO Make a table of actual_nest_fields / values
    nested_fields_values = dom.xpath(nested_fields_xpath.values)
    nested_fields = []

    # Match Dato-fieldnames (keys)
    for value in nested_fields_values:
        for key, val in nested_fields_xpath.items():
            if value == val:
                nested_field = key
                nested_fields.append(nested_field)

    content = zip(nested_fields, nested_fields_values)

    # TODO: For each nested_field, add rest of required dato-model-fields

    return content