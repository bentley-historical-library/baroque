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

    def check_tag_text(self, tag, argument, value=None):
        if argument == "Is":
            if tag.text != value:
                self.error(
                    self.path_to_mets,
                    self.item_id,
                    tag.text + ' text does not equal ' + value + ' value in ' + tag.tag
                )

    def check_tag_attrib(self, tag, argument, attribute, value=None):
        if argument == "Exists": # Does Not Exist, Is, Is Not, Contains, Does Not Contain, Is Greater Than, Is At Least, Is Less Than
            if attribute not in tag.attrib:
                self.error(
                    self.path_to_mets,
                    self.item_id,
                    attribute + ' attribute does not exist in ' + tag.tag
                )
        elif argument == "Is":
            if tag.attrib[attribute] != value:
                self.error(
                    self.path_to_mets,
                    self.item_id,
                    tag.attrib[attribute] + ' in ' + attribute + ' attribute does not equal ' + value + ' value in ' + tag.tag
                )

    def validate_mets_header(self):
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
        
        mets_header = self.tree.xpath("/mets:mets/mets:metsHdr", namespaces=namespaces)

        if not mets_header:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no mets header'
            )
        
        else:
            # Check that metsHdr attribute CREATE DATE exists
            mets_header = mets_header[0]
            self.check_tag_attrib(mets_header, "Exists", "CREATEDATE")

            # Check that there are three agent tags
            agents = mets_header.xpath("./mets:agent", namespaces=namespaces)
            if len(agents) != 3:
                self.error(
                    self.path_to_mets,
                    self.item_id,
                    'mets header has ' + str(len(agents)) + ' agent tags'
                )

            # Check the MediaPreserve agent
            mediapreserve_agent = agents[0]
            self.check_tag_attrib(mediapreserve_agent, "Is", "ROLE", "OTHER") # Feels like I should check to see if this exists first

            mediapreserve_name = [name for name in mediapreserve_agent][0]
            self.check_tag_text(mediapreserve_name, "Is", "The MediaPreserve")
            
            # Check the PRESERVATION Bentley agent
            bhl_preservation_agent = agents[1]
            self.check_tag_attrib(bhl_preservation_agent, "Is", "ROLE", "PRESERVATION")
            self.check_tag_attrib(bhl_preservation_agent, "Is", "TYPE", "ORGANIZATION")

            bhl_preservation_name = [name for name in bhl_preservation_agent][0]
            self.check_tag_text(bhl_preservation_name, "Is", "University of Michigan, Bentley Historical Library")

            # Check the DISSEMINATOR Bentley agent
            bhl_disseminator_agent = agents[2]
            self.check_tag_attrib(bhl_disseminator_agent, "Is", "ROLE", "DISSEMINATOR")
            self.check_tag_attrib(bhl_disseminator_agent, "Is", "TYPE", "ORGANIZATION")

            bhl_disseminator_name = [name for name in bhl_disseminator_agent][0]
            self.check_tag_text(bhl_disseminator_name, "Is", "University of Michigan, Bentley Historical Library")

    def validate_descriptive_metadata(self):
        """
        Validates dmdSec section"""

        descriptive_metadata = self.tree.xpath("/mets:mets/mets:dmdSec", namespaces=namespaces)
        
        if not descriptive_metadata:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no descriptive metadata'
            )

        elif self.item_metadata:
            descriptive_metadata = descriptive_metadata[0]
            dc_metadata = descriptive_metadata.xpath("./mets:mdWrap/mets:xmlData", namespaces=namespaces)[0]
            dc_title = dc_metadata.xpath("./dc:title", namespaces=namespaces)[0]
            dc_relation = dc_metadata.xpath("./dc:relation", namespaces=namespaces)[0]
            dc_identifier = dc_metadata.xpath("./dc:identifier", namespaces=namespaces)[0]

            self.check_tag_text(dc_title, "Is", self.item_metadata["item_title"])
            self.check_tag_text(dc_relation, "Is", self.item_metadata["collection_title"])
            self.check_tag_text(dc_identifier, "Is", self.item_id)


    def validate_administrative_metadata(self):
        """
        Validates amdSec section"""

        administrative_metadata = self.tree.xpath("/mets:mets/mets:amdSec", namespaces=namespaces)
        
        if not administrative_metadata:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no administrative metadata'
            )


    def validate_file_section(self):
        """
        Validates fileSec section"""

        file_section = self.tree.xpath("/mets:mets/mets:fileSec", namespaces=namespaces)

        if not file_section:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no file section'
            )

    def validate_structural_map_section(self):
        """
        Validates structMap section"""

        structural_map_section = self.tree.xpath("/mets:mets/mets:structMap", namespaces=namespaces)

        if not structural_map_section:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no structural map section'
            )


    def parse_item_mets(self, item):
        """
        Parses item METS"""

        path_to_item = item['path']
        mets = item['files']['xml'][0]
        
        self.item_id = item['id']
        self.item_metadata = self.project.metadata["item_metadata"].get(self.item_id)
        self.path_to_mets = os.path.join(path_to_item, mets)
        self.tree = etree.parse(self.path_to_mets)

    def validate_mets(self):
        """ 
        Validates METS"""

        for item in self.project.items:
        
            # Assuming for now that validating directory and file structure would have picked this up
            if not item['files']['xml']:
                continue

            else:
                self.parse_item_mets(item)
            
                self.validate_mets_header()
                self.validate_descriptive_metadata()
                self.validate_administrative_metadata()
                self.validate_file_section()
                self.validate_structural_map_section()
