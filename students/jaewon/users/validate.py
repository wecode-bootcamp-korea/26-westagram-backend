import re


def validate_email(email):
    email_pattern = re.compile("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    return bool(email_pattern.match(email))


def validate_password(password):
    password_pattern = re.compile(
        "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@!%*#?&]{8,}$"
    )
    return bool(password_pattern.match(password))
