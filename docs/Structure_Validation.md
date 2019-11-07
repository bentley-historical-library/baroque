## BAroQUe Structure Validation

Module used: `structure_validation.py`

BAroQUe performs the following checks:

- Shipment folder must have one or more Collection folders.
- Collection folder must have one or more Item folders.
- Item folder must follow the Collection Number-(SR-)Three Digit Item Number convention.
- Item folders must have one and only one XML file.
- Item folders must have at least one JPG file.
- Item folders must have one and only one TXT file.
- Each file must have size.
- For each audio intellectual unit, there must be one archival master (-am) and it must be a WAV file.
- For each audio intellectual unit, there must be one production master (-pm) and it must be a WAV file.
- For each audio intellectual unit, there must be one access derivative and it must be a MP3 file.
- Each WAV and MP3 file must follow the Collection Number-(SR-)Item Number(-am|-pm)-One Digit Sequential Number convention.
- The XML file must follow the Collection Number-(SR-)Item Number convention.
- The JPG files must follow the Collection Number-(SR-)Item Number-Three Digit Sequential Number convention.
- The TXT file must follow the Collection Number-(SR-)Item Number convention.
Ensures that there are no superfluous files
