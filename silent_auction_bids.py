#run in Python 2.7

# KNOWN ANOMALIES: "\^\^" is not valid Latex (needs to not be escaped), but "^" must be escaped everywhere else. Odd edge case.
# I made some changes but have yet to test it because the auction is over. So FYI, it might not run perfectly. -2017

import csv
from helpers import *

ALUMNI_FILTER = False
NUM_LINES = 26

with open('2017/silent.csv', 'r') as sample:
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

	for i, category in enumerate(categories):

		category = sorted(category, key=lambda item:item[3].lower()) # sort by title, alphabetically
		print >>g, "\section{"+categoryNames[i]+"}"
		for j, item in enumerate(category):
			name, email, affiliation, title, description, category, starting_bid, interest_for, num_winners = item #NOTE: make sure this header is right

			if not email:
				email = parse_email(name, affiliation) #format some things correctly
			description = handleLatexChars(description).rstrip()
			starting_bid = handleLatexChars(addDollarSign(starting_bid))
			interest_for = handleLatexChars(interest_for)
			num_winners  = int(num_winners) if num_winners else 1

			# Enable Alumni only filter.
			if ALUMNI_FILTER:
				if 'Alumni' not in interest_for and 'anyone' not in interest_for:
					continue

			print >>f, r"\section*{{{}.{} {}}}".format(i+1, j+1, title) # title
			print >>f, r"{} ({}) \\".format(name, email) # name
			print >>f, r"Starting Bid: {} \\".format(starting_bid)
			print >>f, r"Winner(s): "
			if num_winners == 1: 	print >>f, r"Top bidder \\"
			else: 					print >>f, r"Top {} bids \\".format(num_winners)
			print >>f, r"{} \\[6ex]".format(description) # description
			print >>f, r"\begin{tabular}{c c c}"
			print >>f, r"~~~~~~~~~~~~~Name~~~~~~~~~~~~~ & ~~~~~~~~~Bid (\$)~~~~~~~~~ & ~~~Email Address (if not standard olin.edu)~~~ \\"
			for a in range(NUM_LINES): # print lines for bids
				print >>f, r" & & \\"
				print >>f, r"\hline"
			print >>f, r"\end{tabular}"
			print >>f, r"\clearpage"

			print >>g, r"\subsection{{{}}}".format(title) # title
			print >>g, r"{} ({}) \\".format(name, email) # name
			print >>g, r"Starting Bid: {} \\".format(starting_bid)
			print >>g, r"Winner(s): "
			if num_winners == 1: 	print >>g, r"Top bidder\newline"
			else: 					print >>g, r"Top {} bids\newline".format(num_winners)
			print >>g, r"{}".format(description) # description

	print >>f, r"\end{document}"
	print >>g, r"\end{document}"

	f.close()
	g.close()
