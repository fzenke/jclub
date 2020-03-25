from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.conf import settings
from django.template import defaultfilters

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class TimeSlot(models.Model):
    date_time = models.DateTimeField('date and time')
      
    def __unicode__(self):
        loc_date = timezone.localtime(self.date_time)
        return defaultfilters.date(loc_date,'M. d. Y @ P')

    class Meta:
        ordering = ["date_time"]      

class Meeting(models.Model):
    presenter = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    publication_reference = models.CharField(max_length=200)
    publication_url       = models.CharField(max_length=200)
    publication_category  = models.ManyToManyField(Category)

    def __unicode__(self):
        loc_date = timezone.localtime(self.timeslot.date_time)
        return u'%s: %s %s' % (defaultfilters.date(loc_date,'M. d. Y @ P'), self.presenter.first_name, self.presenter.last_name)
    
    class Meta:
        ordering = ["-timeslot__date_time"] 

# These functions extend the contrib.auth.User without actually writing a linked user_profile
# or subclassing the User class. This, for now, is the most straightforward way of
# implementing the desired features.
# 
# TODO replace this with a proper subclass of the User class.
def user_unicode(self):
    c = []
    if self.last_name:
        c.append(self.last_name)
    if self.first_name:
        c.append(self.first_name)
    if c:
        return ', '.join(c)
    else:
        return self.username
User.add_to_class('__unicode__', user_unicode)

def user_fullname(self):
    c = []
    if self.first_name:
        c.append(self.first_name)
    if self.last_name:
        c.append(self.last_name)
    if c:
        return ' '.join(c)
    else:
        return self.username
User.add_to_class('fullname', user_fullname)

def days_since_meeting(self):
    last_meeting = self.meeting_set.order_by('timeslot__date_time').last()
    t_delta = timezone.timedelta.max
    if last_meeting:
        t_last = last_meeting.timeslot.date_time
        t_now = timezone.now()    
        t_delta = t_now - t_last
    return t_delta.days

def days_since_meeting_str(self):
    d_meet = days_since_meeting(self)
    if d_meet == timezone.timedelta.max.days:
        return str(settings.BRANDING['NOT_PRESENTED'])
    else:
        return str(d_meet)
        
User.add_to_class('d_meet', property(fget=days_since_meeting))
User.add_to_class('d_meet_str', property(fget=days_since_meeting_str))