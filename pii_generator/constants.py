from datetime import datetime

MASTER_CARD_PREFIXS = [
        ['5', '1'],
        ['5', '2'], 
        ['5', '3'], 
        ['5', '4'], 
        ['5', '5']
      ]

VISA_PREFIXS = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

VISA = 'visa'
MASTER_CARD = 'master card'

BLOOD_GROUP = ['A+', 'A-', 'B+', 'B-', "O+", "O-", "AB+", "AB-"]

MONTHS = list(range(1, 13))

YEARS = list(range(datetime.today().year, datetime.today().year + 14))

CARDS_LIST = [VISA, MASTER_CARD]