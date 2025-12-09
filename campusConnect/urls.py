from django.urls import path
from . import views
from .views import create_sample_activities, join_activity

urlpatterns = [
    # Home / Index
    path('', views.index, name='index'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('student/home/', views.home_student, name='home_student'),
    path('lecturer/home/', views.home_lecturer, name='home_lecturer'),

    # Clubs
    path('clubs/', views.clubs, name='clubs'),

    # Tutors
    path('tutors/', views.tutors, name='tutors'),

    # Announcements
    path('announcement/', views.announcement, name='announcement'),

    # About
    path('about/', views.about, name='about'),

    # Team Building Activities
    path('teambuilding/', views.teambuilding, name='teambuilding'),
    path('create-samples/', create_sample_activities, name='create_samples'),
    path('join-activity/<int:activity_id>/', join_activity, name='join_activity'),

path('announcement/delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),

path('tutors/add/', views.add_tutor, name='add_tutor'),
path('tutors/delete/<int:tutor_id>/', views.delete_tutor, name='delete_tutor'),

]
