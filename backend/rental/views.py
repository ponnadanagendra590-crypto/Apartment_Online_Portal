from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Apartment
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .serializer import ApartmentSerializer

# API view
@api_view(['GET'])
def apartment_api_list(request):
    apartments = Apartment.objects.all()
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)

# Template views
def apartment_list_page(request):
    apartments = Apartment.objects.all()
    return render(request, 'apartment_list.html', {'apartments': apartments})

def apartment_detail_page(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    return render(request, 'apartment_detail.html', {'apartment': apartment})

@login_required(login_url='rental:login')
def apartment_form_page(request, pk=None):
    # basic create/edit form handler (keeps minimal fields matching model)
    if pk:
        apartment = get_object_or_404(Apartment, pk=pk)
    else:
        apartment = None

    if request.method == 'POST':
        title = request.POST.get('title')
        city = request.POST.get('address') or request.POST.get('city') or ''
        try:
            rent = int(float(request.POST.get('price') or request.POST.get('rent') or 0))
        except Exception:
            rent = 0

        beds = int(request.POST.get('beds') or 0)
        baths = int(request.POST.get('baths') or 0)
        area = request.POST.get('area') or None
        address = request.POST.get('address') or ''
        description = request.POST.get('description') or ''

        owner = request.user if getattr(request, 'user', None) and request.user.is_authenticated else User.objects.first()

        if apartment:
            apartment.title = title or apartment.title
            apartment.city = city or apartment.city
            apartment.rent = rent or apartment.rent
            apartment.beds = beds
            apartment.baths = baths
            apartment.area = area or apartment.area
            apartment.address = address
            apartment.description = description
            apartment.owner = owner or apartment.owner
            apartment.save()
        else:
            apartment = Apartment.objects.create(
                title=title or 'Untitled',
                city=city or '',
                rent=rent or 0,
                owner=owner,
                beds=beds,
                baths=baths,
                area=area or None,
                address=address,
                description=description,
            )

        # handle uploaded images
        files = request.FILES.getlist('images')
        for f in files:
            from .models import ApartmentImage

            ApartmentImage.objects.create(apartment=apartment, image=f)

        return redirect(reverse('rental:apartment_detail', args=[apartment.pk]))
    return render(request, 'apartment_form.html', {'apartment': apartment})

@login_required(login_url='rental:login')
def apartment_delete(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'POST':
        apartment.delete()
        return redirect('rental:dashboard')
    return render(request, 'apartment_confirm_delete.html', {'apartment': apartment})

def dashboard_page(request):
    total = Apartment.objects.count()
    recent = Apartment.objects.order_by('-id')[:5]
    return render(request, 'dashboard.html', {'total': total, 'recent': recent})
# Authentication views
def login_page(request):
    if request.user.is_authenticated:
        return redirect('rental:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'error': 'Account not verified. Please check your email for the verification code.'})
            login(request, user)
            next_url = request.GET.get('next', 'rental:dashboard')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('rental:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists() and email:
            return render(request, 'register.html', {'error': 'Email already registered'})
        
        # Create user (inactive until email verification)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.is_active = False
        user.save()

        # create OTP and send email
        if email:
            otp = EmailOTP.create_otp_for_user(user)
            subject = 'Your Apartment Portal verification code'
            message = f'Hello {user.username},\n\nYour verification code is: {otp.code}\nIt will expire in 15 minutes.\n\nIf you did not request this, please ignore this email.'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
            try:
                send_mail(subject, message, from_email, [email])
            except Exception:
                # swallow email errors for dev, still allow verification by showing code in UI if needed
                pass

        # redirect to verification page
        request.session['pending_verification_user'] = user.pk
        return redirect('rental:verify_email')
    
    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('rental:dashboard')


def verify_email(request):
    user_pk = request.session.get('pending_verification_user')
    user = None
    if user_pk:
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            user = None

    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'verify_email.html', {'error': 'Invalid username'})

        otp_qs = EmailOTP.objects.filter(user=target_user, code=code, is_used=False).order_by('-created_at')
        if not otp_qs:
            return render(request, 'verify_email.html', {'error': 'Invalid code', 'user': target_user})

        otp = otp_qs[0]
        if not otp.is_valid():
            return render(request, 'verify_email.html', {'error': 'Code expired', 'user': target_user})

        otp.mark_used()
        target_user.is_active = True
        target_user.save()
        login(request, target_user)
        # clear session
        request.session.pop('pending_verification_user', None)
        return redirect('rental:dashboard')

    return render(request, 'verify_email.html', {'user': user})


def resend_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'verify_email.html', {'error': 'Invalid username'})

        if not user.email:
            return render(request, 'verify_email.html', {'error': 'No email on file', 'user': user})

        otp = EmailOTP.create_otp_for_user(user)
        subject = 'Your new verification code'
        message = f'Hello {user.username},\n\nYour new verification code is: {otp.code}\nIt will expire in 15 minutes.'
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        try:
            send_mail(subject, message, from_email, [user.email])
        except Exception:
            pass

        request.session['pending_verification_user'] = user.pk
        return render(request, 'verify_email.html', {'message': 'OTP resent', 'user': user})