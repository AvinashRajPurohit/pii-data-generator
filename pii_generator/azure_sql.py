import pytds
from pydantic import BaseModel, Field
from json import load as json_load
from pathlib import Path
try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION
abs_path = Path(__file__).parent.absolute()

  
if PRODUCTION:
    from .constants import MARIADB_EXCLUDED_DBS, SQL_QUERY, INSERT_QUERY_MARIADB
    from .utils import is_json_path_valid
else:
    from constants import MARIADB_EXCLUDED_DBS, SQL_QUERY, INSERT_QUERY_MARIADB
    from utils import is_json_path_valid



def get_sql_connection(config: dict):
    """
    this function is responsible for creating
     connection between app and psql db
    """
    try:
        print(config)
        print('here', '*******************')
        ssl_file = f'{abs_path}/BaltimoreCyberTrustRoot.crt.pem'
        config['cafile'] = ssl_file
        config['validate_host'] = False
        print(config)
        cnxn = pytds.connect(**config)
        cnxn.autocommit = True
        return cnxn
    except Exception as e:
        return f" message :  //{e}"



class SqlConfig(BaseModel):
    """
    Have some validation
    """
    user: str = Field(...)
    password: str = Field(...)
    database: str = Field(...)
    server: str = Field(...)
    port: str = None


def get_sql_config_data_from_json(file_path: str):

    if is_json_path_valid(file_path):
        f = open(file_path)
        data = json_load(f)
        f.close()
        try:
            SqlConfig(**data)
        except Exception as e:
            return f"message: {e}"
        return data
        
    else:
        return "message: kindly enter the valid path of json"



def enter_pii_data_in_azure_sql(file_path: str, pii_data: list):
    config_data = get_sql_config_data_from_json(file_path)
    if type(config_data) == dict:
        print(config_data, '------')
        conn = get_sql_connection(config_data)
        print(conn)
        cursor = conn.cursor()
        if config_data['database'] in MARIADB_EXCLUDED_DBS:
            cursor.execute("Create Database test;")
            print('test database has been created...')
            cursor.execute("Use test;")
        try:
            cursor.execute(SQL_QUERY)
        except Exception as e:
            print(e)
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
