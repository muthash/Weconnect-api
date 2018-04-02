import re, uuid

from smtplib import SMTPException
from flask_mail import Message
from app import mail


def validate_email(email):
    """Returns true if email is valid email format else false"""
    regex = r"(^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$)"
    if len(email) < 5 or re.match(regex, email) is None:
        return False
    return True

def validate_null(**kwargs):
    """Returns a list with invalid field messages"""
    messages = []
    for key in kwargs:
        if kwargs[key] is None:
            message = 'Please enter your {}'.format(key)
            messages.append(message)
        else:
            strip_text = re.sub(r'\s+', '', kwargs[key])
            if not strip_text:
                message = 'Please enter your {}'.format(key)
                messages.append(message)
    return messages

def random_string(string_length=8):
    """Returns a random string of length string_length"""
    random = str(uuid.uuid4())
    random = random.replace("-", "")
    return random[:string_length]

def send_reset_password(email, password):
    """Returns a random string of length string_length"""
    message = Message(
        subject='Password Reset',
        recipients=[email],
        body='Your new password is: {}'.format(password),
        html='<a href="https://github.com/muthash" target="_blank">Click link to reset password</a>'
    )
    mail.send(message)

def remove_more_spaces(user_input):
    """Maximum number os spaces between words should be one"""
    strip_text = user_input.strip()
    return re.sub(r'\s+', ' ', strip_text)


messages = {
    'account_created': 'Account created successfully',
    'exists': 'User already exists',
    'valid_email': 'Please enter a valid email address',
    'login': 'Login successfull',
    'valid_epass': 'Invalid email or password',
    'sent_mail': 'An email has been sent with your new password',
    'not_reset': 'Password was not reset. Try again',
    'password': 'Password changed successfully',
    'valid_pass': 'Invalid password',
    'valid_login': 'Please login to continue',
    'delete':'Account deleted successfully',
    'business_created': 'Business created successfully'
}