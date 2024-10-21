from lxml import etree
import sys
import logging

logging.basicConfig(level=logging.INFO)

# Add the whitelisted Party IDs
WHITELISTED_PARTY_IDS = ["PADPIDA2014021302H"]

def validate_xml(xml_file, schema_url):
    try:
        parser = etree.XMLParser(recover=True)
        xml_doc = etree.parse(xml_file, parser)

        schema_doc = etree.parse(schema_url)
        schema = etree.XMLSchema(schema_doc)

        if schema.validate(xml_doc):
            logging.info("CHECK 1... PASS. Schema validation")
            return True
        else:
            logging.error("CHECK 1... FAIL. Schema validation")
            for error in schema.error_log:
                logging.error(f"Error: {error.message}, Line: {error.line}")
            return False
    except Exception as e:
        logging.error(f"CHECK 1... FAIL. Schema validation - Error: {e}")
        return False

def check_whitelisted_party_id(xml_doc):
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        party_id_xpath = "//ern:NewReleaseMessage/*[local-name()='MessageHeader']/*[local-name()='MessageSender']/*[local-name()='PartyId']"
        party_id_elements = xml_doc.xpath(party_id_xpath, namespaces=namespaces)

        if not party_id_elements:
            logging.error("CHECK 2... FAIL. No PartyID found in MessageSender")
            return False

        party_id_value = party_id_elements[0].text.strip()
        if party_id_value in WHITELISTED_PARTY_IDS:
            logging.info("CHECK 2... PASS. PartyId is whitelisted")
            return True
        else:
            logging.error(f"CHECK 2... FAIL. PartyId '{party_id_value}' is not whitelisted")
            return False

    except Exception as e:
        logging.error(f"CHECK 2... FAIL. PartyId check - Error: {e}")
        return False

def check_right_share_percentage(xml_doc):
    """
    Check 3: Ensure that the RightSharePercentage inside ResourceRightsController,
    inside SoundRecording, inside ResourceList is never negative and never over 100.
    """
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        right_share_percentage_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']/*[local-name()='ResourceRightsController']/*[local-name()='RightSharePercentage']"
        right_share_elements = xml_doc.xpath(right_share_percentage_xpath, namespaces=namespaces)

        if not right_share_elements:
            logging.info("CHECK 3... PASS. No RightSharePercentage found, skipping check")
            return True

        for right_share_element in right_share_elements:
            right_share_value = float(right_share_element.text.strip())
            if right_share_value < 0 or right_share_value > 100:
                logging.error(f"CHECK 3... FAIL. RightSharePercentage '{right_share_value}' is out of range (0-100)")
                return False

        logging.info("CHECK 3... PASS. RightSharePercentage values are valid")
        return True

    except Exception as e:
        logging.error(f"CHECK 3... FAIL. RightSharePercentage check - Error: {e}")
        return False

def check_affiliation_type_for_sender(xml_doc):
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        party_id_xpath = "//ern:NewReleaseMessage/*[local-name()='MessageHeader']/*[local-name()='MessageSender']/*[local-name()='PartyId']"
        party_id_elements = xml_doc.xpath(party_id_xpath, namespaces=namespaces)

        if not party_id_elements:
            logging.error("CHECK 4... FAIL. No PartyID found in MessageSender")
            return False

        party_id_value = party_id_elements[0].text.strip()

        party_xpath = f"//ern:NewReleaseMessage/*[local-name()='PartyList']/*[local-name()='Party'][*[local-name()='PartyId']/*[local-name()='DPID']='{party_id_value}' or *[local-name()='PartyId'][text()='{party_id_value}']]"
        party_elements = xml_doc.xpath(party_xpath, namespaces=namespaces)

        if not party_elements:
            logging.error(f"CHECK 4... FAIL. No Party found in PartyList for PartyId '{party_id_value}'")
            return False

        affiliation_type_xpath = ".//*[local-name()='Affiliation']/*[local-name()='Type']"
        affiliation_type_elements = party_elements[0].xpath(affiliation_type_xpath)

        if not affiliation_type_elements:
            logging.error(f"CHECK 4... FAIL. No 'Affiliation Type' found for PartyId '{party_id_value}' in PartyList")
            return False

        affiliation_type_value = affiliation_type_elements[0].text.strip()
        if affiliation_type_value == "MusicLicensingCompany":
            logging.info("CHECK 4... PASS. Affiliation Type is set correctly to 'MusicLicensingCompany'")
            return True
        else:
            logging.error(f"CHECK 4... FAIL. Affiliation Type for PartyId '{party_id_value}' is '{affiliation_type_value}', not 'MusicLicensingCompany'")
            return False

    except Exception as e:
        logging.error(f"CHECK 4... FAIL. Affiliation Type check - Error: {e}")
        return False

