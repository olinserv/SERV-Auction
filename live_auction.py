#! /usr/bin/python

import csv
from helpers import *

sample = open('2017/live.csv', "rb")
readSample = csv.reader(sample, delimiter=',', quotechar='"')

f = open('2017/live.tex','w')

print >>f, "\documentclass[11pt]{article}"
print >>f, "\pagestyle{plain} \\topmargin -.5in \oddsidemargin 0in"
print >>f, "\evensidemargin 0in \\textwidth 6.5in \\textheight 8in"
print >>f, "\setlength{\parindent}{0in}"
print >>f, "\\title{Live Auction Donation Packet}"
print >>f, "\\author{SERV Auction 2016}"
print >>f, "\\date{November 7th, 2016 to November 11th, 2016}"
print >>f, "\\begin{document}"
print >>f, "\\maketitle"

for item in readSample:

# Timestamp,
# Donor Name(s),
# Donator Email Address,
# Donator Affiliation,
# Item Title,
# Item Category,
# Item Starting Bid,
# Item Description,
# Number of Winners,
# Who might be interested in this item? Please select all that you think applies.,
# Do you want to nominate this for the live auction?

    personName  = item[1]
    title       = item[4]
    startingBid = item[6]
    description = item[7]

    print >>f, "\subsection{"+handleLatexChars(title)+"}" # title
    print >>f, handleLatexChars(personName) # name
    print >>f, "\\\\"
    print >>f, "Starting Bid: "+handleLatexChars(addDollarSign(startingBid))
    print >>f, "\\newline"
    print >>f, handleLatexChars(description).rstrip() # description

print >>f, "\\end{document}"
