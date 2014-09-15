from django.contrib import admin
from jclub.apps.meetings.models import Meeting,TimeSlot,Category
from jclub.apps.meetings.forms import MeetingAdminForm

# Custom admin backend form - this restricts the timeslots dropdown 
# to only the ones not assigned to a meeting
class MeetingAdmin(admin.ModelAdmin):
    form = MeetingAdminForm

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(TimeSlot)
admin.site.register(Category)
