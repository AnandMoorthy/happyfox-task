import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import psycopg2
import pickle

def get_db_connection():
	# Creating postgres connection here
	connection = psycopg2.connect(
		user="anand",
		password="anand123",
		host="127.0.0.1",
		port="5432",
		database="happyfox"
	)
	return connection

def get_gmail_service():
	scopes = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']
	creds = None

	# Check if the token.pickle exists
	# If exists take credentials from it
	if os.path.exists('token.pickle'):

		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# Check creds value if it's none or invalid, ask user to login
	# Login will return the credential details
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connecting Gmail API
	service = build('gmail', 'v1', credentials=creds)
	return service