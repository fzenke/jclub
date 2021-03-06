from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from jclub.apps.meetings.models import Meeting, TimeSlot
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
    upcoming_meetings_list = Meeting.objects.filter(
        timeslot__date_time__gte=current_day).order_by('timeslot__date_time')[:3]

    # get untaken timeslots and order by date
    upcoming_timeslots_list = TimeSlot.objects.filter(meeting__isnull=True).filter(
        date_time__gte=current_day).order_by('date_time')[:3]

    # use custom function d_meet to order objects
    users = User.objects.all()
    users_act = [o for o in users if o.is_active]
    upcoming_presenters_list = sorted(users_act, key=lambda o: -o.d_meet)[:8]

    meetings_count = Meeting.objects.count()
    users_count = User.objects.count()

    context = {
        'upcoming_meetings_list': upcoming_meetings_list,
        'upcoming_timeslots_list': upcoming_timeslots_list,
        'upcoming_presenters_list': upcoming_presenters_list,
        'meetings_count': meetings_count,
        'users_count': users_count,
    }

    return render(request, 'index.html', context)


def detail(request, meeting_id):

    meeting = Meeting.objects.get(id=meeting_id)
    context = {
        'meeting': meeting,
    }

    return render(request, 'meetings/detail.html', context)


def meetings_index(request):

    current_day = timezone.now()
    current_day.replace(hour=0, minute=0, second=0, microsecond=0)

    upcoming_meetings_list = Meeting.objects.filter(
        timeslot__date_time__gte=current_day).order_by('timeslot__date_time')
    past_meetings_list = Meeting.objects.filter(
        timeslot__date_time__lt=current_day).order_by('-timeslot__date_time')

    context = {
        'upcoming_meetings_list': upcoming_meetings_list,
        'past_meetings_list': past_meetings_list,
    }
    return render(request, 'meetings/index.html', context)


def presenters_index(request):

    presenters = User.objects.all().annotate(meetings_count=Count(
        'meeting__id')).order_by('-meetings_count', 'last_name')

    context = {
        'presenters': presenters,
    }

    return render(request, 'presenters/index.html', context)


def presenters_detail(request, user_id):

    presenter = get_object_or_404(User, id=user_id)
    meetings = presenter.meeting_set.all()
    meetings_count = len(meetings)
    context = {
        'presenter': presenter,
        'meetings': meetings,
        'meetings_count': meetings_count,
    }

    return render(request, 'presenters/detail.html', context)


class Calendar(Events):

    def __init__(self, request):
        super(Calendar, self).__init__()
        self.request = request

    def items(self):
        return Meeting.objects.all()

    def cal_name(self):
        return "%s %s" % (settings.BRANDING['INSTITUTION'], settings.BRANDING['DESC'])

    def cal_desc(self):
        return "ics feed for the %s %s calendar" % (settings.BRANDING['INSTITUTION'], settings.BRANDING['DESC'])

    def item_summary(self, item):
        out = "%s @ %s %s" % (item.presenter.fullname(), settings.BRANDING[
                              'INSTITUTION'], settings.BRANDING['DESC'])
        return out

    def item_start(self, item):
        return item.timeslot.date_time

    def item_end(self, item):
        return item.timeslot.date_time + timezone.timedelta(hours=2)

    def item_url(self, item):
        # thanks to added request object we can get the host
        return self.request.build_absolute_uri(reverse('meetings_detail', kwargs={'meeting_id': item.id}))

    def item_rruleset(self, item):
        rruleset = rrule.rruleset()
        return rruleset

    def item_categories(self, item):
        return [settings.BRANDING['INSTITUTION'], settings.BRANDING['DESC']]


def calendar_ics(request):

    cal = Calendar(request)
    vcal = cal.get_ical(None, request)

    # add timezone id of event (google calendar needs this for correct feed
    # behaviour)
    for ev in vcal.vevent_list:
        ev.add('TZID').value = settings.TIME_ZONE

    response = HttpResponse(vcal.serialize(), content_type="text/calendar")
    name = cal.cal_name().replace(' ', '_').lower()
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % name
    return response


def calendar_index(request):

    cal_url = request.build_absolute_uri(reverse('calendar_ics'))

    context = {
        'cal_url': cal_url
    }

    return render(request, 'calendar.html', context)
