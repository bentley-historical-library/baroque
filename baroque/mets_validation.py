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
            if tag.attrib.get(attribute) != value:
                self.error(
                    self.path_to_mets,
                    self.item_id,
                    tag.attrib.get(attribute) + ' in ' + attribute + ' attribute does not equal ' + value + ' value in ' + tag.tag
                )
    
    def check_element_exists(self, element):
        elements = self.tree.xpath(element, namespaces=namespaces)
        if len(elements) == 0:
            self.error(
                self.path_to_mets,
                self.item_id,
                'mets xml has no element {}'.format(element)
            )
            return elements
        else:
            return elements[0]
    
    def check_subelements_exist(self, element, subelement_path, expected=1):
        subelements = element.findall(subelement_path, namespaces=namespaces)
        if len(subelements) != expected:
            self.error(
                self.path_to_mets,
                self.item_id,
                "{} {} subelements found in {}, expected {}".format(len(subelements), subelement_path, element.tag, expected)
            )
            subelements = None

        return subelements

    
    def check_subelement_exists(self, element, subelement_path):
        subelement = element.find(subelement_path, namespaces=namespaces)
        if subelement is None:
            self.error(
                self.path_to_mets,
                self.item_id,
                "subelement {} not found in {}".format(subelement_path, element.tag)
            )

        return subelement

    def validate_root_element(self):
        """
        Validates root mets element"""
        mets_element = self.check_element_exists("/mets:mets")

        if mets_element is not None:
            mets_element_nsmap = mets_element.nsmap
            for ns, namespace in namespaces.items():
                if not mets_element_nsmap.get(ns) == namespace:
                    self.error(
                        self.path_to_mets,
                        self.item_id,
                        "mets xml is missing the following namespace: {}:{}".format(ns, namespace)
                    )
            
            self.check_tag_attrib(mets_element, "Exists", "OBJID")
            self.check_tag_attrib(mets_element, "Is", "OBJID", self.item_id)
            self.check_tag_attrib(mets_element, "Exists", "TYPE")
            self.check_tag_attrib(mets_element, "Is", "AUDIO RECORDING") # Note: this assumes BAroQUe will only be used for audio QC

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
        
        mets_header = self.check_element_exists("/mets:mets/mets:metsHdr")

        if mets_header is not None:
            # Check that metsHdr attribute CREATE DATE exists
            self.check_tag_attrib(mets_header, "Exists", "CREATEDATE")

            # Check that there are three agent tags
            agents = self.check_subelements_exist(mets_header, "mets:agent", expected=3)
            if agents is not None:
                # Check the MediaPreserve agent
                mediapreserve_agent = agents[0]
                self.check_tag_attrib(mediapreserve_agent, "Is", "ROLE", "OTHER") # Feels like I should check to see if this exists first

                mediapreserve_name = self.check_subelement_exists(mediapreserve_agent, "mets:name")
                if mediapreserve_name is not None:
                    self.check_tag_text(mediapreserve_name, "Is", "The MediaPreserve")
                
                # Check the PRESERVATION Bentley agent
                bhl_preservation_agent = agents[1]
                self.check_tag_attrib(bhl_preservation_agent, "Is", "ROLE", "PRESERVATION")
                self.check_tag_attrib(bhl_preservation_agent, "Is", "TYPE", "ORGANIZATION")

                bhl_preservation_name = self.check_subelement_exists(bhl_preservation_agent, "mets:name")
                if bhl_preservation_name is not None:
                    self.check_tag_text(bhl_preservation_name, "Is", "University of Michigan, Bentley Historical Library")

                # Check the DISSEMINATOR Bentley agent
                bhl_disseminator_agent = agents[2]
                self.check_tag_attrib(bhl_disseminator_agent, "Is", "ROLE", "DISSEMINATOR")
                self.check_tag_attrib(bhl_disseminator_agent, "Is", "TYPE", "ORGANIZATION")

                bhl_disseminator_name = self.check_subelement_exists(bhl_disseminator_agent, "mets:name")
                if bhl_disseminator_name is not None:
                    self.check_tag_text(bhl_disseminator_name, "Is", "University of Michigan, Bentley Historical Library")

    def validate_descriptive_metadata(self):
        """
        Validates dmdSec section"""

        descriptive_metadata = self.check_element_exists("/mets:mets/mets:dmdSec")

        if descriptive_metadata is not None:
            if self.item_metadata:
                mdWrap = self.check_subelement_exists(descriptive_metadata, "mets:mdWrap")
                if mdWrap is not None:
                    xmlData = self.check_subelement_exists(mdWrap, "mets:xmlData")
                    if xmlData is not None:
                        dc_title = self.check_subelement_exists(xmlData, "dc:title")
                        if dc_title is not None:
                            self.check_tag_text(dc_title, "Is", self.item_metadata["item_title"])
                        
                        dc_relation = self.check_subelement_exists(xmlData, "dc:relation")
                        if dc_relation is not None:
                            self.check_tag_text(dc_relation, "Is", self.item_metadata["collection_title"])
                        
                        dc_identifier = self.check_subelement_exists(xmlData, "dc:identifier")
                        if dc_identifier is not None:
                            self.check_tag_text(dc_identifier, "Is", self.item_id)
            else:
                self.warn(
                    self.path_to_mets,
                    self.item_id,
                    "item has no associated metadata to validate against mets xml dmdSec"
                )


    def validate_administrative_metadata(self):
        """
        Validates amdSec section"""

        administrative_metadata = self.check_element_exists("/mets:mets/mets:amdSec")


    def validate_file_section(self):
        """
        Validates fileSec section"""

        file_section = self.check_element_exists("/mets:mets/mets:fileSec")


    def validate_structural_map_section(self):
        """
        Validates structMap section"""

        structural_map_section = self.check_element_exists("/mets:mets/mets:structMap")


    def parse_item_mets(self, item):
        """
        Parses item METS"""

        path_to_item = item['path']
        mets = item['files']['xml'][0]
        
        self.item_id = item['id']
        self.item_metadata = self.project.metadata["item_metadata"].get(self.item_id)
        self.path_to_mets = os.path.join(path_to_item, mets)
        try:
            self.tree = etree.parse(self.path_to_mets)
            return True
        except:
            self.error(
                self.path_to_mets,
                self.item_id,
                "mets xml is not valid"
            )
            return False

    def validate_mets(self):
        """ 
        Validates METS"""

        for item in self.project.items:
        
            # Assuming for now that validating directory and file structure would have picked this up
            if not item['files']['xml']:
                continue
            else:
                if self.parse_item_mets(item):
                    self.validate_root_element()
                    self.validate_mets_header()
                    self.validate_descriptive_metadata()
                    self.validate_administrative_metadata()
                    self.validate_file_section()
                    self.validate_structural_map_section()
