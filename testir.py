#! /usr/bin/env python3

import os
import sys
import csv
from lxml import etree
import urllib.request

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


def processDIDL(didl, csvOut):

    # Parse DIDL
    urls = parseDidl(didl)

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
            try:
                contentDisposition = headers['Content-Disposition']
            except KeyError:
                contentDisposition = "n/a"
                
            # Content-Type header
            try:
                contentType = headers['Content-Type']
            except KeyError:
                contentType = "n/a"

        except urllib.error.HTTPError:
            outURL = "n/a"
            contentDisposition = "n/a"
            contentType = "n/a"

        # Write record to output file
        csvOut.writerow([inURL,outURL,contentDisposition, contentType])

    # TODO: include full http headers (maybe to separate file)

def main():

    # Replace by input from input CSV
    didls = ["./didlWUR.xml"]

    # Open output file and create CSV writer object
    fileOut = "./out.csv"
    fOut = open(fileOut, "w", encoding="utf-8")
    csvOut = csv.writer(fOut, lineterminator='\n')
    
    # Write header line to output file
    csvOut.writerow(["URLIn","URLout","Content-Disposition", "Content-Type"])

    # Iterate over didl files
    for didl in didls:
        processDIDL(didl,csvOut)

    fOut.close()

if __name__ == "__main__":
    main()
