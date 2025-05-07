from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

from .models import Signup1  # Import your model


# Register User model with admin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


# --- Forms ---

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    terms = forms.BooleanField(required=True)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
            
        return cleaned_data


# --- Views ---

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Save additional info to Signup1
                Signup1.objects.create(
                    user=user,
                    email=email,
                    password=user.password  # already hashed
                )

                messages.success(request, 'Account created successfully! Please login now.')
                return redirect('login')

            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignupForm()
    
    return render(request, "signup.html", {"form": form})


@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('query')
    results = None

    if query:
        headers = {
            'Accept': 'application/json'
        }
        base_url = "https://api.openverse.engineering/v1"

        try:
            image_response = requests.get(f"{base_url}/images", params={"q": query}, headers=headers)
            images = image_response.json().get("results", []) if image_response.status_code == 200 else []

            audio_response = requests.get(f"{base_url}/audio", params={"q": query}, headers=headers)
            audio = audio_response.json().get("results", []) if audio_response.status_code == 200 else []

            dummy_videos = [
                {
                    "url": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "title": "Sample Video 1"
                },
                {
                    "url": "https://www.w3schools.com/html/movie.mp4",
                    "title": "Sample Video 2"
                }
            ]

            results = {
                "images": images[:10],
                "audio": audio[:5],
                "videos": dummy_videos
            }

        except requests.RequestException as e:
            messages.error(request, f"Error fetching results: {str(e)}")

    return render(request, "dashboard.html", {
        "results": results,
        "query": query,
        "username": request.user.username
    })


def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def home_redirect(request):
    return redirect('login')
