from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse

from .forms import SignUpForm, LoginForm, AnnouncementForm
from .models import Club, Tutor, Announcement, TeamBuilding, StudentProfile

# ---------- HOME / INDEX ----------
def index(request):
    if request.user.is_authenticated:
        return redirect('home_lecturer' if request.user.is_staff else 'home_student')
    return render(request, 'campusConnect/index.html')


# ---------- SIGNUP ----------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create student profile for non-staff users
            if not user.is_staff:
                StudentProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home_lecturer' if user.is_staff else 'home_student')
    else:
        form = SignUpForm()
    return render(request, 'campusConnect/signup.html', {'form': form})


# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_lecturer' if user.is_staff else 'home_student')
    else:
        form = LoginForm()
    return render(request, 'campusConnect/login.html', {'form': form})


# ---------- LOGOUT ----------
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')


# ---------- STUDENT DASHBOARD ----------
@login_required
def home_student(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    context = {
        'student_profile': student_profile,
        'enrolled_clubs': student_profile.clubs.all(),
        'booked_tutorials': student_profile.tutorials.all(),
        'joined_activities': student_profile.team_buildings.all(),
        'announcements': Announcement.objects.all().order_by('-date_posted')[:5],
    }
    return render(request, 'campusConnect/home_student.html', context)


# ---------- LECTURER DASHBOARD ----------
@login_required
def home_lecturer(request):
    context = {
        'lecturer_clubs': Club.objects.filter(patron=request.user),
        'lecturer_tutors': Tutor.objects.filter(lecturer=request.user),
        'announcements': Announcement.objects.filter(author=request.user).order_by('-date_posted')[:5],
    }
    return render(request, 'campusConnect/home_lecturer.html', context)


# ---------- CLUBS ----------
@login_required
def clubs(request):
    clubs_list = Club.objects.all()
    if request.method == 'POST' and not request.user.is_staff:
        club_id = request.POST.get('club_id')
        club = get_object_or_404(Club, id=club_id)
        student_profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        student_profile.clubs.add(club)
        return redirect('clubs')
    return render(request, 'campusConnect/clubs.html', {'clubs': clubs_list})


# ---------- TUTORS ----------
@login_required
def tutors(request):
    tutors_list = Tutor.objects.all()
    if request.method == 'POST' and not request.user.is_staff:
        tutor_id = request.POST.get('tutor_id')
        tutor = get_object_or_404(Tutor, id=tutor_id)
        student_profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        student_profile.tutorials.add(tutor)
        return redirect('tutors')
    return render(request, 'campusConnect/tutors.html', {'tutors': tutors_list})


# ---------- ANNOUNCEMENTS ----------
@login_required
def announcement(request):
    announcements_list = Announcement.objects.all().order_by('-date_posted')
    form = AnnouncementForm(request.POST or None)
    if request.user.is_staff and request.method == 'POST' and form.is_valid():
        announcement = form.save(commit=False)
        announcement.author = request.user
        announcement.save()
        return redirect('announcement')
    return render(request, 'campusConnect/announcement.html', {
        'announcements': announcements_list,
        'form': form,
    })


# ---------- ABOUT ----------
def about(request):
    return render(request, 'campusConnect/about.html')


# ---------- TEAM BUILDING ----------
@login_required
def teambuilding(request):
    activities = TeamBuilding.objects.all()
    return render(request, 'campusConnect/teambuilding.html', {'activities': activities})


# ---------- CREATE SAMPLE ACTIVITIES (STAFF ONLY) ----------
@login_required
def create_sample_activities(request):
    if not request.user.is_staff:
        return HttpResponse("🚫 Only staff can create sample activities.", status=403)

    organizer = User.objects.filter(is_staff=True).first()
    if not organizer:
        return HttpResponse("⚠️ No staff user found to assign as organizer.", status=400)

    activities = [
        ("Outdoor Retreat", "A day full of outdoor team challenges and bonding."),
        ("Coding Hackathon", "Collaborate with fellow students to solve coding challenges."),
        ("Sports Day", "Participate in fun sports activities to build teamwork."),
        ("Art & Creativity Workshop", "Engage in creative projects to strengthen team collaboration."),
    ]

    created_count = 0
    for title, description in activities:
        activity, created = TeamBuilding.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'organizer': organizer,
                'date': timezone.now() + timedelta(days=7)
            }
        )
        if created:
            created_count += 1

    if created_count == 0:
        return HttpResponse("ℹ️ All sample activities already exist.")
    
    return HttpResponse(f"✅ {created_count} sample activities created successfully!")


# ---------- JOIN ACTIVITY ----------
@login_required
def join_activity(request, activity_id):
    if request.user.is_staff:
        return redirect('teambuilding')  # Staff cannot join

    activity = get_object_or_404(TeamBuilding, id=activity_id)
    student_profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    student_profile.team_buildings.add(activity)

    return redirect('teambuilding')


def teambuilding(request):
    activities = TeamBuilding.objects.all()
    return render(request, 'campusConnect/teambuilding.html', {'activities': activities})

# ---------- DELETE ANNOUNCEMENT ----------
@login_required
def delete_announcement(request, announcement_id):
    if not request.user.is_staff:
        return HttpResponse("🚫 Only staff can delete announcements.", status=403)
    
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement')
    
    return redirect('announcement')

# ---------- ADD TUTOR ----------
@login_required
def add_tutor(request):
    if not request.user.is_staff:
        return HttpResponse("🚫 Only lecturers can add tutoring sessions.", status=403)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        availability = request.POST.get('availability')
        contact = request.POST.get('contact')
        rate = request.POST.get('rate', '')
        
        Tutor.objects.create(
            name=name,
            subject=subject,
            availability=availability,
            contact=contact,
            rate=rate,
            lecturer=request.user
        )
        return redirect('tutors')
    
    return redirect('tutors')


# ---------- DELETE TUTOR ----------
@login_required
def delete_tutor(request, tutor_id):
    if not request.user.is_staff:
        return HttpResponse("🚫 Only lecturers can delete tutoring sessions.", status=403)
    
    tutor = get_object_or_404(Tutor, id=tutor_id)
    
    # Check if the tutor belongs to the logged-in lecturer
    if tutor.lecturer != request.user:
        return HttpResponse("🚫 You can only delete your own tutoring sessions.", status=403)
    
    if request.method == 'POST':
        tutor.delete()
        return redirect('tutors')