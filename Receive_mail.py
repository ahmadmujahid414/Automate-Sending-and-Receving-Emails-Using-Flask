import imaplib, email, os
from config import Config
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

user = 'techdiv07@gmail.com'
password = '$mak123456'

imap_url = 'imap.gmail.com'
attachment_dir = 'E:/Python/fedral organization Python developer task/Task#1 Server End Coding using Flask/Attachments'


def get_unseen_mail():
	con = imaplib.IMAP4_SSL(imap_url)
	con.login(user,password)
	con.select('INBOX')
	result, search_data = con.search(None,'UNSEEN')
	my_message = []
	for num in search_data[0].split():
		email_data = {}
		d, data = con.fetch(num,'(RFC822)')
		s, b = data[0]
		email_message = email.message_from_bytes(b)
		for header in ['subject','to','from','date']:
			email_data[header] = email_message[header]
		for part in email_message.walk():
			if part.get_content_type() == "text/plain":
				body = part.get_payload(decode=True)
			elif part.get_content_type() == "text/html":
				html_body = part.get_payload(decode=True)
				email_data['html_body'] = html_body.decode()
		my_message.append(email_data)
	con.close()
	return my_message

def get_mail_attachments(msg):
	for part in msg.walk():
		if part.get_content_maintype() == "multipart":
			continue
		if part.get('Content-Disposition') is None:
			continue
		fileName = part.get_filename()
	
		if bool(fileName):
			filePath = os.path.join(attachment_dir,fileName)
			with open(filePath,'wb') as f:
				f.write(part.get_payload(decode=True))
			return True
		else:
			return False

def search_mail():
	con = imaplib.IMAP4_SSL(imap_url)
	con.login(user,password)
	con.select('INBOX')
	result, search = con.search(None,'UNSEEN')
	return search

def save_data():
	data = pd.read_csv('E:/Python/fedral organization Python developer task/Task#1 Server End Coding using Flask/Attachments/order.csv')
	conn = sqlite3.connect('flask_DB.db')
	c = conn.cursor()
	c.execute("INSERT INTO records VALUES(?, ?, ?,?)",(data['mail_from'][0],data['data'][0],data['mail_to'][0],'n')  )
	conn.commit()
	conn.close()
	return True


def download():
	con = imaplib.IMAP4_SSL(imap_url)
	con.login(user,password)
	con.select('INBOX')
	message_id = search_mail()[0]
	try:
		result, data = con.fetch(message_id,'(RFC822)')
		raw = email.message_from_bytes(data[0][1])
	except:
		return False
	if bool(get_mail_attachments(raw)):
		con.close()
		return True
	else:
		con.store(message_id,'-FLAGS','(\Seen)')
		con.close()
		return False		
 
def reply_mail():
	my_inbox = get_unseen_mail()
	try:
		body = my_inbox[0]
		soup = BeautifulSoup(body['html_body'],'lxml')
		text = soup.find('div').text
		return text
	except:
		return False
