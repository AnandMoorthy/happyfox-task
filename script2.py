import psycopg2.extras
import json

from utils import get_db_connection, get_gmail_service

def process_email():
    """
    This Function process the emails from the db and apply
    the rules from rules.json file.
    """
    # Getting DB Connection
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    rules = []
    # Reading rules from rules.json
    with open('rules.json', 'r') as f:
        rules = f.read()
    rules = json.loads(rules).get('rules')
    # Iterating through rules
    for rule in rules:
        rule_name = rule.get('name')
        print('Processing Rule: ', rule_name)
        condition = rule.get('condition')
        filters = rule.get('filters')
        query = query_builder(filters, condition)
        cursor.execute(query)
        email_ids = cursor.fetchall()
        email_ids = [i[0] for i in email_ids]
        print('Total Records Found', len(email_ids))
        if len(email_ids) > 0:
            actions(email_ids, rule)
        print('\n')
    return

def actions(email_ids, rule):
    """
    This is an helper function to run the actions
    specified in the rules.json
    """
    rule_name = rule.get('name')
    print('Deploying Action for Rule: ', rule_name)
    action = rule.get('action')
    action_name = action.get('name')
    apply = action.get('apply')
    addLabelIds = []
    RemoveLabelIds = []
    # looping through apply to decide on the action
    for task in apply:
        if task == 'Mark as unread':
            RemoveLabelIds.append('UNREAD')
    if action_name == 'Move Message':
        addLabelIds.append(action.get('destination'))
    service = get_gmail_service()
    body = {
        "ids": email_ids,
        "addLabelIds": addLabelIds,
        "removeLabelIds": RemoveLabelIds
    }
    try:
        service.users().messages().batchModify(
            userId="me", body=body).execute()
        print('Action Processed for Rule: ', rule_name)
        print('\n')
    except Exception as e:
        print('Got Exception', e)


def query_builder(filters, condition):
    """
    This is an helper function to build the query
    for each rules
    """
    field_mapper = {
        "From": "from_email",
        "To": "to_email",
        "Subject": "subject",
        "Date": "created_on"
    }
    query = 'where '
    for filter in filters:

        logic_raw = filter.get('logic')
        field_raw = filter.get('field')
        value = filter.get('value')
        field = field_mapper.get(field_raw)

        # For Contains case
        if logic_raw == 'contains':
            sub_query = field+" "+"like '%"+value+"%'"
        # For Equal case
        elif logic_raw == 'equal':
            sub_query = field+'='+"'"+value+"'"
        # For Date range case less than
        elif field_raw == 'Date' and logic_raw == 'less than':
            sub_query = '(NOW()::date - '+field+'::date) > '+value
        # For Date range case less than or equal
        elif field_raw == 'Date' and logic_raw == 'less than or equal':
            sub_query = '(NOW()::date - '+field+'::date) >= '+value
        # Other cases
        else:
            sub_query = ''
        if sub_query != '':
            if condition == 'all':
                sub_query = sub_query +' and '
            else:
                sub_query = sub_query +' or '
        else:
            print('Got Unhandled logic, passing', logic_raw)
            pass
        query = query + sub_query
    # Removing and/or in the end of the query if any
    query = query.removesuffix(' or ')
    query = query.removesuffix(' and ')
    query = 'select email_id from emails '+query
    return query

process_email()