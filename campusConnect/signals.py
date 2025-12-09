from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile  # update to your profile model

@receiver(post_save, sender=User)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile automatically when a new user is created
        StudentProfile.objects.create(user=instance)
    else:
        # Save profile for existing users if it exists
        if hasattr(instance, 'studentprofile'):
            instance.studentprofile.save()
