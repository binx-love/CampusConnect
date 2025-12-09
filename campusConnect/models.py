from django.db import models
from django.contrib.auth.models import User

# ---------- CLUB MODEL ----------
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    patron = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='patron_clubs'
    )

    def __str__(self):
        return f"{self.name} (Patron: {self.patron.username})"


# ---------- TUTOR MODEL ----------
class Tutor(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.CharField(max_length=200)
    lecturer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tutor_lectures'
    )
    rating = models.PositiveSmallIntegerField(default=0)  # 0-5 stars

    def __str__(self):
        return f"{self.name} ({self.subjects}) - Lecturer: {self.lecturer.username}"


# ---------- ANNOUNCEMENT MODEL ----------
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"


# ---------- TEAM BUILDING MODEL ----------
class TeamBuilding(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='organized_activities'
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.date})"


# ---------- STUDENT PROFILE ----------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clubs = models.ManyToManyField(
        Club, 
        blank=True, 
        related_name='members'
    )
    tutorials = models.ManyToManyField(
        Tutor, 
        blank=True, 
        related_name='students'
    )
    team_buildings = models.ManyToManyField(
        TeamBuilding, 
        blank=True, 
        related_name='participants'
    )

    def __str__(self):
        return self.user.username
