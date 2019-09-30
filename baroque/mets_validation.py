import os
from lxml import etree

"""
Note: Some namespaces referenced in the example XML files are not used in the METS file.
Unless I'm mission some, these are: fits, fn, rights, marc21 and  tcf."""

def parse_mets_header(item_id, path_to_mets, tree):
    """
    Parses metsHdr"""
    
    namespaces = {
        'mets': 'http://www.loc.gov/METS/'
    }
    
    if not tree.xpath('/mets:mets/mets:metsHdr', namespaces=namespaces):
        errors =[
            'mets_validation',
            'requirement',
            path_to_mets,
            item_id,
            'mets xml has no mets header'
        ]
        print('SYSTEM ERROR:' + str(errors))
    
    else:
        mets_header = tree.xpath("/mets:mets/mets:metsHdr", namespaces=namespaces)[0]
        return mets_header

def parse_descriptive_metadata(item_id, path_to_mets, tree):
    """
    Parses dmdSec"""
    
    namespaces = {
        'mets': 'http://www.loc.gov/METS/',
        'dc': 'http://purl.org/dc/elements/1.1'
    }

    if not tree.xpath('/mets:mets/mets:dmdSec', namespaces=namespaces):
        errors =[
            'mets_validation',
            'requirement',
            path_to_mets,
            item_id,
            'mets xml has no descriptive metadata'
        ]
        print('SYSTEM ERROR:' + str(errors))

    else:
        descriptive_metadata = tree.xpath("/mets:mets/mets:dmdSec", namespaces=namespaces)[0]
        return descriptive_metadata

def parse_administrative_metadata(item_id, path_to_mets, tree):
    """
    Parses amdSec"""
    
    namespaces = {
        'mets': 'http://www.loc.gov/METS/',
        'aes': 'http://www.aes.org/audioObject',
        'ph': 'http://www.aes.org/processhistory',
        'mods': 'http://www.loc.gov/mods/v3',
    }

    if not tree.xpath('/mets:mets/mets:amdSec', namespaces=namespaces):
        errors =[
            'mets_validation',
            'requirement',
            path_to_mets,
            item_id,
            'mets xml has no administrative metadata'
        ]
        print('SYSTEM ERROR:' + str(errors))

    else:
        administrative_metadata = tree.xpath("/mets:mets/mets:amdSec", namespaces=namespaces)[0]
        return administrative_metadata

def parse_file_section(item_id, path_to_mets, tree):
    """
    Validates fileSec"""
    
    namespaces = {
        'mets': 'http://www.loc.gov/METS/'
    }

    if not tree.xpath('/mets:mets/mets:fileSec', namespaces=namespaces):
        errors =[
            'mets_validation',
            'requirement',
            path_to_mets,
            item_id,
            'mets xml has no file section'
        ]
        print('SYSTEM ERROR:' + str(errors))

    else:
        administrative_metadata = tree.xpath("/mets:mets/mets:fileSec", namespaces=namespaces)[0]
        return administrative_metadata

def parse_structural_map_section(item_id, path_to_mets, tree):
    """
    Parses structMap"""
    
    namespaces = {
        'mets': 'http://www.loc.gov/METS/'
    }

    if not tree.xpath('/mets:mets/mets:structMap', namespaces=namespaces):
        errors =[
            'mets_validation',
            'requirement',
            path_to_mets,
            item_id,
            'mets xml has no structural map section'
        ]
        print('SYSTEM ERROR:' + str(errors))

    else:
        administrative_metadata = tree.xpath("/mets:mets/mets:structMap", namespaces=namespaces)[0]
        return administrative_metadata

def parse_item_mets(item):
    """
    Parses item METS"""

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

        else:
            item_id, path_to_mets, tree = parse_item_mets(item)
        
            mets_header = parse_mets_header(item_id, path_to_mets, tree)
            descriptive_metadata = parse_descriptive_metadata(item_id, path_to_mets, tree)
            administrative_metadata = parse_administrative_metadata(item_id, path_to_mets, tree)
            file_section = parse_file_section(item_id, path_to_mets, tree)
            structural_map_section = parse_structural_map_section(item_id, path_to_mets, tree)
