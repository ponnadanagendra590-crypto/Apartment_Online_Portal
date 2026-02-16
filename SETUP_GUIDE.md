# Apartment Rental Portal - Complete Setup Summary

## 🎯 Project Overview
A Django-based apartment rental portal with user authentication, apartment listings with image uploads, and a modern responsive UI.

**Status**: ✅ Complete with Login/Register/Logout System

## 📁 Project Structure

```
Apartment_Rental_Portal/
├── backend/
│   ├── rental/
│   │   ├── models.py          (Apartment, ApartmentImage models)
│   │   ├── views.py           (API views + auth views)
│   │   ├── urls.py            (URL routing for rental app)
│   │   ├── admin.py           (Django admin configuration)
│   │   └── serializer.py      (DRF serializers)
│   ├── backend/
│   │   ├── settings.py        (Django configuration)
│   │   ├── urls.py            (Root URL configuration)
│   │   └── wsgi.py
│   ├── manage.py
│   └── media/                 (Uploaded apartment images)
│       └── apartments/
├── Templates/
│   ├── base.html              (Master template)
│   ├── dashboard.html         (Home/dashboard)
│   ├── login.html             (Login form)
│   ├── register.html          (Registration form)
│   ├── apartment_list.html    (Apartment listings)
│   ├── apartment_detail.html  (Single apartment view)
│   ├── apartment_form.html    (Create/edit apartment)
│   └── apartment_images/      (Image storage for templates)
├── frontend/
│   └── public/
│       ├── logo_apartment.svg
│       └── logo_apartment_mono.svg
├── docker-compose.yml
├── README.md
└── AUTH_SETUP_GUIDE.md        (This authentication guide)
```

## 🔐 Authentication System

### Views & Routes
| Route | View | Purpose |
|-------|------|---------|
| `/Portal/` | `dashboard_page()` | Dashboard (home) |
| `/Portal/login/` | `login_page()` | User login |
| `/Portal/register/` | `register_page()` | User registration |
| `/Portal/logout/` | `logout_page()` | User logout |
| `/Portal/apartments/` | `apartment_list_page()` | Browse apartments |
| `/Portal/apartments/add/` | `apartment_form_page()` | Create apartment (🔒 requires login) |
| `/Portal/apartments/<id>/` | `apartment_detail_page()` | View apartment details |
| `/Portal/apartments/<id>/edit/` | `apartment_form_page()` | Edit apartment (🔒 requires login) |
| `/Portal/api/apartments/` | `apartment_api_list()` | JSON API endpoint |

### Authentication Features
✅ User Registration with validation
✅ Password confirmation check
✅ User login with sessions
✅ Protected views (login_required)
✅ User logout with session cleanup
✅ Auto-login after registration
✅ Responsive navbar with auth status

## 💾 Database Models

### User Model
```python
User (Django built-in)
├── username (unique)
├── email
├── first_name
├── last_name
└── password (hashed)
```

### Apartment Model
```python
Apartment
├── title
├── city
├── rent (monthly price)
├── owner (ForeignKey → User)
├── beds
├── baths
├── area (sqft)
├── address
└── description
```

### ApartmentImage Model
```python
ApartmentImage
├── apartment (ForeignKey → Apartment)
├── image (ImageField, upload_to='apartments/')
├── caption
└── uploaded_at
```

## 🎨 Frontend Templates

### Template Hierarchy
```
base.html (master)
├── dashboard.html
├── login.html
├── register.html
├── apartment_list.html
├── apartment_detail.html
└── apartment_form.html
```

