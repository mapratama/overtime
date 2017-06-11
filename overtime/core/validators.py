from django.core.exceptions import ValidationError

from id_phonenumbers import parse

from phonenumbers import phonenumberutil


def validate_mobile_phone(phone_number):
    try:
        number = parse(phone_number)
    except phonenumberutil.NumberParseException:
        raise ValidationError('Please enter a valid mobile phone number.')

    if number.is_mobile:
        return True

    raise ValidationError('Please enter a valid mobile phone number.')
