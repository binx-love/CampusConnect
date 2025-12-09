from django.contrib import admin
from .models import Club, Tutor, Announcement, TeamBuilding, StudentProfile

# Register your models to appear in the admin site
admin.site.register(Club)
admin.site.register(Tutor)
admin.site.register(Announcement)
admin.site.register(TeamBuilding)
admin.site.register(StudentProfile)
