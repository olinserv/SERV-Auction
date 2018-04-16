'''
PRECONDITION:	AUCTION is a dictionary filled with up-to-date information
				about this year's SERV Auction.
PRECONDITION:	{AUCTION[year]}/final.csv is a csv file where each row is an item,
				with information about the donor and winner, and a column that
				is blank to start at the end. The order of the columns is specified
				in HEADER. Feel free to change it.
PRECONDITION:	keys.py is a script containing EMAIL_USERNAME and EMAIL_PASSWORD,
				valid GMail credentials, and the attached GMail account has "Allow
				less secure apps" turned on.
POSTCONDITION:	Each winner who has been paid will be emailed along with the donor
				saying that they paid, unless they have already been emailed
				(the 'receipt' column keeps track of this automatically).
POSTCONDITION:	Each winner who has yet to pay will be emailed with a reminder,
				if and only if REMINDING is set to True.
POSTCONDITION:	{AUCTION[year]}\final_updated.csv is a duplicate of final.csv,
				where anyone who has been emailed with a receipt has a timestamp
				in their receipt column. This new version should be copied to
				whatever Google Sheet to keep track of who has been notified of
				their payment.
NOTE:			During payment week, this should be run as often as possible with
				updated information on who has been paid, such that donors and
				winners have up-to-date information.
TODO:			Actually send the receipts
'''

import csv
import string
import time

import smtplib
from email.mime.text import MIMEText

from helpers import *

import keys


REMINDING = False # are we reminding those who did not pay?


AUCTION = dict(
		year=2017,
		charity="Unidos por Puerto Rico",
		ein="66-0886334",
		total="$10,707.78",
		auctiondate="October 30, 2017",
		timestamp=time.strftime('%Y-%m-%d %H:%M:%S'))

HEADER = ['donor_name', 'donor_email', 'donor_affiliation', 'title', 'description', 'category', 'starting_bid',
		'interest_for', 'winner_name', 'winner_email', 'winning_bid', 'paid', 'receipt'] #NOTE: make sure this header is right

PAID_SUBJECT = '''{winner_name} has paid for the SERV Auction Item "{title}"'''
PAID_TEXT = '''\
Hello, {winner_name}. This email confirms that you paid {winning_bid} {payment_mode} for {donor_name}'s "{title}". You both should now work out amongst yourselves the details of the exchange.

{donor_name}, if your item had multiple winners, then you should receive a separate email for each winner who pays.

Thank you both for participating in the SERV Auction! With your help, we raised {total} for {charity}. Let me know if you have any questions.\
'''

REMIND_SUBJECT = '''SERV Auction item'''
REMIND_TEXT = '''\
I see you still haven't paid your {winning_bid} for "{title}". Please pay somehow as soon as physically possible. If you don't have a PayPal, please create one. It's really easy.
https://www.paypal.com/us/webapps/mpp/account-selection\
'''

D_RECEIPT_SUBJECT = '''Receipt - Item donation to the SERV Auction'''
D_RECEIPT_TEXT = '''\
This email serves as a receipt for your donation to the SERV Auction for the benefit of {charity}, which is tax-deductible under section 501-c3 of the IRS code. {charity}'s Employer Identification Number is {ein}.

Donor name:	{donor_name}
Donation date:	{auctiondate:.10}
Beneficiary: {charity} ({ein})
Donation:	{title}
	"{description}"
No goods or services were provided in exchange for this donation.\
'''

W_RECEIPT_SUBJECT = '''Receipt - Monetary donation to the SERV Auction'''
W_RECEIPT_TEXT = '''\
This email serves as a receipt for your donation to the SERV Auction for the benefit of {charity}, which is tax-deductible under section 501-c3 of the IRS code. {charity}'s Employer Identification Number is {ein}.

Donor Name:	{donor_name}
Date received:	{timestamp:.10}
Beneficiary: {charity} ({ein})
Donation:	{winning_bid}
In exchange for this monetary donation, {donor_name} received "{title}", with a fair market value of approximately {starting_bid}. The amount of this contribution that is eligible for deduction for federal income tax purposes is limited to the amount donated over the fair market value of "{title}".\
'''


with open('{}/final.csv'.format(AUCTION['year']), 'r', newline='') as f:
	with open('{}/final_updated.csv'.format(AUCTION['year']), 'w', newline='') as g:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		writer = csv.writer(g, delimiter=',', quotechar='"')

		header = True # I can't for the life of me figure out a better way to skip the header
		for row in reader:
			if header:
				header = False
				writer.writerow(row)
				continue

			item = {key:val.encode().decode('ascii','ignore').strip() for key,val in zip(HEADER,row)} # unpack the row into a dict

			if not item['donor_email']:
				item['donor_email'] = parse_email(item['donor_name'], item['donor_affiliation']) # check to make sure the email addresses are real
			if not item['winner_email']:
				raise ValueError('There was no winner email address provided for "{title}".'.format(**item))
			item['starting_bid'] = item['starting_bid'] # make sure all monetary amounts have exactly one dollar sign
			item['winning_bid'] = item['winning_bid']
			if item['paid'].lower() == "paypal":
				item['payment_mode'] = "via PayPal" # specify how tho payment was made, in words
			elif item['paid']:
				item['payment_mode'] = "to "+string.capwords(item['paid'])

			if item['paid'] and not item['receipt']: # send the receipt email
				msg = MIMEText(PAID_TEXT.format(**item, **AUCTION)) #TODO: send the legal tax receipts as well
				msg['Subject'] = PAID_SUBJECT.format(**item)
				msg['From'] = keys.EMAIL_USERNAME
				msg['To'] = "{winner_email}, {donor_email}".format(**item)
				row[-1] = AUCTION['timestamp']

			elif not item['paid'] and REMINDING: # send the reminder email
				msg = MIMEText(REMIND_TEXT.format(**item))
				msg['Subject'] = REMIND_SUBJECT.format(**item)
				msg['From'] = keys.EMAIL_USERNAME
				msg['To'] = "{winner_email}".format(**item)

			else:
				msg = None

			if msg is not None:
				print(msg, end='\n\n\n')
				# print("{donor_email}, {winner_email}, {title}".format(**item))
				# Send the message via gmail
				server = smtplib.SMTP('smtp.gmail.com', '587') # send the email using smtplib and gmail
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(keys.EMAIL_USERNAME, keys.EMAIL_PASSWORD)
				server.send_message(msg)
				server.quit()

			writer.writerow(row)
