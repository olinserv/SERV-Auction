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
POSTCONDITION:	{AUCTION[year]}/final_updated.csv is a duplicate of final.csv,
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


SAFETY_ON = False # flag to disable the actual email sending
REMINDING = True # are we reminding those who did not pay?


AUCTION = dict(
		year=2018,
		charity="The Human Rights Initiative",
		ein="75-2842602",
		total="$7 854.40",
		auctiondate="2018-11-09 12:40",
		timestamp=time.strftime('%Y-%m-%d %H:%M:%S'))

HEADER = ['title', 'description', 'donor_name', 'donor_email', 'num_winners',
		'winner_name', 'winner_email', 'starting_bid', 'winning_bid', 'paid', 'receipt'] #NOTE: make sure this header is right

PAID_SUBJECT = '''{winner_name} has paid for the SERV Auction item "{title}"'''
PAID_TEXT = '''\
Hello, {winner_name}. This email confirms that you paid ${winning_bid} {payment_mode} for {donor_name}'s "{title}". You both should now work out amongst yourselves the details of the exchange.

{donor_name}, if your item had multiple winners, then you will receive a separate email for each winner who pays.

Thank you both for participating in the SERV Auction! With your help, we raised {total} for {charity}. Let me know if you have any questions.\
'''

REMIND_SUBJECT = '''Serv Auction Item'''
REMIND_TEXT = '''\
Please let me know if you're having any difficulty paying which we might alleviate. If you pay through the Paypal invoice, you shouldn't need a Paypal account; just a card or bank account.

Thank you,
SERV
'''

D_RECEIPT_SUBJECT = '''Receipt - Item donation to the SERV Auction'''
D_RECEIPT_TEXT = '''\
This email serves as a receipt for your donation to the SERV Auction for the benefit of {charity}, which is tax-deductible under section 501-c3 of the IRS code. {charity}'s Employer Identification Number is {ein}.

Donor name:	{donor_name}
Donation date:	{auctiondate:.10}
Beneficiary:	{charity} ({ein})
Donation:	{title}
	"{description}"
No goods or services were provided in exchange for this donation.\
'''

W_RECEIPT_SUBJECT = '''Receipt - Monetary donation to the SERV Auction'''
W_RECEIPT_TEXT = '''\
This email serves as a receipt for your donation to the SERV Auction for the benefit of {charity}, which is tax-deductible under section 501-c3 of the IRS code. {charity}'s Employer Identification Number is {ein}.

Donor Name:	{winner_name}
Date received:	{timestamp:.10}
Beneficiary:	{charity} ({ein})
Donation:	{winning_bid}
In exchange for this monetary donation, {winner_name} received "{title}"{value_hack}. The amount of this contribution that is eligible for deduction for federal income tax purposes is limited to the amount donated over the fair market value of "{title}".\
'''


if __name__ == '__main__':
	with open('{}/final.csv'.format(AUCTION['year']), 'r', newline='', encoding='utf-8') as f_in, \
			open('{}/final_updated.csv'.format(AUCTION['year']), 'w', newline='', encoding='utf-8') as f_out:
		reader = csv.reader(f_in, delimiter=',', quotechar='"')
		writer = csv.writer(f_out, delimiter=',', quotechar='"')

		header = True # I can't for the life of me figure out a better way to skip the header
		for row in reader:
			assert len(row) == len(HEADER), "Length of {} is wrong".format(row)
			if header:
				header = False
				writer.writerow(row)
				continue

			item = {key:val.encode().decode('ascii','ignore').strip() for key,val in zip(HEADER,row)} # unpack the row into a dict
			if not item['winner_name']:
				print("No one bid on {title}".format(**item))
				continue # skip ones on which no one bid
			if not item['title']:
				continue # skip fake rows if they exist

			if not item['donor_email']:
				item['donor_email'] = parse_email(item['donor_name'], item.get('donor_affiliation', None)) # check to make sure the email addresses are real
			if not item['winner_email']:
				item['winner_email'] = parse_email(item['winner_name'], item.get('winner_affiliation', None))
			item['value_hack'] = ", with a fair market value of approximately {}".format(item['starting_bid']) if item['starting_bid'] else ""
			# item['starting_bid'] = item['starting_bid'] # make sure all monetary amounts have exactly one dollar sign
			# item['winning_bid'] = item['winning_bid']
			if item['paid'].lower() == "paypal":
				item['payment_mode'] = "via PayPal" # specify how the payment was made, in words
			elif item['paid']:
				item['payment_mode'] = "to "+string.capwords(item['paid'])

			msgs = []
			if item['paid'] and not item['receipt']: # send the receipt email
				msgs.append(MIMEText(PAID_TEXT.format(**item, **AUCTION)))
				msgs[-1]['Subject'] = PAID_SUBJECT.format(**item)
				msgs[-1]['From'] = keys.EMAIL_USERNAME
				msgs[-1]['To'] = "{winner_email}, {donor_email}".format(**item)
				msgs.append(MIMEText(D_RECEIPT_TEXT.format(**item, **AUCTION))) # TODO: uncomment this
				msgs[-1]['Subject'] = D_RECEIPT_SUBJECT.format(**item)
				msgs[-1]['From'] = keys.EMAIL_USERNAME
				msgs[-1]['To'] = "{donor_email}".format(**item)
				msgs.append(MIMEText(W_RECEIPT_TEXT.format(**item, **AUCTION)))
				msgs[-1]['Subject'] = W_RECEIPT_SUBJECT.format(**item)
				msgs[-1]['From'] = keys.EMAIL_USERNAME
				msgs[-1]['To'] = "{winner_email}".format(**item)
				row[HEADER.index('receipt')] = AUCTION['timestamp']

			elif not item['paid'] and REMINDING: # send the reminder email
				msgs.append(MIMEText(REMIND_TEXT.format(**item, **AUCTION)))
				msgs[-1]['Subject'] = REMIND_SUBJECT.format(**item)
				msgs[-1]['From'] = keys.EMAIL_USERNAME
				msgs[-1]['To'] = "{winner_email}".format(**item)

			for msg in msgs:
				if SAFETY_ON: # Send the message via stdout
					print(msg, end='\n\n\n')
				else: # Send the message via gmail
					print("{To}, {title}, {Subject}".format(**msg, **item))
					cooldown = 1
					while True:
						try:
							server = smtplib.SMTP('smtp.gmail.com', '587') # send the email using smtplib and gmail
							server.ehlo()
							server.starttls()
							server.ehlo()
							server.login(keys.EMAIL_USERNAME, keys.EMAIL_PASSWORD)
							server.send_message(msg)
							server.quit()
							break
						except (smtplib.SMTPServerDisconnected, smtplib.SMTPSenderRefused):
							print("Email failed. Trying again in {} seconds.".format(cooldown))
							time.sleep(cooldown)
							cooldown *= 2

			writer.writerow(row)
