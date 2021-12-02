from datetime import datetime

MASTER_CARD_PREFIXS = [
        ['5', '1'],
        ['5', '2'], 
        ['5', '3'], 
        ['5', '4'], 
        ['5', '5']
      ]

VISA_PREFIXS = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

VISA = 'visa'
MASTER_CARD = 'master card'

BLOOD_GROUP = ['A+', 'A-', 'B+', 'B-', "O+", "O-", "AB+", "AB-"]

MONTHS = list(range(1, 13))

YEARS = list(range(datetime.today().year, datetime.today().year + 14))

CARDS_LIST = [VISA, MASTER_CARD]


MARIADB = 'maria'
MYSQL = 'msql'
POSTGRES = 'psql'
SQL = 'sql'

MARIADB_EXCLUDED_DBS = ['information_schema', 'mysql', 'performance_schema']

PSQL_EXCLUDED_DBS = ["information_schema", "mysql", "performance_schema", "sys", "postgres", "azure_maintenance", "azure_sys"]


PII_TABLE_SQL_QUERY = ( "CREATE TABLE if not exists PII ("
                        "first_name VARCHAR(255),"
                        "last_name VARCHAR(255),"
                        "address VARCHAR(255),"
                        "email VARCHAR(255),"
                        "country VARCHAR(255),"
                        "dob VARCHAR(255),"
                        "credit_card VARCHAR(255),"
                        "card_type VARCHAR(255),"
                        "cvv INTEGER,"
                        "height REAL,"
                        "weight INTEGER,"
                        "blood_group VARCHAR(255),"
                        "expiry_data VARCHAR(255))")



INSERT_QUERY_MARIADB = """ insert into PII (
first_name, last_name, address, email, country, dob, credit_card, card_type, cvv, expiry_data, height, weight, blood_group) 
values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)           
"""


AZURE_DATABASES = ['maria', 'sql', 'mysql', 'psql']

GCP_DATABASES = ["sql", "mysql", "psql"]