# pii-data-generator

```
A simple "Personally identifiable information" (PII) Data Generator for both programmers and non programmers...
```

Built with ❤︎ and :coffee: in one night by  [Deepak Rajpurohit](https://github.com/AvinashRajPurohit)

---

[![GitHub](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/OmkarPathak/pyresparser/blob/master/LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) 
[![Build Status](https://travis-ci.com/OmkarPathak/pyresparser.svg?branch=master)](https://travis-ci.com/OmkarPathak/pyresparser)


# Features
#### Generate Data of PII like :
- Generate Cradit-Card (Visa/Master-card)
- Generate email
- Generate mobile numbers
- Generate First Name
- Generate Last Name
- Generate Address
- Generate Country
- Generate Weight/Height
- Generate CVV number
- Generate Card - Expiry Date


# Installation

- You can install this package using

```bash
pip install pii-data-generator
```
- after installing package 

# Usage

#### For Non-Programmers usage / CLI:
* write pii command that will generate for 10 persons and store them in json file 
* for more data generation use ```pii --n 400``` this will generate 400 PII person data with "visa" credit card
* if you want to generate master cards ```pii --n 400  --c master card``` this will generate  400 PII data with master card
* if you want both cards types than use ```pii --n 400  --a yes```

* if you want to insert this data in mongodb ```pii --n 400  --a yes --conn <mongo-db connection string>```

```bash
# PII
pii --n 100 --a yes

# insert data in mongodb
pii --n 400  --a yes --conn <mongo-db connection string>
```

#### For Programmers usage:
```bash
from pprint import pprint
from pii_generator.pii_data_generator import PIIGenerator

pii_gen = PIIGenerator(100, 'visa', True)

# this will give you data in dictionary format
pprint(pii_gen.get_data_in_dict())

# this will give you data in json format
pii_gen.get_data_in_json()

# this will give you data in json file on desktop
pii_gen.get_data_in_json_file()


# this will give you data in pandas data frame
pii_gen.get_data_in_df()


# this will Insert pii data in data in mongodb
pii_gen.insert_data_in_mongo(connection_string)


```
#### Thank you 