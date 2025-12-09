import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualityEducation.settings')
django.setup()

from campusConnect.models import TeamBuilding

print('COUNT:', TeamBuilding.objects.count())
print(list(TeamBuilding.objects.values('id','title')))
