from django import forms

from overtime.apps.overtimes.models import Overtime
from overtime.apps.users.models import User
from overtime.core.fields import TimeStampField
from overtime.core.notifications import (send_coordinator_notification,
                                         send_manager_notification,
                                         send_accepted_coordinator_notification,
                                         send_accepted_manager_notification,
                                         send_canceled_notification,
                                         send_new_overtime_notification)


class AddOvertimeForm(forms.Form):
    user = forms.ModelChoiceField(queryset=None, required=False)
    start = TimeStampField()
    end = TimeStampField()
    description = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, user, *args, **kwargs):
        super(AddOvertimeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['user'].queryset = User.objects.exclude(id=user.id)\
            .filter(department=user.department)

    def save(self, *args, **kwargs):
        selected_user = self.cleaned_data['user']
        type = self.user.type
        if selected_user:
            self.user = selected_user

        overtime = self.user.overtimes.create(
            start=self.cleaned_data['start'],
            end=self.cleaned_data['end'],
            description=self.cleaned_data['description'],
        )

        if selected_user:
            if type == User.TYPE.coordinator:
                created_by = "Koordinator"
                overtime.status = Overtime.STATUS.approved_coordinator
            else:
                created_by = "Manager"
                overtime.status = Overtime.STATUS.approved_manager
            overtime.save()

            send_new_overtime_notification(overtime.user, created_by)
        else:
            send_coordinator_notification(overtime.user)

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

        # send_manager_notification(overtime.user)
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


class CanceledForm(forms.Form):

    overtime = forms.ModelChoiceField(queryset=None)
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(CanceledForm, self).__init__(*args, **kwargs)
        self.fields['overtime'].queryset = Overtime.objects \
            .exclude(status__in=[Overtime.STATUS.approved_manager, Overtime.STATUS.canceled])

    def save(self, user):
        overtime = self.cleaned_data['overtime']
        notes = self.cleaned_data['notes']

        if overtime.status == Overtime.STATUS.bid:
            overtime.notes_coordinator = notes
            send_canceled_notification(overtime, canceled_by_manager=False)
        elif overtime.status == Overtime.STATUS.approved_coordinator:
            overtime.notes_manager = notes
            send_canceled_notification(overtime, canceled_by_manager=True)

        overtime.status = Overtime.STATUS.canceled
        overtime.save()

        return overtime
