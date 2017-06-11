from datetime import datetime

from django import forms

import pytz

from .utils import normalize_phone
from .validators import validate_mobile_phone


class MobileNumberField(forms.Field):
    def clean(self, value):
        super(MobileNumberField, self).clean(value)
        if value:
            validate_mobile_phone(value)
            return normalize_phone(value)
        else:
            return value


class TimeStampField(forms.Field):

    def clean(self, value):
        value = super(TimeStampField, self).clean(value)

        if not value:
            return None

        try:
            value = float(value)
        except ValueError as e:
            raise forms.ValidationError(e)

        date_time = datetime.utcfromtimestamp(value)
        date_time = date_time.replace(tzinfo=pytz.utc)

        return date_time
