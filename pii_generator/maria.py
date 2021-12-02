from mongoengine import connection
import mysql.connector
from pathlib import Path
from pydantic import BaseModel, Field
from json import load as json_load
try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION
if PRODUCTION:
    from .constants import MARIADB_EXCLUDED_DBS, PII_TABLE_SQL_QUERY, INSERT_QUERY_MARIADB
    from .utils import is_json_path_valid
else:
    from constants import MARIADB_EXCLUDED_DBS, PII_TABLE_SQL_QUERY, INSERT_QUERY_MARIADB
    from utils import is_json_path_valid


abs_path = Path(__file__).parent.absolute()

def get_maria_connection(user: str, host: str,
                         port: int, database: str, password: str):
    
    """
    this function return maria connection
    user: str = user name of database admin
    db_server_name: str = server name of database on azure
    db_port: str = database port on azure
    db_name: str = name of database
    """
    # try:
    ssl_file = f'{abs_path}/BaltimoreCyberTrustRoot.crt.pem'
    connection = mysql.connector.connect(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port,
        ssl_ca=ssl_file

    )
    return connection


# Pydentic model

class MariaConfig(BaseModel):
    """
    Have some validation
    """
    user: str = Field(...)
    password: str = Field(...)
    database: str = Field(...)
    host: str = Field(...)
    port: int = Field(...)


def get_maria_config_data_from_json(file_path: str):

    if is_json_path_valid(file_path):
        f = open(file_path)
        data = json_load(f)
        f.close()
        try:
            MariaConfig(**data)
        except Exception as e:
            return f"message: {e}"
        return data
        
    else:
        return "message: kindly enter the valid path of json"


def enter_pii_data_in_maria(file_path: str, pii_data: list):
    config_data = get_maria_config_data_from_json(file_path)
    if type(config_data) == dict:
        conn = get_maria_connection(**config_data)
        conn.autocommit = True
        cursor = conn.cursor()
        if config_data['database'] in MARIADB_EXCLUDED_DBS:
            cursor.execute("Create Database test;")
            cursor.execute("Use test;")
        try:
            cursor.execute(PII_TABLE_SQL_QUERY)
        except:
            pass

        try:
            cursor.executemany(INSERT_QUERY_MARIADB, pii_data)
            cursor.execute("SELECT * from PII;")
            print(cursor.fetchall())
            cursor.close()
            conn.close()
        except Exception as e:
            return f"message : {str(e)}"
        
        return True

    else:
        return config_data


# Insert the data in 





# s = get_maria_connection("microsec@mariaserver","mariaserver.mariadb.database.azure.com", 3306, 'test', 'admin@123')
# s.autocommit = True
# cur = s.cursor()

# database = 'test'

# # cur.execute("Drop table PII;")
# cur.execute("Use test;")
# p = PIIGenerator(how_many=4, both_credit_type=True)
# d = p.get_data_for_sql()
# print(d)
# cur.execute(PII_TABLE_SQL_QUERY)

# # # try:
# cur.executemany(INSERT_QUERY_MARIADB, d)
# cur.execute('Select * from PII;')
# print(cur.fetchall())
# except:
#     conn.rollback()



