from django.contrib import admin
from .models import Servant, Meeting, Attendance, Excuse, Schedule

admin.site.register(Servant)
admin.site.register(Meeting)
admin.site.register(Attendance)
admin.site.register(Excuse)
admin.site.register(Schedule)