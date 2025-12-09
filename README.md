📚 CampusConnect

A centralized platform for students to access clubs, tutors, team-building activities, and academic resources in one place.

🚀 Features
👥 User Management

Student sign-up and login

Lecturer sign-up/login

Role-based pages (Student Dashboard & Lecturer Dashboard)

🎓 Tutors Section

Display available tutors

Book tutorials

Tutor ratings

Lecturer profile display

🤝 Team Building Activities

Display upcoming activities

Students can join activities

Admin/staff can create activities

📰 Announcements

Lecturers can post announcements

Students can view updates on their dashboards

🧭 Clubs 

Students browse and join clubs

Club admins manage club updates

🛠️ Technologies Used

Django 4+

Python

Bootstrap 5


HTML / CSS / 

📁 Project Structure
CampusConnect/
│
├── campusconnect/       
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── main/                
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── templates/
│   │   ├── home_student.html
│   │   ├── home_lecturer.html
│   │   ├── team_activities.html
│   │   └── tutors.html
│   └── static/
│
└── manage.py

⚙️ Installation
1️⃣ Clone the project
git clone https://github.com/yourusername/CampusConnect.git
cd CampusConnect

2️⃣ Create a virtual environment
python -m venv env
source env/bin/activate   # Mac/Linux
env\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py migrate

5️⃣ Create a superuser
python manage.py createsuperuser

6️⃣ Run the server
python manage.py runserver
