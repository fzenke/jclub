from django.contrib import admin
from meetings.models import Meeting,TimeSlot,Category

# Register your models here.

admin.site.register(Meeting)
admin.site.register(TimeSlot)
admin.site.register(Category)
