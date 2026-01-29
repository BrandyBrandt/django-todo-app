# Django ToDo Application

A full-featured task management web application built with Django, featuring user authentication, task organization, and a clean, responsive interface.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

- **User Management**
  - User registration and authentication
  - Profile management
  - Password reset functionality (email displayed in console for development)

- **Task Management**
  - Create, edit, and delete tasks
  - Task priorities (low, medium, high)
  - Due dates and reminders
  - Task status tracking (active/completed)

- **Organization**
  - Categories and tags (private per user)
  - Advanced filtering (active, completed, today, this week, overdue)
  - Search functionality

- **API**
  - RESTful API endpoints (JSON)

## 🛠️ Technologies

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django built-in auth system

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BrandyBrandt/django-todo-app.git
   cd django-todo-app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser account (REQUIRED)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account. This account will be used to access the admin panel and manage the application.

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
django-todo-app/
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── README.md                # Project documentation
│
├── WebBlogProject/          # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
│
├── accounts/                # User authentication app
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── urls.py              # Auth URL patterns
│
├── blog/                    # Main tasks/blog app
│   ├── models.py            # Task, Category, Tag models
│   ├── views.py             # Task management views
│   ├── forms.py             # Task forms
│   └── urls.py              # App URL patterns
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Auth templates
│   └── tasks/               # Task templates
│
└── static/                  # Static files
    ├── style.css            # Main stylesheet
    └── js/                  # JavaScript files
```

## 🔑 Key Features Explained

### Task Filtering
- **Active Tasks**: View all incomplete tasks
- **Completed**: Archive of finished tasks
- **Today**: Tasks due today
- **This Week**: Tasks due within 7 days
- **Overdue**: Past due tasks requiring attention

### Categories & Tags
Each user has private categories and tags for personal organization. Create custom categories for different areas of life (Work, Personal, Study, etc.) and use tags for additional context.

### Priorities
Three priority levels help you focus on what matters:
- 🔴 High - Urgent and important
- 🟡 Medium - Important but not urgent
- 🟢 Low - Nice to have

## 🔒 Security Notes

- `SECRET_KEY` should be set via environment variable in production
- `DEBUG` must be `False` in production
- Add allowed hosts in `ALLOWED_HOSTS` setting
- Use environment variables for sensitive data

## 🚀 Deployment

For production deployment:
1. Set environment variables (`SECRET_KEY`, `DEBUG=False`)
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up static files serving
5. Use a production WSGI server (gunicorn, uwsgi)

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Aleksander Brandt**
- Email: aleksander.brandtwaw@gmail.com
- GitHub: [@BrandyBrandt](https://github.com/BrandyBrandt)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show your support

Give a ⭐️ if this project helped you!
