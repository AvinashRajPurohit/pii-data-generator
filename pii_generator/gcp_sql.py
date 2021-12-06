import pytds
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



def get_sql_connection(config: dict):
    """
    this function is responsible for creating
     connection between app and psql db
    """
    # try:
    cnxn = pytds.connect(**config)
    cnxn.autocommit = True
    return cnxn
    # except OperationalError as e:
    #     return f" message :  //{e}"



class SqlConfig(BaseModel):
    """
    Have some validation
    """
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)
    host: str = Field(...)


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



def enter_pii_data_in_gcp_sql(file_path: str, pii_data: list):
    config_data = get_sql_config_data_from_json(file_path)
    if type(config_data) == dict:
        conn = get_sql_connection(**config_data)
        cursor = conn.cursor()
        if config_data['db_name'] in MARIADB_EXCLUDED_DBS:
            cursor.execute("Create Database test;")
            print('test database has been created...')
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
