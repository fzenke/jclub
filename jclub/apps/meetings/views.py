from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from jclub.apps.meetings.models import Meeting,TimeSlot
from django.contrib.auth.models import User
from datetime import *
from collections import OrderedDict

# Create your views here.

def index(request):

    # get next meetings from today and order by date
    current_day = datetime.now()
    current_day.replace(hour=0, minute=0, second=0, microsecond=0)
    upcoming_meetings_list = Meeting.objects.filter(timeslot__date_time__gte=current_day).order_by('timeslot__date_time')[:3]
    
    # get untaken timeslots and order by date
    upcoming_timeslots_list = TimeSlot.objects.filter(meeting__isnull=True).order_by('date_time')[:3]
    
    # get 1) presenters that are not assigned to a slot 2) that presented the longest ago
    upcoming_presenters_list_empty = User.objects.filter(meeting__isnull=True)
    
    # this works on postgresql but sadly not on anything else
    
    # upcoming_presenters_list_given = User.objects.filter(meeting__isnull=False).order_by("meeting__timeslot__date_time").distinct('id')[:3]
    # TODO filter for distinct results here
    upcoming_presenters_list_given = User.objects.filter(meeting__isnull=False).order_by("meeting__timeslot__date_time")
    upcoming_presenters_list = (list(upcoming_presenters_list_empty) + list(upcoming_presenters_list_given))[:5]

    template = loader.get_template('index.html')
    
    context = RequestContext(request, {
        'upcoming_meetings_list': upcoming_meetings_list,
        'upcoming_timeslots_list': upcoming_timeslots_list,
        'upcoming_presenters_list': upcoming_presenters_list,
    })
    return HttpResponse(template.render(context))

def detail(request, meeting_id):

    template = loader.get_template('meetings/detail.html')

    meeting = Meeting.objects.get(id=meeting_id)
    context = RequestContext(request, {
        'meeting': meeting,
    })
    return HttpResponse(template.render(context))


def meetings_index(request):

    current_day = datetime.now()
    current_day.replace(hour=0, minute=0, second=0, microsecond=0)

    upcoming_meetings_list = Meeting.objects.filter(timeslot__date_time__gte=current_day).order_by('timeslot__date_time')
    past_meetings_list = Meeting.objects.filter(timeslot__date_time__lt=current_day).order_by('-timeslot__date_time')
    
    template = loader.get_template('meetings/index.html')
    
    context = RequestContext(request, {
        'upcoming_meetings_list': upcoming_meetings_list,
        'past_meetings_list': past_meetings_list,
    })
    return HttpResponse(template.render(context))
