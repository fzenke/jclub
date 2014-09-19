from django.db import models
from django.contrib.auth.models import User

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
        return self.date_time.strftime('%a, %d.%m.%Y @ %H:%M')

    class Meta:
        ordering = ["date_time"]      

class Meeting(models.Model):
    presenter = models.ForeignKey(User, unique=False)
    timeslot  = models.ForeignKey(TimeSlot, unique=True)
    location  = models.CharField(max_length=100)
    publication_reference = models.CharField(max_length=200)
    publication_url       = models.CharField(max_length=200)
    publication_category  = models.ManyToManyField(Category)

    def __unicode__(self):
        return u'%s: %s %s' % (self.timeslot.date_time.strftime('%a, %d.%m.%Y @ %H:%M'), self.presenter.first_name, self.presenter.last_name)

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
        return self.user_name
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
        return self.user_name
User.add_to_class('fullname', user_fullname)