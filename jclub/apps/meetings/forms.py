from django import forms
from django.db.models import Q
from jclub.apps.meetings.models import Meeting, TimeSlot

# This restricts the timeslots dropdown to only the ones not assigned to a meeting
class MeetingAdminForm(forms.ModelForm):

    # fix display for timeslots
    def __init__(self, *args, **kwargs):
    	
        super(MeetingAdminForm, self).__init__(*args, **kwargs)

        # if we already have this meeting created (id!=None)
        # we have to allow the already assigned meeting timeslot to the filtered list
        if self.instance.id:
        	self.fields['timeslot'] = forms.ModelChoiceField(queryset=TimeSlot.objects.filter(
		    	Q(meeting__isnull=True) | Q(meeting__id=self.instance.id)
		))
        	
    class Meta:
        model = Meeting