from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from jclub.apps.meetings.models import Meeting,TimeSlot
from django.contrib.auth.models import User
from django.utils import timezone
from collections import OrderedDict
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_cal.views import Events
from django.conf import settings
import dateutil.rrule as rrule
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):

    # get next meetings from today and order by date
    current_day = timezone.now()
    current_day.replace(hour=0, minute=0, second=0, microsecond=0)
    upcoming_meetings_list = Meeting.objects.filter(timeslot__date_time__gte=current_day).order_by('timeslot__date_time')[:3]
    
    # get untaken timeslots and order by date
    upcoming_timeslots_list = TimeSlot.objects.filter(meeting__isnull=True).order_by('date_time')[:3]
    
    # use custom function d_meet to order objects
    upcoming_presenters_list = sorted(User.objects.all(), key=lambda o: -o.d_meet)[:8]
    
    meetings_count = Meeting.objects.count()
    users_count = User.objects.count()

    template = loader.get_template('index.html')
    
    context = RequestContext(request, {
        'upcoming_meetings_list': upcoming_meetings_list,
        'upcoming_timeslots_list': upcoming_timeslots_list,
        'upcoming_presenters_list': upcoming_presenters_list,
        'meetings_count': meetings_count,
        'users_count': users_count,
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

    current_day = timezone.now()
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

class Calendar(Events):

    def __init__(self, request):
        super(Calendar, self).__init__()
        self.request = request

    def items(self):
        return Meeting.objects.all()

    def cal_name(self):
        return "%s %s" % (settings.BRANDING['INSTITUTION'],settings.BRANDING['DESC'])

    def cal_desc(self):
        return "ics feed for the %s %s calendar" % (settings.BRANDING['INSTITUTION'],settings.BRANDING['DESC'])

    def item_summary(self, item):
        out = "%s @ %s %s" % (item.presenter.fullname(), settings.BRANDING['INSTITUTION'], settings.BRANDING['DESC'])
        return out

    def item_start(self, item):
        return item.timeslot.date_time

    def item_end(self, item):
        return item.timeslot.date_time + timezone.timedelta(hours=2)
    
    def item_url(self, item):
        # thanks to added request object we can get the host
        return self.request.build_absolute_uri(reverse('meetings_detail',kwargs={'meeting_id': item.id}))
    
    def item_rruleset(self, item):
        rruleset = rrule.rruleset()
        return rruleset

    def item_categories(self, item):
        return [settings.BRANDING['INSTITUTION'],settings.BRANDING['DESC']]

def calendar_ics(request):
    cal = Calendar(request)
    response = HttpResponse(cal.get_ical(None,request).serialize(), content_type="text/calendar")
    name = cal.cal_name().replace(' ','_').lower()
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % name
    return response

def calendar_index(request):
    template = loader.get_template('calendar.html')
    cal_url = request.build_absolute_uri(reverse('calendar_ics'))
    return HttpResponse(template.render(RequestContext(request, {
        'cal_url': cal_url 
    })))