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
      presenter = models.ForeignKey(User, unique=False)
      timeslot  = models.ForeignKey(TimeSlot, unique=True)
      location  = models.CharField(max_length=100)
      publication_reference = models.CharField(max_length=200)
      publication_url       = models.CharField(max_length=200)
      publication_category  = models.ManyToManyField(Category)
      def __unicode__(self):
          return "%s/%s"%(self.timeslot,self.presenter)

# class UserProfile(models.Model):
#    #required field
#    user = models.ForeignKey(User, unique=True)

#    sciper = models.PositiveIntegerField(null=True, blank=True)
#    where = models.CharField(max_length=100, null=True, blank=True)
#    units = models.CharField(max_length=300, null=True, blank=True)
#    group = models.CharField(max_length=150, null=True, blank=True)
#    classe = models.CharField(max_length=100, null=True, blank=True)
#    statut = models.CharField(max_length=100, null=True, blank=True)

#    # Trigger for creating a profile on user creation
#    def user_post_save(sender, instance, **kwargs):
#        profile, new = UserProfile.objects.get_or_create(user=instance)

#    # Register the trigger
#    models.signals.post_save.connect(user_post_save, sender=User)