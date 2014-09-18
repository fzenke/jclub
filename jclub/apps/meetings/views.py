from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from jclub.apps.meetings.models import Meeting,TimeSlot
from django.contrib.auth.models import User
from datetime import *
from collections import OrderedDict
from django.shortcuts import get_object_or_404
from django.db.models import Count

# Create your views here.

def index(request):

    # get next meetings from today and order by date
    current_day = datetime.now()
    current_day.replace(hour=0, minute=0, second=0, microsecond=0)
    upcoming_meetings_list = Meeting.objects.filter(timeslot__date_time__gte=current_day).order_by('timeslot__date_time')[:3]
    
    # get untaken timeslots and order by date
    upcoming_timeslots_list = TimeSlot.objects.filter(meeting__isnull=True).order_by('date_time')[:3]
    
    # use custom function d_meet to order objects
    upcoming_presenters_list = sorted(User.objects.all(), key=lambda o: -o.d_meet)[:8]
    
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

def presenters_index(request):
    template = loader.get_template('presenters/index.html')

    presenters = User.objects.all().annotate(meetings_count=Count('meeting__id')).order_by('-meetings_count', 'last_name')
    context = RequestContext(request, {
        'presenters': presenters,
    })

    return HttpResponse(template.render(context))

def presenters_detail(request, user_id):
    template = loader.get_template('presenters/detail.html')

    presenter = get_object_or_404(User,id=user_id)
    meetings =  presenter.meeting_set.all()
    meetings_count = len(meetings)
    context = RequestContext(request, {
        'presenter': presenter,
        'meetings': meetings,
        'meetings_count': meetings_count,
    })

    return HttpResponse(template.render(context))

