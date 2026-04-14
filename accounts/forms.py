from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rf-form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rf-form-control', 'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'rf-form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'rf-form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'rf-form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'rf-form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'rf-form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'rf-form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'rf-form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'rf-form-control'}),
            'bio': forms.Textarea(attrs={'class': 'rf-form-control', 'rows': 3}),
        }
