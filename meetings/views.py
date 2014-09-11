from django.shortcuts import render
from django.http import HttpResponse

from meetings.models import Meeting,TimeSlot

# Create your views here.

def index(request):
    upcoming_meetings_list = Meeting.objects.order_by('timeslot__date_time')[:5]

    output = ', '.join([p.publication_reference for p in upcoming_meetings_list])
    return HttpResponse(output)

def detail(request, meeting_id):
    return HttpResponse("You're looking at the TODO detail view of meeting %s." % meeting_id)
