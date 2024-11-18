# Email Sender

Django-based email automation application that enables users to upload contact details, create email templates, schedule emails, and monitor email status in real-time. Built with Celery for asynchronous task management, Redis for caching, and WebSockets for live updates.

## 📑 Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Key Components](#key-components)
- [API Documentation](#api-documentation)
- [License](#license)

## 🗂 Project Structure

```bash
email_sender/
├── manage.py
├── email_sender/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── emails/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│   ├── tasks.py
│   ├── templates/
│   │   └── emails/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── prompt.html
│   │       ├── schedule.html
│   │       ├── status.html
│   │       └── upload.html
│   ├── static/
│   │   └── emails/
│   │       └── style.css
│   ├── urls.py
│   └── views.py
├── templates/
│   └── emails/
│       └── index.html
└── requirements.txt
```
## 💻 Installation

### Prerequisites

- Python 3.8+
- Redis Server
- Virtual Environment

1. **Create a Virtual Environment**

'''bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
'''

2. **Install Dependencies**

'''bash
pip install -r requirements.txt
'''

**Dependencies List (requirements.txt)**

'''plaintext
Django==3.2
channels==3.0
channels-redis==3.3
celery==5.1
redis==3.5
django-crispy-forms==1.11
openai==0.11
django-celery-beat==2.2
django-celery-results==2.2
pandas==1.3
'''

3. **Start Required Services**

'''bash
# Start Redis Server
redis-server

# Apply database migrations
python manage.py migrate

# Create superuser (Optional)
python manage.py createsuperuser

# Start Celery Worker
celery -A email_sender worker -l info

# Start Celery Beat Scheduler
celery -A email_sender beat -l info

# Run Django Development Server
python manage.py runserver
'''

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

'''env
DJANGO_SECRET_KEY=your_django_secret_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sender_email
OPENAI_API_KEY=your_openai_api_key
REDIS_URL=redis://localhost:6379/0
'''

Update `settings.py` with your configuration:

'''python
# Email Settings
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL')

# Redis Settings
REDIS_URL = os.environ.get('REDIS_URL')

# OpenAI Settings
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
'''

## 🚀 Usage

### Upload Contacts:

- Visit http://localhost:8000/upload
- Upload CSV file with contact details
- Supported format: name,email,company

### Create Email Templates:

- Navigate to http://localhost:8000/templates
- Use placeholders: {name}, {company}
- Preview template with sample data

### Schedule Emails:

- Choose sending options:
  - Immediate
  - Scheduled time
  - Staggered intervals

- Set recipient groups
- Configure retry settings

### Monitor Status:

- Real-time delivery tracking
- Success/failure statistics
- Bounce rate analytics

## 🔧 Key Components

- **Celery Tasks**:
  - Email sending and scheduling
  - Status updates
  - Error handling and retries

- **WebSocket Integration**:
  - Real-time status updates
  - Connection handling in `consumers.py`
  - Routing configuration in `routing.py`

- **Database Models**:
  - Contact management
  - Template storage
  - Email tracking
  - Schedule configuration

## 📚 API Documentation

**REST Endpoints**

'''plaintext
POST /api/contacts/upload/
POST /api/templates/create/
POST /api/emails/schedule/
GET  /api/emails/status/<uuid:email_id>/
'''

**WebSocket Events**

'''plaintext
ws://<domain>/ws/emails/status/
'''

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