def check_rights_type_for_sender(xml_doc):
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        party_id_xpath = "//ern:NewReleaseMessage/*[local-name()='MessageHeader']/*[local-name()='MessageSender']/*[local-name()='PartyId']"
        party_id_elements = xml_doc.xpath(party_id_xpath, namespaces=namespaces)

        if not party_id_elements:
            logging.error("CHECK 5... FAIL. No PartyID found in MessageSender")
            return False

        party_id_value = party_id_elements[0].text.strip()

        party_xpath = f"//ern:NewReleaseMessage/*[local-name()='PartyList']/*[local-name()='Party'][*[local-name()='PartyId']/*[local-name()='DPID']='{party_id_value}' or *[local-name()='PartyId'][text()='{party_id_value}']]"
        party_elements = xml_doc.xpath(party_xpath, namespaces=namespaces)

        if not party_elements:
            logging.error(f"CHECK 5... FAIL. No Party found in PartyList for PartyId '{party_id_value}'")
            return False

        rights_type_xpath = ".//*[local-name()='Affiliation']/*[local-name()='RightsType']"
        rights_type_elements = party_elements[0].xpath(rights_type_xpath)

        if not rights_type_elements:
            logging.error(f"CHECK 5... FAIL. No 'RightsType' found for PartyId '{party_id_value}' in PartyList")
            return False

        for rights_type in rights_type_elements:
            rights_type_value = rights_type.text.strip()
            if rights_type_value == "MakeAvailableRight":
                logging.info("CHECK 5... PASS. RightsType includes 'MakeAvailableRight'")
                return True

        logging.error(f"CHECK 5... FAIL. RightsType for PartyId '{party_id_value}' does not include 'MakeAvailableRight'")
        return False

    except Exception as e:
        logging.error(f"CHECK 5... FAIL. RightsType check - Error: {e}")
        return False

def check_isrc_in_sound_recording(xml_doc):
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        isrc_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']/*[local-name()='SoundRecordingEdition']/*[local-name()='ResourceId']/*[local-name()='ISRC']"
        isrc_elements = xml_doc.xpath(isrc_xpath, namespaces=namespaces)

        if not isrc_elements:
            logging.error("CHECK 6... FAIL. No ISRC found in SoundRecordingEdition inside ResourceList")
            return False

        isrc_value = isrc_elements[0].text.strip()
        if len(isrc_value) == 12 and isrc_value.isalnum():
            logging.info("CHECK 6... PASS. ISRC exists and is 12 characters long")
            return True
        else:
            logging.error(f"CHECK 6... FAIL. ISRC '{isrc_value}' is not valid (should be 12 characters long)")
            return False

    except Exception as e:
        logging.error(f"CHECK 6... FAIL. ISRC validation - Error: {e}")
        return False

def check_rights_controller_is_music_licensing_company(xml_doc):
    """
    Check 7: Ensure that the RightsControllerPartyReference inside ResourceRightsController,
    inside SoundRecording, inside ResourceList corresponds to a Party that is listed 
    as a MusicLicensingCompany in the PartyList.
    """
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}

        music_licensing_company_xpath = "//ern:NewReleaseMessage/*[local-name()='PartyList']/*[local-name()='Party'][*[local-name()='Affiliation']/*[local-name()='Type']='MusicLicensingCompany']/*[local-name()='PartyReference']"
        music_licensing_company_elements = xml_doc.xpath(music_licensing_company_xpath, namespaces=namespaces)

        if not music_licensing_company_elements:
            logging.error("CHECK 7... FAIL. No MusicLicensingCompany found in PartyList")
            return False

        music_licensing_company_refs = {elem.text.strip() for elem in music_licensing_company_elements}

        rights_controller_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']/*[local-name()='ResourceRightsController']/*[local-name()='RightsControllerPartyReference']"
        rights_controller_elements = xml_doc.xpath(rights_controller_xpath, namespaces=namespaces)

        if not rights_controller_elements:
            logging.error("CHECK 7... FAIL. No RightsControllerPartyReference found in ResourceRightsController")
            return False

        for rights_controller_elem in rights_controller_elements:
            rights_controller_ref = rights_controller_elem.text.strip()
            if rights_controller_ref not in music_licensing_company_refs:
                logging.error(f"CHECK 7... FAIL. RightsControllerPartyReference '{rights_controller_ref}' is not a MusicLicensingCompany")
                return False

        logging.info("CHECK 7... PASS. All RightsControllerPartyReferences are MusicLicensingCompanies")
        return True

    except Exception as e:
        logging.error(f"CHECK 7... FAIL. RightsController check - Error: {e}")
        return False

