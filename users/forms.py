from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from .models import User
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")  # Modify the field label

    def clean(self):
        user_username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # Allow login with either username or email
        user = authenticate(self.request, username=user_username, password=password)
        if user is None:
            # If authentication fails, try logging in as email
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model() 
                user = User.objects.get(email=user_username)  # Fetch user by email
                user = authenticate(self.request, username=user.username, password=password)

            except User.DoesNotExist:
                pass

        if user is None:
            raise forms.ValidationError("Invalid username/email or password.")

        self.user_cache = user
        return self.cleaned_data

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'name', 'dob', 'country', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set optional fields
        self.fields['email'].required = False  # Email is optional
        self.fields['name'].required = False  # Name is optional
        self.fields['dob'].required = False  # Date of birth is optional
        self.fields['country'].required = False  # Country is optional
        self.fields['profile_pic'].required = False  # Profile picture is optional

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and email != self.instance.email:
            # Mark email as unverified
            self.instance.is_email_verified = False
        return email

    def clean(self):
        cleaned_data = super().clean()
        # Additional custom validation logic (if needed)
        return cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ['current_password', 'new_password1', 'new_password2']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if current_password:
            # Ensure that the current password is correct
            user = self.user
            if not user.check_password(current_password):
                raise ValidationError("The current password is incorrect.")
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise ValidationError("The two password fields must match.")
        return new_password2

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email Address",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your registered email',
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new password',
        }),
        help_text="Your password must be at least 8 characters long and include numbers or special characters."
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password',
        }),
    )