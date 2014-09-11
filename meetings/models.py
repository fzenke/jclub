from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
      name = models.CharField(max_length=200)
      def __unicode__(self):
          return self.name


class TimeSlot(models.Model):
      date_time = models.DateTimeField('date and time')
      def __unicode__(self):
          return self.date_time.strftime('%Y-%m-%d %H:%M')
      

class Meeting(models.Model):
      presenter = models.ForeignKey(User, unique=True)
      timeslot  = models.ForeignKey(TimeSlot, unique=True)
      location  = models.CharField(max_length=100)
      publication_reference = models.CharField(max_length=200)
      publication_url       = models.CharField(max_length=200)
      publication_category  = models.ManyToManyField(Category)
      def __unicode__(self):
          return "%s/%s"%(self.timeslot,self.presenter)

