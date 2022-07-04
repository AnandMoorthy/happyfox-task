### Steps to run the script

1. Open Command Line
2. Clone this repo
3. Create Virutal Environment(Follow: https://docs.python.org/3/library/venv.html) and activate
4. Run `pip install -r requirements.txt` to install the dependencies
5. Login to Google Developer Console and create Gmail API app and download credentials.json and move it to this folder
6. Setup DB 
    1. Create database in postgresql named happyfox
    2. Create table in the database happyfox         
        1. RUN `create table emails (id serial not null, email_id varchar(50) not null, from_email text, to_email text, subject text, created_on date);`
7. Modify the `rule.json` file as required
8. Run `python script1.py` and enter the number of email to process to download and store in the DB
9. Run `python script2.py` to apply the rules and actions from rules.json to the data we stored in the DB

### TODO

#### There are Multiple features can be added in the future
1. Support more rules and actions in the code
2. Batch Insert can be performed in script1.py to improve the insertion speed
3. GIN Index can be added to email_id, from_email, to_email, subject to make the search faster.
    