def check_rights_control_type_is_royalty_administrator(xml_doc):
    """
    Check 8: Ensure that the RightsControlType inside ResourceRightsController,
    inside SoundRecording, inside ResourceList is set to 'RoyaltyAdministrator'.
    """
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}

        rights_control_type_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']/*[local-name()='ResourceRightsController']/*[local-name()='RightsControlType']"
        rights_control_type_elements = xml_doc.xpath(rights_control_type_xpath, namespaces=namespaces)

        if not rights_control_type_elements:
            logging.error("CHECK 8... FAIL. No RightsControlType found in ResourceRightsController")
            return False

        for rights_control_type in rights_control_type_elements:
            rights_control_type_value = rights_control_type.text.strip()
            if rights_control_type_value == "RoyaltyAdministrator":
                logging.info("CHECK 8... PASS. RightsControlType is set to 'RoyaltyAdministrator'")
                return True

        logging.error(f"CHECK 8... FAIL. RightsControlType is not 'RoyaltyAdministrator'")
        return False

    except Exception as e:
        logging.error(f"CHECK 8... FAIL. RightsControlType check - Error: {e}")
        return False

def check_territory_of_rights_delegation(xml_doc):
    """
    Check 9: Ensure that every DelegatedUsageRights inside ResourceRightsController,
    inside SoundRecording, inside ResourceList contains a TerritoryOfRightsDelegation.
    """
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        delegated_usage_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']/*[local-name()='ResourceRightsController']/*[local-name()='DelegatedUsageRights']"
        delegated_usage_elements = xml_doc.xpath(delegated_usage_xpath, namespaces=namespaces)

        for delegated_usage in delegated_usage_elements:
            territory_xpath = ".//*[local-name()='TerritoryOfRightsDelegation']"
            territory_elements = delegated_usage.xpath(territory_xpath)

            if not territory_elements:
                logging.error("CHECK 9... FAIL. No TerritoryOfRightsDelegation found in DelegatedUsageRights")
                return False

        logging.info("CHECK 9... PASS. All DelegatedUsageRights have TerritoryOfRightsDelegation")
        return True

    except Exception as e:
        logging.error(f"CHECK 9... FAIL. TerritoryOfRightsDelegation check - Error: {e}")
        return False

def check_use_type_in_sound_recording(xml_doc):
    """
    Check 10: Ensure every SoundRecording has a UseType value of at least one of the following:
    'Stream', 'PermanentDownload', 'ConditionalDownload', 'TetheredDownload'.
    """
    try:
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}
        valid_use_types = {"Stream", "PermanentDownload", "ConditionalDownload", "TetheredDownload"}
        sound_recording_xpath = "//ern:NewReleaseMessage/*[local-name()='ResourceList']/*[local-name()='SoundRecording']"
        sound_recordings = xml_doc.xpath(sound_recording_xpath, namespaces=namespaces)

        for sound_recording in sound_recordings:
            use_type_xpath = ".//*[local-name()='DelegatedUsageRights']/*[local-name()='UseType']"
            use_type_elements = sound_recording.xpath(use_type_xpath)

            if not use_type_elements:
                logging.error("CHECK 10... FAIL. No UseType found for a SoundRecording")
                return False

            for use_type_element in use_type_elements:
                use_type_value = use_type_element.text.strip()
                if use_type_value in valid_use_types:
                    logging.info("CHECK 10... PASS. Valid UseType found")
                    break
            else:
                logging.error("CHECK 10... FAIL. No valid UseType found")
                return False

        return True

    except Exception as e:
        logging.error(f"CHECK 10... FAIL. UseType check - Error: {e}")
        return False

def main(xml_file, schema_url):
    total_checks = 10  # Updated for the current number of checks
    passed_checks = 0

    try:
        # Parse the XML file and handle encoding automatically
        xml_doc = etree.parse(xml_file, etree.XMLParser(recover=True))

        if validate_xml(xml_file, schema_url):
            passed_checks += 1

        if check_whitelisted_party_id(xml_doc):
            passed_checks += 1

        if check_right_share_percentage(xml_doc):
            passed_checks += 1

        if check_affiliation_type_for_sender(xml_doc):
            passed_checks += 1

        if check_rights_type_for_sender(xml_doc):
            passed_checks += 1

        if check_isrc_in_sound_recording(xml_doc):
            passed_checks += 1

        if check_rights_controller_is_music_licensing_company(xml_doc):
            passed_checks += 1

        if check_rights_control_type_is_royalty_administrator(xml_doc):
            passed_checks += 1

        if check_territory_of_rights_delegation(xml_doc):
            passed_checks += 1

        if check_use_type_in_sound_recording(xml_doc):
            passed_checks += 1

    except Exception as e:
        logging.error(f"Error processing file: {e}")

    failed_checks = total_checks - passed_checks
    logging.info(f"\nTOTAL CHECKS: {total_checks}")
    logging.info(f"PASSED CHECKS: {passed_checks}")
    logging.info(f"FAILED CHECKS: {failed_checks}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <xml_file> <schema_url>")
        sys.exit(1)

    xml_file = sys.argv[1]
    schema_url = sys.argv[2]
    main(xml_file, schema_url)
