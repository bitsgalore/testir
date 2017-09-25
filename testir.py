#! /usr/bin/env python3

from lxml import etree

def parseDidl(didl):
    oai_pmh_ns = 'http://www.openarchives.org/OAI/2.0/'
    didl_ns = 'urn:mpeg:mpeg21:2002:02-DIDL-NS'
    didl_combined_ns = 'http://gh.kb-dans.nl/combined/v0.9/'
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance/'

    NSMAP =  {"ns": oai_pmh_ns,
              "xsi": xsi_ns,
              "didl": didl_ns,
              "dc": didl_combined_ns}
    
    parser = etree.XMLParser()          
    root = etree.parse(didl, parser)
    DIDL = root.find('//ns:GetRecord/ns:record/ns:metadata/dc:nl_didl_combined/dc:nl_didl_norm/didl:DIDL/', 
                             namespaces=NSMAP)

    #nl_didl_norm = root.find('OAI-PMH', namespaces=NSMAP)
    # nl_didl_norm = tree.find("OAI-PMH/nl_didl_norm")
    print(DIDL)

    #for identifierURI in identifiersURI:
    #    modsIdentifierURI = etree.SubElement(modsRelatedItem, "{%s}identifier" %(config.mods_ns))
    #    modsIdentifierURI.attrib["type"] = "uri"
    #    modsIdentifierURI.text = identifierURI


def main():
    didl = "./didl.xml"
    parseDidl(didl)

if __name__ == "__main__":
    main()
