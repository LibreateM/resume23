# 📄 ResumeForge - AI-Powered Resume Builder & ATS Checker

A modern Django-based web application that helps users create professional resumes with AI assistance and check their resume compatibility with Applicant Tracking Systems (ATS).

## 🌟 Features

### Resume Building
- 📝 Interactive resume builder with multiple templates
- 🎨 Professional design templates
- 📋 Step-by-step form guidance
- 🖥️ Live preview of resume
- 📥 Import resume data
- 💾 Save and edit resumes

### AI-Powered Features
- 🤖 AI Resume Content Generator (using Groq API)
- ✨ Smart content suggestions
- 🔄 Resume optimization assistance
- 📊 Real-time feedback

### ATS Checker
- ✅ Resume ATS compatibility analysis
- 📈 Score-based evaluation
- 🔍 Keyword optimization suggestions
- 📊 Detailed ATS report

### User Management
- 👤 User registration and authentication
- 🔐 Secure login/logout
- 📊 User dashboard
- 👨‍💼 Admin panel for management
- 📧 Contact form with admin replies

### Export Options
- 📄 PDF export with professional formatting
- 🖨️ Print-friendly layouts
- 📥 Download resume

---

## 🛠️ Tech Stack

### Backend
- **Python 3.x**
- **Django 5.0.6** - Web framework
- **PostgreSQL** - Database
- **Gunicorn** - WSGI server

### Frontend
- **HTML5 / CSS3**
- **JavaScript** - Interactivity
- **Bootstrap** - UI Framework

### External APIs & Libraries
- **Groq API** - AI content generation
- **ReportLab** - PDF generation
- **PyPDF2** - PDF manipulation
- **Pillow** - Image processing

### Deployment
- **Render** - Cloud hosting
- **WhiteNoise** - Static file serving

---

## 📋 Requirements

- Python 3.8+
- PostgreSQL
- pip (Python Package Manager)
- Git
- Groq API Key

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/LibreateM/resume23.git
cd resume23
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
```bash
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=postgresql://user:password@localhost:5432/resumeforge_db
GROQ_API_KEY=your-groq-api-key-here
EOF
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/resumeforge_db

# Groq API (for AI features)
GROQ_API_KEY=your-groq-api-key

# Optional: Render/Production Settings
RENDER=True
```

### Groq API Setup
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and get your API key
3. Add `GROQ_API_KEY` to environment variables

### Database Setup
Using PostgreSQL:
```bash
createdb resumeforge_db
psql resumeforge_db < backup.sql  # If you have a backup
```

---

## 📁 Project Structure

```
resume23/
├── accounts/              # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin_urls.py
│   ├── dashboard_urls.py
│   └── forms.py
│
├── resumes/               # Resume management app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│
├── ats_checker/           # ATS analysis app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── analyzer.py
│
├── resumeforge/           # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   └── ...
│
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── img/
│
├── resumes/               # Uploaded resumes directory
│
├── media/                 # Media files
│
├── manage.py
├── requirements.txt
├── build.sh               # Build script for deployment
└── README.md
```

---

## 🌐 API Endpoints

### User Authentication
- `GET/POST /accounts/signin/` - User login
- `GET/POST /accounts/signup/` - User registration
- `GET /accounts/logout/` - User logout
- `GET/POST /accounts/profile/` - User profile management

### Resume Management
- `GET /resumes/` - List all user resumes
- `GET/POST /resumes/create/` - Create new resume
- `GET/POST /resumes/<id>/edit/` - Edit resume
- `GET /resumes/<id>/preview/` - Preview resume
- `GET /resumes/<id>/download/` - Download resume as PDF
- `DELETE /resumes/<id>/delete/` - Delete resume

### ATS Checker
- `GET/POST /ats/upload/` - Upload resume for ATS check
- `GET /ats/results/<id>/` - View ATS analysis results
- `GET /ats/report/<id>/` - Download ATS report

### Dashboard
- `GET /dashboard/` - User dashboard
- `GET /dashboard/resumes/` - Resume management
- `GET /dashboard/settings/` - User settings

### Admin Panel
- `GET /admin-panel/` - Admin dashboard
- `GET /admin-panel/users/` - Manage users
- `GET /admin-panel/contacts/` - Manage contact messages
- `GET /admin-panel/reports/` - View analytics

### Public Pages
- `GET /` - Home page
- `GET /about/` - About page
- `GET /contact/` - Contact form
- `GET /templates-page/` - Browse templates

---

## 🚀 Deployment on Render

### Prerequisites
- GitHub account
- Render account
- PostgreSQL database

### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Connect to Render**
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click "New +" → "Web Service"
- Connect your GitHub repository

3. **Configure Build & Start Commands**

**Build Command:**
```bash
./build.sh
```

Or manually:
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn resumeforge.wsgi:application
```

4. **Set Environment Variables**

In Render Dashboard → Environment:
```
DEBUG=False
SECRET_KEY=your-random-secret-key
ALLOWED_HOSTS=your-domain.onrender.com
DATABASE_URL=postgresql://...
GROQ_API_KEY=your-groq-api-key
```

5. **Deploy**
- Click "Create Web Service"
- Render will automatically deploy

---

## 🗄️ Database Models

### User Model
- Extends Django User
- Related to Resume, ATSResult

### Resume Model
```python
- user (ForeignKey to User)
- title
- content (JSON format)
- template_type
- created_at
- updated_at
- is_public (boolean)
```

### ATSResult Model
```python
- user (ForeignKey to User)
- resume_file (FileField)
- ats_score (IntegerField 0-100)
- missing_keywords (TextField)
- suggestions (TextField)
- analyzed_at (DateTime)
```

### Contact Model
```python
- name (CharField)
- email (EmailField)
- message (TextField)
- created_at (DateTime)
- is_resolved (boolean)
```

---

## 🤖 AI Features (Groq Integration)

### Resume Content Generation
The app uses Groq's API to generate AI-powered resume content:

```python
# Example usage
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {"role": "user", "content": "Generate a professional resume summary..."}
    ]
)
```

### Supported Models
- `mixtral-8x7b-32768` (Default)
- `llama2-70b-4096`
- `gemma-7b-it`

---

## 📊 ATS Checker Features

### Analysis Includes
- ✅ Keyword extraction and analysis
- ✅ Format compatibility check
- ✅ Content readability score
- ✅ Missing important keywords
- ✅ Optimization suggestions
- ✅ Overall ATS compatibility score (0-100)

### How It Works
1. Upload resume (PDF or Word)
2. System extracts text
3. AI analyzes against job keywords
4. Generates detailed report
5. Provides optimization tips

---

## 🔒 Security Features

- ✅ CSRF Protection
- ✅ SQL Injection prevention
- ✅ XSS Protection
- ✅ Secure password hashing
- ✅ Session management
- ✅ Environment variables for secrets
- ✅ HTTPS in production
- ✅ User authentication required

---

## 📸 Screenshots

### Home Page
- Hero section with CTA
- Feature highlights
- Template showcase

### Resume Builder
- Multi-step form
- Live preview
- AI suggestions

### ATS Checker
- File upload
- Analysis results
- Optimization tips

### Dashboard
- Resume management
- ATS history
- Profile settings

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Run migrations
python manage.py migrate
```

### Groq API Error
- Verify `GROQ_API_KEY` is set correctly
- Check API key has quota
- Try different model

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Media Files Not Showing
- Check `MEDIA_URL` and `MEDIA_ROOT` settings
- Verify file permissions

---

## 📝 Usage Examples

### Create a Resume
1. Go to Dashboard
2. Click "Create New Resume"
3. Fill in your details
4. Select a template
5. Preview and download

### Check ATS Compatibility
1. Go to ATS Checker
2. Upload your resume
3. Wait for analysis
4. View detailed report
5. Follow optimization tips

### Generate AI Content
1. In resume builder
2. Click "AI Suggest"
3. Choose section (summary, skills, etc.)
4. Accept or edit suggestions
5. Save changes

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support & Contact

### Get Help
- **Email:** [Your Email]
- **GitHub Issues:** [Report a bug](https://github.com/LibreateM/resume23/issues)
- **Contact Form:** Available on website

### Social Links
- Portfolio: [Your Portfolio]
- LinkedIn: [Your LinkedIn]
- Twitter: [Your Twitter]

---

## 🎯 Roadmap

### Upcoming Features
- [ ] LinkedIn integration
- [ ] Multiple language support
- [ ] Resume templates marketplace
- [ ] Cover letter builder
- [ ] Job matching algorithm
- [ ] Collaboration features
- [ ] Mobile app (React Native)
- [ ] Video interview prep

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [ReportLab Guide](https://www.reportlab.com/)
- [PostgreSQL Guide](https://www.postgresql.org/docs/)

---

## ✨ Credits

Built with ❤️ using:
- Django Framework
- Groq AI API
- ReportLab
- Bootstrap
- PostgreSQL

---

## 📊 Stats

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-5.0.6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

**Happy Resume Building! 📄✨**

*Last Updated: 2026-04-25*
