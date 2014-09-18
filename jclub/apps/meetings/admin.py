from django.contrib import admin
from jclub.apps.meetings.models import Meeting,TimeSlot,Category
from jclub.apps.meetings.forms import MeetingAdminForm
from django.db.models import Q

# Custom admin backend form - this restricts the timeslots dropdown 
# to only the ones not assigned to a meeting, as well as the users for non-admin users
# to only himself and the currently assigned one.

# TODO check on save if user is allowed to save the chosen presenter. Currently
# this just restricts the selection, probably a modified request could smuggle in
# any user as presenter.

class MeetingAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):

        form = super(MeetingAdmin, self).get_form(request, obj, **kwargs)
        
        # restrict presenters to current + self for non-superusers 
        if not request.user.is_superuser:
            idset = []
            if obj:
                idset=[obj.presenter.id]
            form.base_fields['presenter'].queryset = form.base_fields['presenter'].queryset.filter(Q(id=request.user.id) | Q(id__in=idset))

        # restrict timeslots to current + available
        idset = []
        if obj:
            idset=[obj.id]
        form.base_fields['timeslot'].queryset = form.base_fields['timeslot'].queryset.filter(Q(meeting__isnull=True) | Q(meeting__id__in=idset))
            
        return form

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(TimeSlot)
admin.site.register(Category)