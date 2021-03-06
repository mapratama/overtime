from dateutil import parser
from dateutil.relativedelta import relativedelta

from django import forms
from django.utils import timezone

from overtime.apps.users.models import User
from overtime.core.fields import MobileNumberField
from overtime.core.notifications import (send_need_approval_notification,
                                         send_new_forgets_notification)


class APIRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    no_file = forms.CharField()
    type = forms.IntegerField(required=False)
    department = forms.IntegerField()
    position = forms.CharField(required=False)
    name = forms.CharField(max_length=30)
    mobile_number = MobileNumberField()
    push_notification_key = forms.CharField(max_length=254, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return email

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if User.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("User with this mobile number already exists")
        return mobile_number

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')

        try:
            birthday = parser.parse(birthday).date()
        except ValueError:
            raise forms.ValidationError("%s is not right formatted" % birthday)

        if birthday > timezone.now().date() - relativedelta(years=12):
            raise forms.ValidationError("Minimum age is 12 years")

        if birthday.year < 1900:
            raise forms.ValidationError("Birthday can't registered")

        return birthday

    def clean_name(self):
        return self.cleaned_data['name'].title()

    def save(self, *args, **kwargs):
        user = User.objects.create(
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name'],
            no_file=self.cleaned_data['no_file'],
            department=self.cleaned_data['department'],
            mobile_number=self.cleaned_data['mobile_number'],
            push_notification_key=self.cleaned_data['push_notification_key'],
            is_active=False,
            has_been_activated=False
        )
        user.set_password(self.cleaned_data['password'])

        if self.cleaned_data['type']:
            user.type = self.cleaned_data['type']

        if self.cleaned_data['position']:
            user.position = self.cleaned_data['position']

        send_need_approval_notification()
        user.save()

        return user


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()

        if self.errors:
            return cleaned_data

        email = cleaned_data['email'].lower().strip()
        users = User.objects.filter(email=email)
        if not users.exists():
            raise forms.ValidationError("Maaf email tidak ditemukan")

        self.user = users.first()

        return cleaned_data

    def save(self):
        forget = self.user.forgets.create()
        send_new_forgets_notification()

        return forget
