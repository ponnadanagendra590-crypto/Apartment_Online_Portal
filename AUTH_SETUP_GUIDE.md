# Authentication Setup Guide

## Overview
The Apartment Rental Portal now includes a complete authentication system with login, registration, and logout functionality.

## Features Added

### 1. **Authentication Views** (`backend/rental/views.py`)
- `login_page()` - Handles user login with username/password
- `register_page()` - Creates new user accounts with validation
- `logout_page()` - Logs out authenticated users
- `apartment_form_page()` - Now requires authentication (decorated with `@login_required`)

### 2. **Authentication URLs** (`backend/rental/urls.py`)
```
/Portal/login/        - User login page
/Portal/register/     - User registration page
/Portal/logout/       - User logout (redirect to dashboard)
```

### 3. **Templates**
- **base.html** - Master template with responsive navbar
  - Shows user name when logged in
  - Displays login/register buttons when logged out
  - Navigation links with URL reversing

- **login.html** - Clean login form
  - Username and password fields
  - Error message display
  - Link to register page

- **register.html** - User registration form
  - Username, email, first name, last name fields
  - Password confirmation validation
  - Link back to login page

### 4. **Template Updates**
All apartment-related templates now:
- Extend `base.html` for consistent styling
- Use Django template URL reversing (`{% url %}` tag)
- Include improved styling with gradients and hover effects
- Show authentication status in navigation

## Usage

### Starting the Development Server
```bash
cd backend
python manage.py runserver
```

Then visit: `http://localhost:8000/Portal/`

### User Registration
1. Click **Register** button in navbar
2. Fill in username and password (email/name optional)
3. Confirm password matches
4. Click **Register**
5. You'll be automatically logged in and redirected to dashboard

### Logging In
1. Click **Login** button in navbar
2. Enter username and password
3. Click **Login**
4. Redirected to dashboard on success

### Adding Apartment Listings
1. Ensure you're logged in
2. Click **+ Add Apartment** button in navbar
3. Fill in apartment details:
   - Title (required)
   - Monthly Rent (required)
   - Bedrooms, Bathrooms, Area (optional)
   - Address (required)
   - City (required)
   - Description (optional)
   - Upload photos (optional, up to 8 previewed)
4. Click **Save Listing**

### Logging Out
1. Click **Logout** button in navbar (only visible when logged in)
2. Redirected to dashboard

## Technical Details

### Authentication Flow
1. **Registration**: User submits form → validation → User created in database → Auto-login
2. **Login**: User submits credentials → Django authenticate() → Session created → Redirect to dashboard
3. **Logout**: User clicks logout → Session destroyed → Redirect to dashboard
4. **Protected Views**: Accessing apartment form without login → Redirect to login page

### User Model
Uses Django's built-in `User` model with:
- `username` - Unique identifier
- `email` - Optional email address
- `first_name` - Optional first name
- `last_name` - Optional last name
- `password` - Hashed password

### Apartment Ownership
Each apartment has an `owner` field (ForeignKey to User):
```python
owner = models.ForeignKey(User, on_delete=models.CASCADE)
```

Currently, apartments assigned to the logged-in user on creation.

## Styling

### Color Scheme
- **Primary Gradient**: `#667eea` → `#764ba2` (purple)
- **Background**: Linear gradient background
- **Text**: Dark gray `#2d3748`
- **Accents**: Light gray `#e2e8f0`

### Responsive Design
- Mobile-friendly layouts
- Grid-based gallery for apartments
- Flexible navigation bar

## Future Enhancements

Potential improvements:
1. Email verification on registration
2. Password reset functionality
3. User profile pages
4. Apartment filtering by owner
5. Save favorite apartments
6. Message apartment owners
7. Social login (Google, GitHub)
8. Two-factor authentication

## Troubleshooting

### "Login required" error when adding apartment
- Make sure you're logged in
- Click login button in navbar if not authenticated

### Incorrect password error
- Ensure caps lock is off
- Password is case-sensitive
- Whitespace matters

### Can't register with username
- Username already exists
- Choose a different username
- Usernames are unique

### Session timeout
- Sessions expire after configured time
- Click login to create new session
- Clear browser cookies if having issues

## Environment Configuration

Key settings in `backend/settings.py`:
```python
LOGIN_URL = 'rental:login'  # Default redirect for @login_required
INSTALLED_APPS = [
    'django.contrib.auth',      # Authentication
    'django.contrib.contenttypes',
    'rental',                   # Your app
]
```

## Security Notes

✅ **Implemented**:
- Password hashing (Django default)
- CSRF token protection on forms
- SQL injection prevention (ORM)
- Session-based authentication

⚠️ **Production Checklist**:
- [ ] Set `DEBUG = False`
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Set secure cookies (`SESSION_COOKIE_SECURE = True`)
- [ ] Enable HSTS
- [ ] Use environment variables for secrets