### Key Features
- **Responsive Design**: Works on mobile/tablet/desktop
- **Gradient Styling**: Purple gradient (#667eea → #764ba2)
- **Modern UI**: Rounded corners, shadows, hover effects
- **Form Validation**: Client-side HTML5 + server-side Python
- **Image Previews**: Client-side preview before upload
- **Error Handling**: User-friendly error messages

## 🚀 Getting Started

### Prerequisites
```
Python 3.12.5+
Django 5.2
Django REST Framework
Pillow (for image handling)
MySQLdb (for MySQL connection)
```

### Installation
```bash
# 1. Navigate to project
cd c:\Apartment_Rental_Portal

# 2. Install dependencies
pip install -r requirements.txt  # if available, or:
pip install Django==5.2 djangorestframework Pillow mysqlclient

# 3. Run migrations
cd backend
python manage.py migrate

# 4. Create superuser (optional, for admin)
python manage.py createsuperuser

# 5. Collect static files (production)
python manage.py collectstatic

# 6. Start development server
python manage.py runserver
```

### First Steps
1. Open `http://localhost:8000/Portal/`
2. Click **Register** to create account
3. Fill in username and password
4. Click **+ Add Apartment** to create listing
5. Upload apartment photos
6. View listings, edit, or logout

## 🔒 Security Features

✅ **Implemented**:
- CSRF token protection on all forms
- Password hashing (PBKDF2)
- SQL injection prevention (ORM)
- Session-based authentication
- HttpOnly session cookies
- Login required decorators

⚠️ **For Production**:
```python
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com']
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
```

## 📊 Database Configuration

**MySQL/MariaDB**
- Host: `localhost:3306`
- Database: `projectdb`
- Driver: `django.db.backends.mysql`
- Client: `MySQLdb`

## 🎯 Key View Functions

### Authentication Views
```python
def login_page(request):
    # Handle GET (show form) and POST (authenticate)
    # Redirect authenticated users to dashboard
    
def register_page(request):
    # Validate passwords match
    # Check username uniqueness
    # Create user and auto-login
    
def logout_page(request):
    # Destroy session and redirect
```

### Protected Views
```python
@login_required(login_url='rental:login')
def apartment_form_page(request, pk=None):
    # Only accessible to logged-in users
    # Redirect to login if not authenticated
```

## 🖼️ Image Handling

**Upload Process**:
1. User selects multiple images in apartment form
2. `apartment_form_page()` receives `request.FILES.getlist('images')`
3. Each file creates `ApartmentImage` record
4. Images stored in `MEDIA_ROOT/apartments/`
5. Accessible via `apartment.images.all` in templates

**Template Usage**:
```django
{% for img in apartment.images.all %}
  <img src="{{ img.image.url }}" alt="{{ apartment.title }}" />
{% endfor %}
```

## 📱 Responsive Breakpoints

- Desktop: 1200px+ (full layout)
- Tablet: 768px-1199px (flexible grid)
- Mobile: <768px (single column)

## 🧪 Testing the Auth Flow

### Test Register
```bash
1. Go to /Portal/register/
2. Enter: username=testuser, password=Test123!
3. Confirm password matches
4. Click Register
5. Should redirect to dashboard with "Welcome, testuser"
```

### Test Login
```bash
1. Click Logout
2. Go to /Portal/login/
3. Enter: username=testuser, password=Test123!
4. Click Login
5. Should redirect to dashboard
```

### Test Protected View
```bash
1. Logout
2. Try accessing /Portal/apartments/add/
3. Should redirect to login page
4. Login again to access
```

## 📝 Form Fields

### Login Form
- Username (required, text)
- Password (required, password)

### Register Form
- Username (required, text)
- Email (optional, email)
- First Name (optional, text)
- Last Name (optional, text)
- Password (required, password)
- Confirm Password (required, password)

### Apartment Form
- Title (required, text)
- Monthly Rent (required, number)
- Bedrooms (optional, number)
- Bathrooms (optional, number)
- Area in sqft (optional, number)
- Address (required, text)
- City (required, text)
- Description (optional, textarea)
- Photos (optional, multiple file upload)

## 🎨 Styling Details

### Colors
```css
Primary: #667eea (blue-purple)
Secondary: #764ba2 (darker purple)
Text: #2d3748 (dark gray)
Light BG: #f7fafc (very light gray)
Border: #e2e8f0 (light gray)
```

### Typography
- Font: Segoe UI, Roboto, Arial, sans-serif
- Headers: Bold, dark gray
- Body: Regular, medium gray

## 🔧 Admin Interface

Access at `/admin/`:
```bash
1. python manage.py createsuperuser
2. Go to http://localhost:8000/admin/
3. Login with superuser account
4. Manage apartments and images
```

**Admin Features**:
- View/edit/delete apartments
- Manage apartment images inline
- Filter by city or owner
- Search by title or address

## 📦 Dependencies

```
Django==5.2.0
djangorestframework
Pillow==11.3.0
mysqlclient
pytz
sqlparse
```

## ⚡ Performance Tips

1. **Image Optimization**: Compress images before upload
2. **Database Indexing**: Add indexes on frequently queried fields
3. **Caching**: Use Redis for session caching
4. **CDN**: Serve images from CDN in production
5. **Pagination**: Limit apartment listings per page

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| Database connection error | Check MySQL is running, credentials in settings |
| Image uploads fail | Ensure `media/apartments/` directory exists |
| Login not working | Clear cookies, check database migrations |
| Templates not found | Verify `TEMPLATES DIRS` in settings.py |

## 📚 Additional Resources

- [Django Authentication Docs](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Forms & Templates](https://docs.djangoproject.com/en/5.2/topics/forms/)

---

**Last Updated**: 2024
**Status**: Production Ready ✅
**License**: MIT
