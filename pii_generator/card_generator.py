#!/usr/bin/python
# -*- coding: utf-8 -*-


"""

this file will handle all the function related to credit card...
some part of this file inspired from https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py

"""
import copy
try:
  from production_config import PRODUCTION
except:
  from .production_config import PRODUCTION
if PRODUCTION:
  from .utils import get_random_generator
else:
  from utils import get_random_generator


  
class CreditCardGenerator(object):

  def __init__(self,
    size: int,
    how_many: int,):
    super().__init__()
    self.size = size
    self.random_generator = get_random_generator()
    self.how_many = how_many

  @staticmethod
  def card_comp_number(prefix, size, random_generator):
    """
    prefix: type of card prefixs
    size: card number lenght
    """

    # make card numbers
    cc_number = prefix

    while len(prefix) < (size-1):
      digit = str(random_generator.choice(range(0, 10)))
      cc_number.append(digit)

    sum = 0
    pos = 0

    reversed_cc_number = []
    reversed_cc_number.extend(cc_number)
    reversed_cc_number.reverse()
    
    while pos < size - 1:

      odd = int(reversed_cc_number[pos]) * 2

      if odd > 9:
        odd -= 9

      sum += odd

      if pos != (size-2):
          sum += int(reversed_cc_number[pos + 1])
        
      pos += 2

    check_digit = ((sum / 10 +1) * 10 - sum) % 10

    cc_number.append(str(check_digit))
    
    return  ''.join(cc_number) 


  @staticmethod
  def convert_number_into_format(card_number: str):
    """
    this function will convert numbers into card formates
    card_number: int = number of card
    """
    final_str = ''
    counter = 0
    for i in range(4, len(card_number)+5, 4):
      final_str += ' ' + card_number[counter:i]
      counter+=4
    return final_str[1:-1]


  def return_card_number(self, prefix_ls):
    """
    This function will return perticular cradit card number
    """

    cc_number = copy.copy(self.random_generator.choice(prefix_ls))
    generated_num =self.card_comp_number(cc_number, self.size, self.random_generator)
    num = generated_num.split('.')[0]

    if len(num)%4 != 0:
      return "message: kindly use 16 lenght"
    
    return self.convert_number_into_format(num)





