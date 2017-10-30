# KNOWN ANOMALIES: "\^\^" is not valid Latex (needs to not be escaped), but "^" must be escaped everywhere else. Odd edge case.

import csv
from helpers import *

ALUMNI_FILTER = False
NUM_LINES = 26

sample = open('2017/silent.csv', "rb")
readSample = csv.reader(sample, delimiter=',', quotechar='"')

f = open('2017/servsheets.tex','w')
g = open('2017/servpacket.tex','w')

print >>f, "\\documentclass[11pt]{article}"
print >>f, "\\pagestyle{plain} \\topmargin -.5in \oddsidemargin 0in"
print >>f, "\\evensidemargin 0in \\textwidth 6.5in \\textheight 8in"
print >>f, "\\setlength{\parindent}{0in}"
print >>f, "\\begin{document}"

print >>g, "\\documentclass[11pt]{article}"
print >>g, "\\pagestyle{plain} \\topmargin -.5in \oddsidemargin 0in"
print >>g, "\\evensidemargin 0in \\textwidth 6.5in \\textheight 8in"
print >>g, "\\setlength{\parindent}{0in}"
print >>g, "\\title{Silent Auction Donation Packet}"
print >>g, "\\author{SERV Auction 2016}"
# TODO: Update these dates.
print >>g, "\\date{November 7th, 2016 to November 11th, 2016}"
print >>g, "\\begin{document}"
print >>g, "\\maketitle"

categories = [[],[],[],[],[],[]]
categoryNames = ["Services", "Food", "Events", "Lessons", "Arts and Crafts", "Miscellaneous"]

header = True # I can't for the life of me figure out a better way to skip the header
for item in readSample:
	if header:
		header = False
		continue
	idx = categoryNames.index(item[5])
	categories[idx].append(item)

for (i, category) in enumerate(categories):

	category = sorted(category,key=lambda item: float(item[6])) # sort by minimum bid, lowest to highest
	print >>g, "\section{"+categoryNames[i]+"}"
	for (j,item) in enumerate(category):

		# NOTE: Change the numbers here to match the CSV.
		personName  = handleLatexChars(item[0])
		affiliation = handleLatexChars(item[2])
		email       = handleLatexChars(item[1]) if item[1] else parse_email(personName, affiliation)
		title       = handleLatexChars(item[3])
		description = handleLatexChars(item[4]).rstrip()
		startingBid = handleLatexChars(addDollarSign(item[6]))
		interestFor = handleLatexChars(item[7])
		numWinners  = int(item[8]) if item[8] else 1

		# Enable Alumni only filter.
		if ALUMNI_FILTER:
			if 'Alumni' not in interestFor and 'anyone' not in interestFor:
				continue

		print >>f, r"\section*{{{}.{} {}}}".format(i+1, j+1, title) # title
		print >>f, r"{} ({}) \\".format(personName, email) # name
		print >>f, r"Starting Bid: {} \\".format(startingBid)
		print >>f, r"Winner(s): "
		if numWinners == 1: 	print >>f, r"Top bidder \\"
		else: 					print >>f, r"Top {} bids \\".format(numWinners)
		print >>f, r"{} \\[6ex]".format(description) # description
		print >>f, r"\begin{tabular}{c c c}"
		print >>f, r"~~~~~~~~~~~~~Name~~~~~~~~~~~~~ & ~~~~~~~~~Bid (\$)~~~~~~~~~ & ~~~Email Address (if not standard olin.edu)~~~ \\"
		for a in range(NUM_LINES): # print lines for bids
			print >>f, r" & & \\"
			print >>f, r"\hline"
		print >>f, r"\end{tabular}"
		print >>f, r"\clearpage"

		print >>g, r"\subsection{{{}}}".format(title) # title
		print >>g, r"{} ({}) \\".format(personName, email) # name
		print >>g, r"Starting Bid: {} \\".format(startingBid)
		print >>g, r"Winner(s): "
		if numWinners == 1: 	print >>g, r"Top bidder\newline"
		else: 					print >>g, r"Top {} bids\newline".format(numWinners)
		print >>g, r"{}".format(description) # description # description

print >>f, r"\end{document}"
print >>g, r"\end{document}"
