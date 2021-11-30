import argparse
import sys 
from pprint import pprint
from .pii_data_generator import PIIGenerator

def get_cli_pii_data(args):
  """
  This function will parse all the arguments
  """
  use_all = False
  if args.a == "yes" or args.a == 'y':
    use_all = True
  pii_gen = PIIGenerator(args.n, args.c, use_all)
  # try:
  if args.conn != None:
    print(args.conn)
    pii_gen.insert_data_in_mongo(args.conn)
    print("*************" * 5)
    print("Data Inserted successfully")
    pii_gen.get_data_in_json_file()
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
  
  args = parser.parse_args()

  # sys.stdout.write(str(get_cli_pii_data(args)))
  print("============"*5)
  pprint(get_cli_pii_data(args))


