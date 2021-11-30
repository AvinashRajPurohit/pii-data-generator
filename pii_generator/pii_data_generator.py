from faker import  Faker
from .card_generator import CreditCardGenerator
import pandas as pd
import json
import os
from datetime import datetime
from mongoengine import connect
from .mongo_docs import PIIDocument
from json import loads as json_loads
from .utils import ( return_prefix_ls, 
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
        data_dict["credit_card"].append(card_gen.return_card_number(prefix_ls))
        data_dict["first_name"].append(name[0])
        data_dict["last_name"].append(name[1])
        data_dict["address"].append(fake_obj.address())
        data_dict["email"].append(fake_obj.email())
        data_dict["country"].append(fake_obj.country())
        data_dict["dob"].append(fake_obj.date())
        data_dict["blood_group"].append(return_random_blood())
        data_dict["cvv"].append(return_random_cvv())
        data_dict["height"].append(height)
        data_dict["weight"].append(weight)
        data_dict["card_type"].append(card_type)
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

  def get_data_in_json_file(self):
    """
    This function will return PII data in json file
    """
    try:
      data = self.get_data_in_dict()
      file_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'data_{str(datetime.today().time())}.json')
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
    


# p = PIIGenerator(how_many=400, both_credit_type=True)
# p.get_data_in_json_file()