from lxml import etree
import sys

# Add the whitelisted Party IDs
WHITELISTED_PARTY_IDS = ["PADPIDA2014021302H"]

def validate_xml(xml_file, schema_url):
    """
    Check 1: Validate XML file against the provided schema.
    - Parses the XML file and the schema.
    - Uses lxml to validate the XML against the schema.
    - Returns True if the file passes validation, False otherwise.
    """
    try:
        # Parse the XML file
        parser = etree.XMLParser(recover=True)
        with open(xml_file, 'rb') as f:
            xml_doc = etree.parse(f, parser)

        # Parse the schema
        schema_doc = etree.parse(schema_url)
        schema = etree.XMLSchema(schema_doc)

        # Validate the XML file against the schema
        if schema.validate(xml_doc):
            print("CHECK 1... PASS. Schema validation")
            return True
        else:
            # If validation fails, print the errors
            print("CHECK 1... FAIL. Schema validation")
            for error in schema.error_log:
                print(f"Error: {error.message}, Line: {error.line}")
            return False
    except Exception as e:
        print(f"CHECK 1... FAIL. Schema validation - Error: {e}")
        return False

def check_whitelisted_party_id(xml_file):
    """
    Check 2: Ensure the PartyId in the MessageSender section is whitelisted.
    - Uses XPath to locate the PartyId in the XML file.
    - Checks if the extracted PartyId is in the list of whitelisted Party IDs.
    - Returns True if the PartyId is whitelisted, False otherwise.
    """
    try:
        # Parse the XML file
        parser = etree.XMLParser(remove_blank_text=True)
        with open(xml_file, 'rb') as f:
            xml_doc = etree.parse(f, parser)
        
        # Define the namespaces
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}

        # Find the PartyId under ern:NewReleaseMessage -> MessageHeader -> MessageSender
        party_id_xpath = "//ern:NewReleaseMessage/*[local-name()='MessageHeader']/*[local-name()='MessageSender']/*[local-name()='PartyId']"
        party_id_elements = xml_doc.xpath(party_id_xpath, namespaces=namespaces)

        if not party_id_elements:
            print("CHECK 2... FAIL. No PartyID found in MessageSender")
            return False

        # Extract the PartyId value and check if it is in the whitelist
        party_id_value = party_id_elements[0].text.strip()
        if party_id_value in WHITELISTED_PARTY_IDS:
            print("CHECK 2... PASS. PartyId is whitelisted")
            return True
        else:
            print(f"CHECK 2... FAIL. PartyId '{party_id_value}' is not whitelisted")
            return False

    except Exception as e:
        print(f"CHECK 2... FAIL. PartyId check - Error: {e}")
        return False

def check_affiliation_type_for_sender(xml_file):
    """
    Check 4: Ensure that the "Type" in "Affiliation" inside "PartyList" for the 
    "PartyId" in the "MessageSender" is set to "MusicLicensingCompany".
    """
    try:
        # Parse the XML file
        parser = etree.XMLParser(remove_blank_text=True)
        with open(xml_file, 'rb') as f:
            xml_doc = etree.parse(f, parser)
        
        # Define the namespaces
        namespaces = {'ern': 'http://ddex.net/xml/ern/43'}

        # Find the PartyId under MessageSender
        party_id_xpath = "//ern:NewReleaseMessage/*[local-name()='MessageHeader']/*[local-name()='MessageSender']/*[local-name()='PartyId']"
        party_id_elements = xml_doc.xpath(party_id_xpath, namespaces=namespaces)

        if not party_id_elements:
            print("CHECK 4... FAIL. No PartyID found in MessageSender")
            return False

        party_id_value = party_id_elements[0].text.strip()

        # Now find the Party in PartyList with matching DPID or PartyId
        party_xpath = f"//ern:NewReleaseMessage/*[local-name()='PartyList']/*[local-name()='Party'][*[local-name()='PartyId']/*[local-name()='DPID']='{party_id_value}' or *[local-name()='PartyId'][text()='{party_id_value}']]"
        party_elements = xml_doc.xpath(party_xpath, namespaces=namespaces)

        if not party_elements:
            print(f"CHECK 4... FAIL. No Party found in PartyList for PartyId '{party_id_value}'")
            return False

        # Check the Type in Affiliation
        affiliation_type_xpath = ".//*[local-name()='Affiliation']/*[local-name()='Type']"
        affiliation_type_elements = party_elements[0].xpath(affiliation_type_xpath)

        if not affiliation_type_elements:
            print(f"CHECK 4... FAIL. No 'Affiliation Type' found for PartyId '{party_id_value}' in PartyList")
            return False

        affiliation_type_value = affiliation_type_elements[0].text.strip()
        if affiliation_type_value == "MusicLicensingCompany":
            print("CHECK 4... PASS. Affiliation Type is set correctly to 'MusicLicensingCompany'")
            return True
        else:
            print(f"CHECK 4... FAIL. Affiliation Type for PartyId '{party_id_value}' is '{affiliation_type_value}', not 'MusicLicensingCompany'")
            return False

    except Exception as e:
        print(f"CHECK 4... FAIL. Affiliation Type check - Error: {e}")
        return False

def main(xml_file):
    """
    Main function that orchestrates the checks:
    - First performs XML schema validation (Check 1).
    - Then performs the PartyId whitelist check (Check 2).
    - Then performs the Affiliation Type check for the MessageSender PartyId (Check 4).
    - Outputs the total number of checks, passed, and failed.
    """
    schema_url = "http://ddex.net/xml/ern/43/release-notification.xsd"
    
    total_checks = 3  # Increment as we add more checks
    passed_checks = 0

    # Check 1: XML Schema Validation
    if validate_xml(xml_file, schema_url):
        passed_checks += 1

    # Check 2: Whitelisted PartyId Check
    if check_whitelisted_party_id(xml_file):
        passed_checks += 1

    # Check 4: Affiliation Type Check for MessageSender PartyId
    if check_affiliation_type_for_sender(xml_file):
        passed_checks += 1

    # Output summary of checks
    failed_checks = total_checks - passed_checks
    print(f"\nTOTAL CHECKS: {total_checks}")
    print(f"PASSED CHECKS: {passed_checks}")
    print(f"FAILED CHECKS: {failed_checks}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <xml_file>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    main(xml_file)
