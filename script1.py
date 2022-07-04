# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import psycopg2

from utils import get_db_connection, get_gmail_service


def getEmails(count):
	"""
	This Function get the list of emails from the logged in user
	and dump it into the postgres database
	"""
	service = get_gmail_service()

	# Get all the messages, maxResult variable can be modified to get
	# n numbers of result
	result = service.users().messages().list(maxResults=email_count, userId='me').execute()
	messages = result.get('messages')

	#Getting DB Connection
	connection = get_db_connection()
	cursor = connection.cursor()

	#Iterating through messages
	print('Processing Emails')
	for msg in messages:
		# Get the message from its id
		email_id = msg.get('id')
		txt = service.users().messages().get(userId='me', id=email_id).execute()

		try:
			payload = txt.get('payload', {})
			headers = payload.get('headers')

			subject = None
			sender = None
			receiver = None
			date = None
			for d in headers:
				if d['name'] == 'Subject':
					subject = d.get('value')
				if d['name'] == 'From':
					sender = d.get('value')
				if d['name'] == 'To':
					receiver = d.get('value')
				if d['name'] == 'Date':
					date = d.get('value')
					date = date.removesuffix(' (UTC)')
				
			
			insert_query = '''
			INSERT INTO emails (email_id, from_email, to_email, subject, created_on) VALUES (%s, %s, %s, %s, %s)'''
			items_tuple = (str(email_id), str(sender), str(receiver), str(subject), str(date))
			try:
				cursor.execute(insert_query, items_tuple)
			except (Exception, psycopg2.Error) as error:
				print("Error while connecting to PostgreSQL", error)
				return
		except Exception as e:
			print('Got Exception', e)
			return
	# Commiting only if there is no exception raised duing the loop
	connection.commit()
	return

email_count = input('Enter number of emails to process: ')
getEmails(email_count)
