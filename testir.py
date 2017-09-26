#! /usr/bin/env python3

import os
import sys
from io import StringIO
import csv
from lxml import etree
import urllib.request

def parseDidl(urlDidl):
    """Parse DIDL and return list of all resources"""

    # List for storing extracted resources
    resources = []

    # Namespace definitions
    oai_pmh_ns = 'http://www.openarchives.org/OAI/2.0/'
    didl_ns = 'urn:mpeg:mpeg21:2002:02-DIDL-NS'
    didl_combined_ns = 'http://gh.kb-dans.nl/combined/v0.9/'
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance/'
    rdf_ns = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

    NSMAP =  {"ns": oai_pmh_ns,
              "xsi": xsi_ns,
              "didl": didl_ns,
              "dc": didl_combined_ns,
              "rdf": rdf_ns}

    # Parse DIDL data
    parser = etree.XMLParser()          
    root = etree.parse(urlDidl, parser)

    # We're only interested in nl_didl_norm and its child elements
    try:
        DIDL = root.xpath('//ns:GetRecord/ns:record/ns:metadata/dc:nl_didl_combined/dc:nl_didl_norm/didl:DIDL', 
                         namespaces=NSMAP)[0]
            
        # Get list of all didl:Item elements
        itemElts = DIDL.xpath('.//didl:Item', namespaces=NSMAP)

        for itemElt in itemElts:
            typeElt = itemElt.xpath('.//didl:Descriptor/didl:Statement/rdf:type', namespaces=NSMAP)[0]
            resourceType = typeElt.xpath('./@rdf:resource', namespaces=NSMAP)[0]
            
            # Only analyse object files, and ignore human start pages
            if resourceType == 'info:eu-repo/semantics/objectFile':
                # Get list of all didl:Resource elements
                resourceElts = itemElt.xpath('.//didl:Component/didl:Resource', namespaces=NSMAP)

                # Iterate over Resource elements and get URLs from 'ref' attribute values 
                for resourceElt in resourceElts:
                    try:
                        url = resourceElt.xpath('./@ref')[0]
                        #url = resourceElt.attrib['ref']
                        resources.append(url)
                    except IndexError:
                        pass

    except AttributeError:
        pass

    return resources


def processDIDL(urlDidl, csvOut):
    """Process one DIDL and write results to csvOut"""

    # Parse DIDL
    urls = parseDidl(urlDidl)
    
    # Iterate over urls
    for inURL in urls:
        try:
            # Open URL location, response to file-like object 'response'                         
            response = urllib.request.urlopen(inURL)

            # Output URL (can be different from inURL in case of redirection)
            outURL=response.geturl()

            # HTTP headers
            headers = response.info()

            # Data (i.e. the actual object that is retrieved)
            data = response.read()

            # Content-Disposition header
            contentDisposition = headers['Content-Disposition']
            if not contentDisposition: 
                contentDisposition = "n/a"
                
            # Content-Type header
            contentType = headers['Content-Type']
            if not contentType:
                contentType = "n/a"

        except urllib.error.HTTPError:
            outURL = "n/a"
            contentDisposition = "n/a"
            contentType = "n/a"

        # Write record to output file
        csvOut.writerow([inURL,outURL,contentDisposition, contentType])


def main():

    # CLI I/O
    if len(sys.argv) != 3:
        print("USAGE: testir.py inputFile outputFile")
        sys.exit()

    # Open input file (one DIDL link per line)
    fileIn = sys.argv[1]
    fIn = open(fileIn, "r", encoding="utf-8")
    # Content to list (each item represents 1 DIDL URL)
    didls = fIn.read().splitlines()
    fIn.close()

     # Open output file and create CSV writer object
    fileOut = sys.argv[2]
    fOut = open(fileOut, "w", encoding="utf-8")
    csvOut = csv.writer(fOut, lineterminator='\n')
    
    # Write header line to output file
    csvOut.writerow(["URLIn","URLOut","Content-Disposition", "Content-Type"])

    # Iterate over didl files
    for didl in didls:
        if didl != "":
            processDIDL(didl,csvOut)

    # Close output file
    fOut.close()

if __name__ == "__main__":
    main()
