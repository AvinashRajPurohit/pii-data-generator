# import psycopg2
# from psycopg2 import OperationalError
# from pydantic import BaseModel, Field
# from json import load as json_load
# import pyodbc


# try:
#   from production_config import PRODUCTION
# except:
#   from .production_config import PRODUCTION

  
# if PRODUCTION:
#     from .constants import MARIADB_EXCLUDED_DBS, PII_TABLE_SQL_QUERY, INSERT_QUERY_MARIADB
#     from .utils import is_json_path_valid
# else:
#     from constants import MARIADB_EXCLUDED_DBS, PII_TABLE_SQL_QUERY, INSERT_QUERY_MARIADB
#     from utils import is_json_path_valid


# def create_psql_connection_string(user: str, db_name: str,
#                                   host: str, password: str):
#     """
#     this function is responsible for creating the psql connection string
#      username: str = username of server
#      password: str = password of server
#      host: str = name of server
#      db_name: str = name of database that want to scan
#     """
#     connection_string = (f"host={host} "
#                          f"user={user} dbname={db_name} "
#                          f"password={password} sslmode=require")
#     return connection_string


# def get_psql_connection(connection_string: str):
#     """
#     this function is responsible for creating
#      connection between app and psql db
#     """
#     # try:
#     print(connection_string)
#     connection = psycopg2.connect(connection_string)
#     connection.autocommit = True
#     return connection
#     # except OperationalError as e:
#     #     return f" message :  //{e}"



# class PsqlConfig(BaseModel):
#     """
#     Have some validation
#     """
#     user: str = Field(...)
#     password: str = Field(...)
#     db_name: str = Field(...)
#     host: str = Field(...)


# def get_psql_config_data_from_json(file_path: str):

#     if is_json_path_valid(file_path):
#         f = open(file_path)
#         data = json_load(f)
#         f.close()
#         try:
#             PsqlConfig(**data)
#         except Exception as e:
#             return f"message: {e}"
#         return data
        
#     else:
#         return "message: kindly enter the valid path of json"



# def enter_pii_data_in_psql(file_path: str, pii_data: list):
#     config_data = get_psql_config_data_from_json(file_path)
#     if type(config_data) == dict:
#         conn_str  = create_psql_connection_string(**config_data)
#         conn = get_psql_connection(conn_str)
#         cursor = conn.cursor()
#         if config_data['db_name'] in MARIADB_EXCLUDED_DBS:
#             cursor.execute("Create Database test;")
#             print('test database has been created...')
#             cursor.execute("Use test;")
#         try:
#             cursor.execute(PII_TABLE_SQL_QUERY)
#         except:
#             pass

#         try:
#             cursor.executemany(INSERT_QUERY_MARIADB, pii_data)
#             cursor.execute("SELECT * from PII;")
#             print(cursor.fetchall())
#             cursor.close()
#             conn.close()
#         except Exception as e:
#             return f"message : {str(e)}"
        
#         return True

#     else:
#         return config_data

# def get_odbc_string(server: str, database: str, username: str,
#                     password: str):
#     """
#     this function will return odbc connection string
#     server_name: str = name of the server
#     database: str = name of the database
#     username: str = username of the database
#     password: str = password of the database
#     driver: str  = version of oracle driver
#     """
#     pwd = f'{password}'
#     driver = '{ODBC Driver 17 for SQL Server}'
#     connection_string = (f'Driver={driver};Server=tcp:{server};'
#                          f'Database={database};Uid={username};Pwd={pwd};'
#                          f'Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;')
#     return connection_string

# # def get_sql_db_client(connection_string: str):
# #   """
# #   This function will return the sql db client
# #   connection_string: str
# #   """
# #   # try:
# #   conn: pyodbc.Connection = pyodbc.connect(connection_string)
# #   cursor: pyodbc.Cursor = conn.cursor()
# #   # except Exception as e:
# #   #     return e
# #   return cursor

# # f = open("/Users/deepak9636/Drive/msec/pii-generator-develop/config_example/azure_sql.json")
# # import json
# # d = json.load(f)
# # f.close()
# # print(d)
# # cs = get_odbc_string(**d)
# # print(cs)
# # con = get_sql_db_client(cs)
# # print(con)