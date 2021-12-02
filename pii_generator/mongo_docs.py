from mongoengine import (Document, 
                         StringField, 
                         DateTimeField, 
                         IntField, 
                         FloatField)

from datetime import datetime

from mongoengine.fields import EmailField



class PIIDocument(Document):
    """
    Mongo document for PII Information
    """
    first_name = StringField()
    last_name = StringField()
    address = StringField()
    country = StringField()
    dob = DateTimeField()
    credit_card = StringField()
    card_type = StringField()
    cvv = IntField()
    height = FloatField()
    weight = IntField()
    email = EmailField()
    blood_group = StringField()
    expiry_data = StringField()
    updated_at = DateTimeField(default=str(datetime.now()))
    created_at = DateTimeField(default=str(datetime.now()))
