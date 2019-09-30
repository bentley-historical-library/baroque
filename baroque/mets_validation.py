import os
from lxml import etree
from pprint import pprint

def parse_item_mets(item):
    path = item['path']

    # Assuming for now that validating directory and file structure would have picked this up
    if not item['files']['xml']:
        return None
    
    else:
        mets = item['files']['xml'][0]
        tree = etree.parse(os.path.join(path, mets))
        return tree

def validate_mets(BaroqueProject):
    """ 
    Validates METS"""
    for item in BaroqueProject.items:
        tree = parse_item_mets(item)
