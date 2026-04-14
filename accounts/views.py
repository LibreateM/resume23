from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm, ProfileUpdateForm
from .models import UserProfile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to ResumeForge, {user.first_name}!")
            return redirect('dashboard')
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, e)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        # Try email lookup
        try:
            u = User.objects.get(email=username_or_email)
            username = u.username
        except User.DoesNotExist:
            username = username_or_email
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'accounts/signin.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
