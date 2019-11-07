## BAroQUe METS File Validation

Module used: mets_validation.py

BAroQUe performs the following checks on each METS XML file:

  - XML must be valid.
  - XML tag must have "mets:mets" tag.
  - "mets:mets" tag must have "xmlns:mets" attribute and value must be "http://www.loc.gov/METS/."
  - "mets:mets" tag must have "xmlns:aes" attribute and value must be "http://www.aes.org/audioObject."
  - "mets:mets" tag must have "xmlns:ph" attribute and value must be "http://www.aes.org/processhistory."
  - "mets:mets" tag must have "xmlns:dc" attribute and value must be "http://purl.org/dc/elements/1.1/."
  - "mets:mets" tag must have "xmlns:mods" attribute and value must be "http://www.loc.gov/mods/v3."
  - "mets:mets" tag must have "OBJID" attribute.
  - "OBJID" attribute value must follow Collection Number-(SR-)Item Number convention.
  - "mets:mets" tag must have "TYPE" attribute.
  - "TYPE" attribute must have "AUDIO RECORDING," "VIDEO RECORDING" or "FILM RECORDING" value as appropriate..
  - "mets:mets" tag must have "mets:metsHdr" tag.
  - "mets:mets" tag must have "mets:dmdSec" tag.
  - "mets:mets" tag must have "mets:amdSec" tag.
  - "mets:mets" tag must have "mets:fileSec" tag.
  - "mets:mets" tag must have "mets:structMap" tag.
  - "mets:metsHdr" tag must have "CREATEDATE" attribute.
  - "mets:metsHdr" tag must have three "mets:agent" tags.
  - This "mets:agent" tag must have "mets:name" tag.
  - One "mets:agent" tag must have "ROLE" attribute with "PRESERVATION" value and "TYPE" attribute with "ORGANIZATION" value.
  - This "mets:agent" tag must have "mets:name" tag with "University of Michigan, Bentley Historical Library" value.
  - One "mets:agent" tag must have "ROLE" attribute with "DISSEMINATOR" value and "TYPE" attribute with "ORGANIZATION" value.
  - This "mets:agent" tag must have "mets:name" tag with "University of Michigan, Bentley Historical Library" value.
  - "mets:dmdSec" tag must have "mets:mdWrap" tag.
  - "mets:mdWrap" tag must have "MDTYPE" attribute with "DC" value and "LABEL" attribute with "Dublin Core Metadata" value.
  - "mets:mdWrap" tag must "mets:xmlData" tag.
  - "mets:xmlData" tag must have "dc:title" tag.
  - "dc:title" tag value must match CSV "title" value. -- 2nd pass
  - "dc:date": At least check if it's there (do additional analysis to see what it would take to see if it matches)
          Essentially three types of errors discovered and accounted for): undated/Undated, MM/DD/YYYY to YYYY Month DD, MM/DD/YYYY to Month DD, YYYY
  - "dc.format" should be present
  - There should be at least one "dc.format.extent"
  - For each version of each audio, film or video intellectual unit, "mets:amdSec" tag must have "mets:techMD" tag.
  - "mets:amdSec" tag must have "mets:sourceMD" tag.
  - "mets:amdSec" tag must have "mets:digiprovMD" tag.
  - "mets:fileSec" tag must have two "mets:fileGrp" tags.
  - One "mets:fileGrp" tag must have an "ID" attribute with "audio-files," "video-files" or "film-files" value, as appropriate.
  - One "mets:fileGrp" tag must have an "ID" attribute with "media_images" value.
  - "mets:fileGrp" tag with an "ID" attribute and an "audio-files" value must have three "mets:fileGrp" tags.
  - "mets:structMap" tag must have "mets:div" tag.
  - "mets:div" tag must have one, but may have more than one "mets:div" tag, as appropriate.
  - "mets:div" tag must have more than one "mets:fptr" tags (three for audio, two for film and video)
