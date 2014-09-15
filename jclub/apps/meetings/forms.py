from django import forms
from jclub.apps.meetings.models import Meeting, TimeSlot

# This restricts the timeslots dropdown to only the ones not assigned to a meeting
class MeetingAdminForm(forms.ModelForm):
    timeslot = forms.ModelChoiceField(queryset=TimeSlot.objects.filter(meeting__isnull=True))
    class Meta:
        model = Meeting