import os
from lxml import etree

def parse_mets_header(item_id, path_to_mets, tree):
    """
    Validates metsHdr"""
    namespaces = {
        'mets': 'http://www.loc.gov/METS/'
    }
    
    if not tree.xpath("/mets:mets/mets:metsHdr", namespaces=namespaces):
        errors =[
            "mets_validation",
            "requirement",
            path_to_mets,
            item_id,
            "mets xml has no mets header"
        ]
        print('SYSTEM ERROR:' + str(errors))
    
    else:
        mets_header = tree.xpath("/mets:mets/mets:metsHdr", namespaces=namespaces)[0]
        return mets_header

def parse_descriptive_metadata(item_id, path_to_mets, tree):
    """
    Validates dmdSec"""
    pass

def parse_administrative_metadata(item_id, path_to_mets, tree):
    """
    Validates amdSec"""
    pass

def parse_file_section(item_id, path_to_mets, tree):
    """
    Validates fileSec"""
    pass

def parse_structural_map_section(item_id, path_to_mets, tree):
    """
    Validates structMap"""
    pass

def parse_item_mets(item):
    path_to_item = item['path']
    item_id = item['id']
    mets = item['files']['xml'][0]
    path_to_mets = os.path.join(path_to_item, mets)
    tree = etree.parse(path_to_mets)
    
    return item_id, path_to_mets, tree

def validate_mets(BaroqueProject):
    """ 
    Validates METS"""
    for item in BaroqueProject.items:
    
        # Assuming for now that validating directory and file structure would have picked this up
        if not item['files']['xml']:
            continue

        item_id, path_to_mets, tree = parse_item_mets(item)
        
        parse_mets_header(item_id, path_to_mets, tree)
        parse_descriptive_metadata(item_id, path_to_mets, tree)
        parse_administrative_metadata(item_id, path_to_mets, tree)
        parse_file_section(item_id, path_to_mets, tree)
        parse_structural_map_section(item_id, path_to_mets, tree)
