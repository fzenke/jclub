from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from jclub.apps.meetings.models import Meeting,TimeSlot

# Create your views here.

def index(request):
    upcoming_meetings_list = Meeting.objects.order_by('timeslot__date_time')[:3]
    upcoming_timeslots_list = Meeting.objects.order_by('timeslot__date_time')[:3]
    upcoming_presenters_list = Meeting.objects.order_by('timeslot__date_time')[:3]


    template = loader.get_template('meetings/index.html')
    print "aha", template
    context = RequestContext(request, {
        'upcoming_meetings_list': upcoming_meetings_list,
        'upcoming_timeslots_list': upcoming_timeslots_list,
        'upcoming_presenters_list': upcoming_presenters_list,
    })
    return HttpResponse(template.render(context))

def detail(request, meeting_id):
    return HttpResponse("You're looking at the TODO detail view of meeting %s." % meeting_id)
