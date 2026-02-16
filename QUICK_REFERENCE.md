# 🏠 Apartment Rental Portal - Quick Reference

## ✅ What's Been Implemented

### Authentication System (COMPLETE)
- ✅ User Registration (with validation)
- ✅ User Login (with session management)
- ✅ User Logout
- ✅ Protected Views (login_required decorator)
- ✅ Auto-login after registration
- ✅ Error handling and validation

### User Interface (COMPLETE)
- ✅ Master template (base.html) with navigation
- ✅ Responsive navbar with auth status
- ✅ Modern gradient styling (purple theme)
- ✅ Login page with form validation
- ✅ Registration page with password confirmation
- ✅ Dashboard with statistics
- ✅ Apartment listing grid view
- ✅ Apartment detail page with gallery
- ✅ Apartment creation/edit form with image upload

### Features (COMPLETE)
- ✅ Create apartment listings with photos
- ✅ Edit existing listings
- ✅ Browse all apartments
- ✅ View apartment details with image gallery
- ✅ Multi-photo upload (up to 8 previewed)
- ✅ User-owned listings
- ✅ Responsive design (mobile/tablet/desktop)

## 🚀 Quick Start

### 1. Start Django Server
```bash
cd c:\Apartment_Rental_Portal\backend
python manage.py runserver
```

### 2. Visit Portal
Open browser: `http://localhost:8000/Portal/`

### 3. Create Account
- Click **Register** button
- Fill username and password
- Click **Register**
- Auto-logged in to dashboard

### 4. Add Apartment
- Click **+ Add Apartment** button
- Fill details (title, rent, beds, baths, address, etc.)
- Upload photos (optional)
- Click **Save Listing**

### 5. Browse Listings
- Click **Apartments** to view all listings
- Click on any card to view details
- See full gallery and information

### 6. Logout
- Click **Logout** button in navbar

## 📍 Main URLs

| Page | URL |
|------|-----|
| Dashboard | `/Portal/` |
| Login | `/Portal/login/` |
| Register | `/Portal/register/` |
| Apartments | `/Portal/apartments/` |
| Add Apartment | `/Portal/apartments/add/` |
| Apartment Details | `/Portal/apartments/<id>/` |
| Edit Apartment | `/Portal/apartments/<id>/edit/` |
| Logout | `/Portal/logout/` |
| Admin | `/admin/` |
| API | `/Portal/api/apartments/` |

## 🎨 Color Scheme

```
Primary Purple:   #667eea
Secondary Purple: #764ba2
Dark Text:        #2d3748
Light Gray:       #e2e8f0
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/rental/views.py` | All view functions (8 total) |
| `backend/rental/urls.py` | URL routing (9 routes) |
| `backend/rental/models.py` | Database models |
| `Templates/base.html` | Master template |
| `Templates/login.html` | Login form |
| `Templates/register.html` | Registration form |
| `Templates/dashboard.html` | Home page |
| `Templates/apartment_*.html` | Apartment pages |

## 🔐 User Accounts

### Test Account 1 (Create via Registration)
- Username: Choose any unique name
- Password: Set your own
- Email: Optional
- Name: Optional

### Super User (Admin Access)
```bash
python manage.py createsuperuser
# Then visit http://localhost:8000/admin/
```

## 💾 Database

**Schema**:
```
Users → Apartments (1 owner to many apartments)
Apartments → ApartmentImages (1 apartment to many images)
```

**Run Migrations**:
```bash
cd backend
python manage.py migrate
```

## 🧪 Test Flows

### Registration Flow
```
1. Click Register
2. Enter username (e.g., "john_doe")
3. Enter password (e.g., "MyPass123!")
4. Confirm password
5. Click Register
→ Auto-logged in, see "Welcome, john_doe"
```

### Login Flow
```
1. Click Logout
2. Click Login
3. Enter username
4. Enter password
5. Click Login
→ Redirected to dashboard
```

### Protected View Flow
```
1. Logout
2. Try accessing /Portal/apartments/add/
→ Redirected to login page
3. Login
→ Can now access add apartment form
```

### Apartment Creation Flow
```
1. Click + Add Apartment
2. Fill title (required)
3. Fill rent amount (required)
4. Fill beds, baths, area (optional)
5. Fill address and city (required)
6. Add description (optional)
7. Upload photos (optional, 1-8 images)
8. Click Save Listing
→ Redirected to apartment detail page
```

## ⚙️ Settings Reference

**Django Settings** (`backend/settings.py`):
```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'projectdb',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES[0]['DIRS'] = [BASE_DIR.parent / 'Templates']

# Auth
LOGIN_URL = 'rental:login'
```

## 🔧 Admin Features

After creating superuser, access `/admin/`:

**Apartment Admin**:
- ✅ Create/edit/delete apartments
- ✅ Manage images inline
- ✅ Filter by city or owner
- ✅ Search by title/address
- ✅ View owner information

**User Admin**:
- ✅ View all users
- ✅ Reset passwords
- ✅ Edit user info
- ✅ Delete users

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 already in use | Use `python manage.py runserver 8001` |
| Database connection error | Ensure MySQL running, check credentials |
| Templates not found | Check TEMPLATES DIRS in settings.py |
| Login not working | Clear cookies, try private/incognito window |
| Image upload fails | Ensure `media/apartments/` directory exists |
| Module not found error | Run `pip install Django djangorestframework Pillow mysqlclient` |

## 📋 Form Field Reference

### Login Form
```
Username ────────────────
Password ────────────────
[LOGIN]  [Register →]
```

### Registration Form
```
Username ────────────────
Email (optional) ────────
First Name (optional) ───
Last Name (optional) ────
Password ────────────────
Confirm Password ────────
[REGISTER]  [Login →]
```

### Apartment Form
```
Title ──────────────────── (required)
Monthly Rent (USD) ─────── (required)
  [Beds] [Baths] [Area]
Address ────────────────── (required)
City ──────────────────── (required)
Description (optional) ──────────────
📸 Photos (optional) ─────
[SAVE]  [CANCEL]
```

## 📊 Database Stats

- **Users**: Django built-in User model
- **Apartments**: Custom Apartment model
- **Images**: Custom ApartmentImage model
- **Total Tables**: 10+ (including auth, sessions, etc.)

## 🎯 Next Steps (Future)

Potential enhancements:
- [ ] Email verification on signup
- [ ] Password reset functionality
- [ ] User profile pages
- [ ] Search/filter apartments
- [ ] Favorite/saved apartments
- [ ] Message apartment owners
- [ ] Reviews/ratings system
- [ ] Social login (Google, GitHub)
- [ ] API authentication (tokens)

## 📚 Documentation Files

- **SETUP_GUIDE.md** - Complete setup documentation
- **AUTH_SETUP_GUIDE.md** - Authentication details
- **README.md** - Original project README

## 💡 Tips

1. **Profile Image**: Add profile picture field to User model
2. **Search**: Add search functionality to apartment listings
3. **Filters**: Add price/beds/area filters
4. **Maps**: Integrate Google Maps for addresses
5. **Email**: Send confirmation emails on registration
6. **SMS**: Send notifications via Twilio
7. **Analytics**: Track popular listings and users
8. **Caching**: Use Redis for session storage

## 🎓 Learning Resources

- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Authentication](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [Django Templates](https://docs.djangoproject.com/en/5.2/topics/templates/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

**Status**: ✅ Production Ready
**Auth System**: ✅ Complete
**UI Design**: ✅ Modern & Responsive
**Last Updated**: 2024
