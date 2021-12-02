import os
import json
import pandas as pd
from faker import  Faker
from datetime import datetime
from mongoengine import connect
from json import loads as json_loads

try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION


if PRODUCTION:
  from .mongo_docs import PIIDocument
  from .card_generator import CreditCardGenerator
  from .utils import ( return_prefix_ls, 
                      return_random_blood,
                      return_random_cvv,
                      return_random_height_weight,
                      return_expiry_date )
  from .maria import enter_pii_data_in_maria
  from .mysql_config import enter_pii_data_in_mysql
  from .psql_config import enter_pii_data_in_psql

else:

  from mongo_docs import PIIDocument
  from card_generator import CreditCardGenerator
  from maria import enter_pii_data_in_maria
  from mysql_config import enter_pii_data_in_mysql
  from psql_config import enter_pii_data_in_psql


  from utils import ( return_prefix_ls, 
                      return_random_blood,
                      return_random_cvv,
                      return_random_height_weight,
                      return_expiry_date )
  



class PIIGenerator(object):

  def __init__(self,
               how_many: int = 10,
               credit_card_type: str = 'visa',
               both_credit_type: bool = False
              ):
      super().__init__()
      self.how_many = how_many
      self.credit_card_type = credit_card_type
      self.faker = Faker()
      self.both_credit_type = both_credit_type


  def return_dummy_pii_data(self):
    
    """
    this function will return dummy pii data 
    fake_obj : Faker Object
    how_many : int = how many data rows you want
    """
    try:

      fake_obj = self.faker

      card_gen = CreditCardGenerator(16, self.how_many)

      data_dict = {
                "first_name": [],
                "last_name": [],
                "address": [],
                "email": [],
                "country": [],
                "dob": [],
                "credit_card": [],
                "card_type": [],
                "cvv": [],
                "expiry_data": [],
                "height": [],
                "weight": [],
                "blood_group": []
            }


      for i in range(0, self.how_many): 
        prefix_ls, card_type = return_prefix_ls(self.credit_card_type, self.both_credit_type)
        if type(prefix_ls) == str:
          return prefix_ls
        name = fake_obj.name().split()
        height, weight = return_random_height_weight()
        data_dict["first_name"].append(name[0])
        data_dict["last_name"].append(name[1])
        data_dict["address"].append(fake_obj.address())
        data_dict["email"].append(fake_obj.email())
        data_dict["country"].append(fake_obj.country())
        data_dict["dob"].append(fake_obj.date())
        data_dict["blood_group"].append(return_random_blood())
        data_dict["height"].append(height)
        data_dict["weight"].append(weight)
        data_dict["card_type"].append(card_type)
        data_dict["credit_card"].append(card_gen.return_card_number(prefix_ls))
        data_dict["cvv"].append(return_random_cvv())
        data_dict["expiry_data"].append(return_expiry_date())
      return data_dict

    except Exception as e:
      return {f"message: something went wrong // {e}"}


  # class method return pandas dataframe
  def get_data_in_df(self):
    """
    This function will return PII data in Pandas Dataframe
    """
    try:
      return pd.DataFrame(self.return_dummy_pii_data())

    except Exception as e:
      return {f"message: something went wrong // {e}"}


  # class method return dict
  def get_data_in_dict(self):
    """
    This function will return PII data in dict
    """
    try:
      return self.get_data_in_df().to_dict('records')

    except Exception as e:
      return {f"message: something went wrong // {e}"}


  # class method return json
  def get_data_in_json(self):
    """
    This function will return PII data in json
    """
    try:
      return json_loads(self.return_dummy_pii_data())

    except Exception as e:
      return {f"message: something went wrong // {e}"}

  def get_data_in_json_file(self, json_path):
    """
    This function will return PII data in json file
    json_path: where you want that file
    """
  
    try:
      data = self.get_data_in_dict()
      file_path = os.path.join(json_path, f'data_{str(datetime.today().time())}.json')
      with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()
      return f"data imported in json successfully // {file_path}"

    except Exception as e:
      return {f"message: something went wrong // {e}"}


  # class method data insert in mongo
  def insert_data_in_mongo(self, connection_str: str):
    """
    This function will insert data in any mongo database using connection string
    connection_str: str = Mongo
    """
    try:

      data = self.get_data_in_dict()
      con = connect(host=connection_str)

      print("++++++++++++++++++++++++++++++++++++++ Connection Has been"
       " Established +++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      mongo_docs = []
      for p in data:
        mongo_docs.append(PIIDocument(**p))
      PIIDocument.objects.insert(mongo_docs)
      con.close()
      return "data has been successfully added"

    except Exception as e:
      return e


  def get_data_for_sql(self):
    """
    This function will return PII data in 
    """
    try:
      return self.get_data_in_df().values.tolist()

    except Exception as e:
      return {f"message: something went wrong // {e}"}

  
  def insert_pii_data_in_azure_maria_db(self, config_file_path: str):
    """
    This function will insert PII data in Azure Maria db
    """
    try:
      pii_data = self.get_data_for_sql()
      insert_data = enter_pii_data_in_maria(config_file_path, pii_data)
      if type(insert_data) == bool:
        return "message: Data has been inserted successfully"
      return insert_data
    except Exception as e:
      return {f"message: something went wrong // {e}"}


  def insert_pii_data_in_azure_mysql_db(self, config_file_path: str):
    """
    This function will insert PII data in Azure Mysql db
    """
    try:
      pii_data = self.get_data_for_sql()
      insert_data = enter_pii_data_in_mysql(config_file_path, pii_data)
      if type(insert_data) == bool:
        return "message: Data has been inserted successfully"
      return insert_data
    except Exception as e:
      return {f"message: something went wrong // {e}"}


  def insert_pii_data_in_azure_psql_db(self, config_file_path: str):
    """
    This function will insert PII data in Azure Mysql db
    """
    try:
      pii_data = self.get_data_for_sql()
      insert_data = enter_pii_data_in_psql(config_file_path, pii_data)

      if type(insert_data) == bool:
        return "message: Data has been inserted successfully"
      return insert_data
      
    except Exception as e:
      return {f"message: something went wrong // {e}"}




# p = PIIGenerator(how_many=400, both_credit_type=True)
# print(p.get_data_in_dict())