#! /usr/bin/env python3

from lxml import etree

def parseDidl(didl):
    """Parse DIDL and return list of all resources"""

    # List for storing extracted resources
    resources = []

    # Namespace definitions
    oai_pmh_ns = 'http://www.openarchives.org/OAI/2.0/'
    didl_ns = 'urn:mpeg:mpeg21:2002:02-DIDL-NS'
    didl_combined_ns = 'http://gh.kb-dans.nl/combined/v0.9/'
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance/'

    NSMAP =  {"ns": oai_pmh_ns,
              "xsi": xsi_ns,
              "didl": didl_ns,
              "dc": didl_combined_ns}

    # Parse DIDL
    parser = etree.XMLParser()          
    root = etree.parse(didl, parser)

    # We're only interested in nl_didl_norm and its child elements  
    DIDL = root.find('//ns:GetRecord/ns:record/ns:metadata/dc:nl_didl_combined/dc:nl_didl_norm/didl:DIDL', 
                             namespaces=NSMAP)

    # Get list of all didl:Resource elements
    resourceElts = DIDL.xpath('//didl:Item/didl:Component/didl:Resource', namespaces=NSMAP)

    # Iterate over Resource elements and get URLs from 'ref' attribute values 
    for resourceElt in resourceElts:
        try:
            url = resourceElt.attrib['ref']
            resources.append(url)
        except KeyError:
            pass

    return resources


def main():
    didl = "./didl.xml"
    resources = parseDidl(didl)
    print(resources)

if __name__ == "__main__":
    main()
