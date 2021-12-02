try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION
import argparse
from pprint import pprint

if PRODUCTION:
  from .pii_data_generator import PIIGenerator
  from .constants import AZURE_DATABASES, GCP_DATABASES
else:
  from pii_data_generator import PIIGenerator
  from constants import AZURE_DATABASES, GCP_DATABASES



def get_cli_pii_data(args):
  """
  This function will parse all the arguments
  """
  use_all = False
  print(args)
  if args.a == "yes" or args.a == 'y':
    use_all = True
  pii_gen = PIIGenerator(args.n, args.c, use_all)
  # try:
  if args.conn != None:
    print(args.conn)
    pii_gen.insert_data_in_mongo(args.conn)
    print("*************" * 5)
    print("Data Inserted successfully")
  if args.filepath != None:
    s = pii_gen.get_data_in_json_file(args.filepath)
    print(str(s), "status of data insert")

  if args.cl.lower() == 'yes' or args.cl.lower() == 'y':


    if args.cloud_name.lower() == 'azure':

      if args.db_type == None:
        return "message: kindly select the db type in azure available are ['maria', 'sql', 'mysql', 'psql']"

      elif args.db_type.lower() in AZURE_DATABASES:

        # Maria db
        if args.db_type.lower() == 'maria':
          if args.json_path  == None:
            return "message: kindly add the path of database config file json for azure maria database"
          else:
            print('maria database')
            suc = pii_gen.insert_pii_data_in_azure_maria_db(args.json_path)
            return suc
                    # Mysql db
        elif args.db_type.lower() == 'mysql':
          
          if args.json_path  == None:
            return "message: kindly add the path of database config file json for azure mysql database"
          else:
            print('mysql database')
            suc = pii_gen.insert_pii_data_in_azure_mysql_db(args.json_path)
            return suc
        # Azure Psql
        elif args.db_type.lower() == 'psql':
            
          if args.json_path  == None:
            return "message: kindly add the path of database config file json for azure psql database"
          else:
            print('psql database')
            suc = pii_gen.insert_pii_data_in_azure_psql_db(args.json_path)
            return suc
        else:
          return f"message: database {args.db_type} is not available in azure available are ['maria', 'sql', 'mysql', 'psql']"

      else:
        return f"message: database {args.db_type} is not available in azure available are ['maria', 'sql', 'mysql', 'psql']"


    else:
      return f"message: cloud {args.cloud_name} is not available, available are ['azure', 'gcp']"





  return pii_gen.get_data_in_dict()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--n',
                      type=int, 
                      default=10,
                      help="number of PII data rows")

  parser.add_argument('--c',
                      type=str, 
                      default='visa',
                      help="select the card type availabel cards (visa, master card)")

  parser.add_argument('--a',
                      type=str, 
                      default='no',
                      help="if you want to use all card types Use 'yes'/'y' ")
  
  parser.add_argument('--conn',
                      type=str, 
                      default=None,
                      help="if you want to insert this data in Mongo database kindly enter the correct connection string")
  
  parser.add_argument('--filepath',
                      type=str, 
                      default=None,
                      help="if you want data in json file than provide the path where you want it.")
  
  parser.add_argument('--cl',
                      type=str,
                      default='no',
                      help="If you want to insert data in cloud's database than enter yes/y ")
                      
  parser.add_argument('--cloud_name',
                      type=str,
                      default=None,
                      help="Enter the cloud name available clouds are [azure, gcp]")
                                          
  parser.add_argument('--db_type',
                      type=str,
                      default=None,
                      help="Enter the db_type name available clouds are Azure = ['maria', 'sql', 'mysql', 'psql'] GCP=[sql, mysql, psql]")

  parser.add_argument('--json_path',
                      type=str,
                      default=None,
                      help="enter the config file path that have the credentials of database (file format json is needed)")

  
  args, unknown = parser.parse_known_args()

  print("============"*5)
  pprint(get_cli_pii_data(args))


print(main())