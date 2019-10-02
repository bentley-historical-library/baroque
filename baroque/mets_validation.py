import os
from lxml import etree

from .baroque_validator import BaroqueValidator

# Note: Some namespaces referenced in the example XML files are not used in the METS file. Unless I'm missing some, these are: fits, fn, rights, marc21 and  tcf.
namespaces = {
    'mets': 'http://www.loc.gov/METS/',
    'dc': 'http://purl.org/dc/elements/1.1',
    'aes': 'http://www.aes.org/audioObject',
    'ph': 'http://www.aes.org/processhistory',
    'mods': 'http://www.loc.gov/mods/v3'
}

class MetsValidator(BaroqueValidator):
    def __init__(self, project):
        validation = "mets"
        validator = self.validate_mets
        super().__init__(validation, validator, project)

    def check_tag_text(self, item_id, path_to_mets, tag, argument, value=None):
        if argument == "Is":
            if tag.text != value:
                self.error(
                    path_to_mets,
                    item_id,
                    tag.text + ' text does not equal ' + value + ' value in ' + tag.tag
                )

    def check_tag_attrib(self, item_id, path_to_mets, tag, argument, attribute, value=None):
        if argument == "Exists": # Does Not Exist, Is, Is Not, Contains, Does Not Contain, Is Greater Than, Is At Least, Is Less Than
            if attribute not in tag.attrib:
                self.error(
                    path_to_mets,
                    item_id,
                    attribute + ' attribute does not exist in ' + tag.tag
                )
        elif argument == "Is":
            if tag.attrib[attribute] != value:
                self.error(
                    path_to_mets,
                    item_id,
                    tag.attrib[attribute] + ' in ' + attribute + ' attribute does not equal ' + value + ' value in ' + tag.tag
                )

    def validate_mets_header(self, item_id, path_to_mets, tree):
        """
        Validates metsHdr section

        <mets:metsHdr CREATEDATE="2019-08-05T11:47:37.538-04:00">
            <mets:agent ROLE="OTHER">
                <mets:name>The MediaPreserve</mets:name>
            </mets:agent>
            <mets:agent ROLE="PRESERVATION" TYPE="ORGANIZATION">
                <mets:name>University of Michigan, Bentley Historical Library</mets:name>
            </mets:agent>
            <mets:agent ROLE="DISSEMINATOR" TYPE="ORGANIZATION">
                <mets:name>University of Michigan, Bentley Historical Library</mets:name>
            </mets:agent>
        </mets:metsHdr>"""
        
        if not tree.xpath('/mets:mets/mets:metsHdr', namespaces=namespaces):
            self.error(
                path_to_mets,
                item_id,
                'mets xml has no mets header'
            )
        
        # Check that metsHdr attribute CREATE DATE exists
        mets_header = tree.xpath("/mets:mets/mets:metsHdr", namespaces=namespaces)[0]
        self.check_tag_attrib(item_id, path_to_mets, mets_header, "Exists", "CREATEDATE")

        # Check that there are three agent tags
        agents = tree.xpath("/mets:mets/mets:metsHdr/mets:agent", namespaces=namespaces)
        if len(agents) != 3:
            self.error(
                path_to_mets,
                item_id,
                'mets header has ' + str(len(agents)) + ' agent tags'
            )

        # Check the MediaPreserve agent
        mediapreserve_agent = tree.xpath("/mets:mets/mets:metsHdr/mets:agent", namespaces=namespaces)[0]
        self.check_tag_attrib(item_id, path_to_mets, mediapreserve_agent, "Is", "ROLE", "OTHER") # Feels like I should check to see if this exists first

        mediapreserve_name = [name for name in mediapreserve_agent][0]
        self.check_tag_text(item_id, path_to_mets, mediapreserve_name, "Is", "The MediaPreserve")
        
        # Check the PRESERVATION Bentley agent
        bhl_preservation_agent = tree.xpath("/mets:mets/mets:metsHdr/mets:agent", namespaces=namespaces)[1]
        self.check_tag_attrib(item_id, path_to_mets, bhl_preservation_agent, "Is", "ROLE", "PRESERVATION")
        self.check_tag_attrib(item_id, path_to_mets, bhl_preservation_agent, "Is", "TYPE", "ORGANIZATION")

        bhl_preservation_name = [name for name in bhl_preservation_agent][0]
        self.check_tag_text(item_id, path_to_mets, bhl_preservation_name, "Is", "University of Michigan, Bentley Historical Library")

        # Check the DISSEMINATOR Bentley agent
        bhl_disseminator_agent = tree.xpath("/mets:mets/mets:metsHdr/mets:agent", namespaces=namespaces)[2]
        self.check_tag_attrib(item_id, path_to_mets, bhl_disseminator_agent, "Is", "ROLE", "DISSEMINATOR")
        self.check_tag_attrib(item_id, path_to_mets, bhl_disseminator_agent, "Is", "TYPE", "ORGANIZATION")

        bhl_disseminator_name = [name for name in bhl_disseminator_agent][0]
        self.check_tag_text(item_id, path_to_mets, bhl_disseminator_name, "Is", "University of Michigan, Bentley Historical Library")

    def validate_descriptive_metadata(self, item_id, path_to_mets, tree):
        """
        Validates dmdSec section"""
        
        if not tree.xpath('/mets:mets/mets:dmdSec', namespaces=namespaces):
            self.error(
                path_to_mets,
                item_id,
                'mets xml has no descriptive metadata'
            )

        descriptive_metadata = tree.xpath("/mets:mets/mets:dmdSec", namespaces=namespaces)[0]

    def validate_administrative_metadata(self, item_id, path_to_mets, tree):
        """
        Validates amdSec section"""
        
        if not tree.xpath('/mets:mets/mets:amdSec', namespaces=namespaces):
            self.error(
                path_to_mets,
                item_id,
                'mets xml has no administrative metadata'
            )

        administrative_metadata = tree.xpath("/mets:mets/mets:amdSec", namespaces=namespaces)[0]

    def validate_file_section(self, item_id, path_to_mets, tree):
        """
        Validates fileSec section"""

        if not tree.xpath('/mets:mets/mets:fileSec', namespaces=namespaces):
            self.error(
                path_to_mets,
                item_id,
                'mets xml has no file section'
            )

        administrative_metadata = tree.xpath("/mets:mets/mets:fileSec", namespaces=namespaces)[0]

    def validate_structural_map_section(self, item_id, path_to_mets, tree):
        """
        Validates structMap section"""

        if not tree.xpath('/mets:mets/mets:structMap', namespaces=namespaces):
            self.error(
                path_to_mets,
                item_id,
                'mets xml has no structural map section'
            )

        stuctural_map_section = tree.xpath("/mets:mets/mets:structMap", namespaces=namespaces)[0]

    def parse_item_mets(self, item):
        """
        Parses item METS"""

        path_to_item = item['path']
        item_id = item['id']
        mets = item['files']['xml'][0]
        path_to_mets = os.path.join(path_to_item, mets)
        tree = etree.parse(path_to_mets)
        
        return item_id, path_to_mets, tree

    def validate_mets(self):
        """ 
        Validates METS"""

        for item in self.project.items:
        
            # Assuming for now that validating directory and file structure would have picked this up
            if not item['files']['xml']:
                continue

            else:
                item_id, path_to_mets, tree = self.parse_item_mets(item)
            
                self.validate_mets_header(item_id, path_to_mets, tree)
                self.validate_descriptive_metadata(item_id, path_to_mets, tree)
                self.validate_administrative_metadata(item_id, path_to_mets, tree)
                self.validate_file_section(item_id, path_to_mets, tree)
                self.validate_structural_map_section(item_id, path_to_mets, tree)
