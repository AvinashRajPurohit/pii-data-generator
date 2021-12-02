from random import Random
import decimal

try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION


if PRODUCTION:
  from .constants import *
else:
  from constants import *




def get_random_generator():
  """
  give the seeded random generator
  """
  generator = Random()
  generator.seed() 
  return generator


def return_prefix_ls(card_type: str, both_credit_type):
  """
  This function will give the perticular card list
  """
  if both_credit_type:
    generator = get_random_generator()
    card_type = generator.choice(CARDS_LIST)

  if card_type == MASTER_CARD:
    return MASTER_CARD_PREFIXS, card_type

  elif card_type == VISA:
    return VISA_PREFIXS, card_type

  else:
    return "this card type is not available"



def return_random_blood():
  """
  This function will give the random blood type
  """
  generator = get_random_generator()
  return generator.choice(BLOOD_GROUP)


def return_random_cvv():
  """
  This function will give the cvv number
  """
  generator = get_random_generator()
  num1, num2, num3 = generator.sample(range(1, 9), 3)
  return int((str(num1) + str(num2) + str(num3)))


def float_range(start, stop, step):
  """
  this function will create generator for float
  """
  while start < stop:
    yield float(start)
    start += decimal.Decimal(step)


def return_random_height_weight():
  """

  This function will give the random height and weight

  """
  generator = get_random_generator()
  height = generator.sample(list(float_range(5, 7, 0.1)), 1)[0]

  weight = generator.sample(range(50, 100), 1)[0]

  return height, weight


def return_expiry_date():
  """
  This function will give the expiry card date
  """
  generator = get_random_generator()
  month = generator.choice(MONTHS)

  year = generator.choice(YEARS)

  month =  str(month) if len(str(month)) == 2 else '0'+str(month)

  return  month+'/'+ str(year)


def is_json_path_valid(json_path: str):
  splitted = json_path.split('.')
  if splitted[-1].lower() == 'json':
    return True
  return False
  