#run in Python 3.5

import csv
import string
import time

import smtplib
from email.mime.text import MIMEText

from helpers import *

import keys


REMINDING = False #are we reminding those who did not pay?


PAID_SUBJECT = '''{winner_name} has paid for the SERV Auction Item "{title}"'''
PAID_TEXT = '''\
Hello, {winner_name}. This email confirms that you paid {winning_bid} {payment_mode} for {donor_name}'s "{title}". You both should now work out amongst yourselves the details of the exchange.

{donor_name}, if your item had multiple winners, then you should receive a separate email for each winner who pays.

Thank you both for participating in the SERV Auction! With your help, we raised $10,707.78 for Unidos por Puerto Rico. Let me know if you have any questions.\
'''

REMIND_SUBJECT = '''Don't forget to pay for your SERV Auction item!'''
REMIND_TEXT = '''\
Hello, {winner_name}. According to our records, you have yet to pay for {donor_name}'s "{title}". You owe {winning_bid}.

If you believe this to be in error, please let me know. Otherwise, please pay us in the dining hall (we weren't there today, but we'll be there the rest of the week). Again, we accept cash, check, and PayPal (team02.ebang@olin.edu).

Thank you\
'''

HEADER = ['donor_name', 'donor_email', 'donor_affiliation', 'title', 'description', 'category', 'starting_bid',
		'interest_for', 'winner_name', 'winner_email', 'winning_bid', 'paid', 'receipt'] #NOTE: make sure this header is right


with open('2017/final.csv', 'r', newline='') as f:
	with open('2017/final_updated.csv', 'w', newline='') as g:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		writer = csv.writer(g, delimiter=',', quotechar='"')

		header = True # I can't for the life of me figure out a better way to skip the header
		for row in reader:
			if header:
				header = False
				writer.writerow(row)
				continue

			item = {key:val.encode().decode('ascii','ignore').strip() for key,val in zip(HEADER,row)}
			if not item['donor_email']:
				item['donor_email'] = parse_email(item['donor_name'], item['donor_affiliation'])
			if not item['winner_email']:
				raise ValueError('There was no winner email address provided for "{title}".'.format(**item))
			if item['paid'].lower() == "paypal":
				item['payment_mode'] = "via PayPal"
			elif item['paid']:
				item['payment_mode'] = "to "+string.capwords(item['paid'])

			if item['paid'] and not item['receipt']:
				msg = MIMEText(PAID_TEXT.format(**item))
				msg['Subject'] = PAID_SUBJECT.format(**item)
				msg['From'] = keys.EMAIL_USERNAME
				msg['To'] = "{winner_email}, {donor_email}".format(**item)
				row[-1] = time.strftime('%Y-%m-%d %H:%M:%S')

			elif not item['paid'] and REMINDING:
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
				server = smtplib.SMTP('smtp.gmail.com', '587')
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(keys.EMAIL_USERNAME, keys.EMAIL_PASSWORD)
				server.send_message(msg)
				server.quit()

			writer.writerow(row)
