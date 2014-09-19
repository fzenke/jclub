# Script to solve problems introduced by starting a django app
# and filling data into the db with the wrong time zone set in the
# settings.
# 
# Effectively converts hours from UTC labeled Europe/Zurich times to
# correct UTC times.

from django.utils import timezone
import pytz, datetime
from jclub.apps.meetings.models import Meeting, TimeSlot

tz = pytz.timezone('Europe/Zurich')
tz_utc = pytz.timezone('UTC')
times = TimeSlot.objects.all()

for t in times:
	print "Converting time ",
	t_old = t.date_time
	print t_old, " --> "
	t_naive = t_old.replace(tzinfo=None)
	t_loc = tz.localize(t_naive)
	t_new = t_loc.astimezone(tz_utc)
	print t_new
	t.date_time = t_new
	t.save()