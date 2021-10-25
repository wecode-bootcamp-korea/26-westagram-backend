import re

def validate_email(email):
    regex = re.compile(
        '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return regex.match(email)

def validate_password(password):
    regex = re.compile(
        '^(?=.*[a-zA-Z])(?=.*[!@#$%^~*+=-])(?=.*[0-9]).{8,20}')
    return regex.match(password)

def validate_phone(phone_number):
    regex = re.compile(
        '^\d{2,3}\d{3,4}\d{4}')
    return regex.match(phone_number.replace('-', ''))