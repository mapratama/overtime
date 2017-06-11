import os

from django.contrib.auth import login
from django.template.defaultfilters import slugify
from django.utils import timezone

import phonenumbers


class FilenameGenerator(object):
    """
    Utility class to handle generation of file upload path
    """
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, instance, filename):
        today = timezone.localtime(timezone.now()).date()

        filepath = os.path.basename(filename)
        filename, extension = os.path.splitext(filepath)
        filename = slugify(filename)

        path = "/".join([
            self.prefix,
            str(today.year),
            str(today.month),
            str(today.day),
            filename + extension
        ])
        return path


try:
    from django.utils.deconstruct import deconstructible
    FilenameGenerator = deconstructible(FilenameGenerator)
except ImportError:
    pass


def normalize_phone(number):
    number = number[1:] if number[:1] == '0' else number
    parse_phone_number = phonenumbers.parse(number, 'ID')
    phone_number = phonenumbers.format_number(
        parse_phone_number, phonenumbers.PhoneNumberFormat.E164)
    return phone_number


def force_login(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
