### Steps to run the script

1. Open Command Line
2. Create Virutal Env(Follow: https://docs.python.org/3/library/venv.html)
3. Run pip install -r requirements.txt
4. Login to Google Developer Console and create app and download credentials.json
5. DB Setup 
    1. Create database in postgresql named happyfox
    2. Create table in the database happyfox         
        1. create table emails (id serial not null, email_id varchar(50) not null, from_email text, to_email text, subject text, created_on date);
6. Run script1.py to download the number of emails and store in the DB
7. Run script2.py to apply the rules and actions from rules.json to the data we stored in the DB
    
