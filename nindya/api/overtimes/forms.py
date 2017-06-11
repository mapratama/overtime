from django import forms

from nindya.apps.overtimes.models import Overtime
from nindya.core.fields import TimeStampField
from nindya.core.notifications import (send_coordinator_notification,
                                       send_manager_notification,
                                       send_accepted_coordinator_notification,
                                       send_accepted_manager_notification)


class AddOvertimeForm(forms.Form):
    start = TimeStampField()
    end = TimeStampField()
    description = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(AddOvertimeForm, self).__init__(*args, **kwargs)

    def save(self, user, *args, **kwargs):
        overtime = user.overtimes.create(
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'],
            description=self.cleaned_data['description'],
        )

        send_coordinator_notification()

        return overtime


class ApprovedCoordinatorForm(forms.Form):

    overtime = forms.ModelChoiceField(queryset=None)
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(ApprovedCoordinatorForm, self).__init__(*args, **kwargs)
        self.fields['overtime'].queryset = Overtime.objects.filter(status=Overtime.STATUS.bid)

    def save(self, user):
        overtime = self.cleaned_data['overtime']
        overtime.status = Overtime.STATUS.approved_coordinator
        overtime.notes_coordinator = self.cleaned_data['notes']
        overtime.save()

        send_manager_notification()
        send_accepted_coordinator_notification(overtime)

        return overtime


class ApprovedManagerForm(forms.Form):

    overtime = forms.ModelChoiceField(queryset=None)
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(ApprovedManagerForm, self).__init__(*args, **kwargs)
        self.fields['overtime'].queryset = \
            Overtime.objects.filter(status=Overtime.STATUS.approved_coordinator)

    def save(self, user):
        overtime = self.cleaned_data['overtime']
        overtime.status = Overtime.STATUS.approved_manager
        overtime.notes_manager = self.cleaned_data['notes']
        overtime.save()

        send_accepted_manager_notification(overtime)

        return overtime
