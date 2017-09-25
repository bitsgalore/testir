#!/bin/bash

# **************
# USER I/O
# **************

# Check command line args
if [ "$#" -ne 1 ] ; then
  echo "Usage: test.sh inputFile" >&2
  exit 1
fi

# Input file
fileIn="$1"

fileOut=out.txt

# **************
# PROCESSING
# **************

while read line; do
  curl -o didl.xml "$line"
done <$fileIn


# Run VeraPDF
#$veraPDF -x --maxfailuresdisplayed 1 --policyfile $schema $pdfDir/* > $veraOut

# Run post-processing script
#python $extractScript $veraOut $veraCleaned $summaryFile
