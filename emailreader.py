import imaplib
import email
from email.header import decode_header
import webbrowser
import os

#https://www.thepythoncode.com/article/reading-emails-in-python

e = "crimealertbot@gmail.com"
pw = "3imajimI"

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(e,pw)

status, messages = imap.select("INBOX")
N=3
messages=int(messages[0])

for i in range(messages, messages-N, -1):
	# fetch the email message by ID
	res, msg = imap.fetch(str(i), "(RFC822)")
	for response in msg:
		if isinstance(response, tuple):
			# parse a bytes email into a message object
			msg = email.message_from_bytes(response[1])
			# decode the email subject
			subject = decode_header(msg["Subject"])[0][0]
			if isinstance(subject, bytes):
				# if it's a bytes, decode to str
				subject = subject.decode()
			# email sender
			from_ = msg.get("From")
			print("Subject:", subject)
			print("From:", from_)
			if msg.is_multipart():
				# iterate over email parts
				for part in msg.walk():
					content_type = part.get_content_type()
					content_disposition = str(part.get("Content-Disposition"))
					try:
						# get the email body
						body = part.get_payload(decode=True).decode()
					except:
						pass
					if content_type == "text/plain":
						print(body)
				print("="*100)
			else:
				# if the email message is multipart
				content_type = msg.get_content_type()
				# get the email body
				body = msg.get_payload(decode=True).decode()
				if content_type == "text/plain":
					# print only text email parts
					print(body)
				if content_type == "text/html":
					# if it's HTML, create a new HTML file and open it in browser
					pass
				print("="*100)

imap.close()
imap.logout()