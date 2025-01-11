import os

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from book_review import settings
from .models import User
from .forms import CustomAuthenticationForm, SignupForm, EditProfileForm, CustomPasswordChangeForm, \
    CustomSetPasswordForm, CustomPasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(CreateView):
    form_class = SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:signin")  # Redirect to signin page after signup

    def form_valid(self, form):
        self.object = form.save()  # Save the user
        login(self.request, self.object)  # Log the user in after signup (optional)
        return super().form_valid(form)

# Signin View
class SigninView(FormView):
    form_class = CustomAuthenticationForm  # Default Django authentication form
    template_name = "users/signin.html"
    success_url = reverse_lazy("users:profile")  # Redirect to profile or any post-login page

    def form_valid(self, form):
        # username = form.cleaned_data.get("username")
        # password = form.cleaned_data.get("password")
        # user = authenticate(self.request, username=username, password=password)

        user = form.user_cache

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password")
            return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "users/edit_profile.html"

    def form_valid(self, form):
        # Show success message on successful update
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Show error message if form is invalid
        messages.error(self.request, "There was an error updating your profile. Please check the form.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

    def get_success_url(self):
        # Redirect to the profile page after successful update
        return reverse('users:profile')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/password_change.html"

    def form_valid(self, form):
        # Save the new password
        user = form.save()
        # Update session auth hash to prevent the user from being logged out after password change
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Show error message if form is invalid
        messages.error(self.request, "There was an error changing your password.")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

    def get_success_url(self):
        # Redirect to the profile page after successful update
        return reverse('users:profile')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def generate_email_verification_link(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # return f"http://127.0.0.1:8000/users/verify_email/{uid}/{token}/"
    host = os.environ.get('ALLOWED_HOSTS')  # Default to localhost for development
    scheme = "https" if not settings.DEBUG else "http"  # Use HTTPS in production, HTTP in development
    return f"{scheme}://{host}/users/verify_email/{uid}/{token}/"
    # return f"https://{os.environ.get('ALLOWED_HOST')}/users/verify_email/{uid}/{token}/"


from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib import messages

def send_verification_email(request):
    user = request.user
    verification_link = generate_email_verification_link(user)
    send_mail(
        'Verify Your Email Address',
        f'Click the following link to verify your email: {verification_link}',
        os.environ.get("EMAIL_HOST_USER"),  # Replace with your email
        [user.email],
        fail_silently=False,
    )
    messages.info(request, "A verification email has been sent to your email address.(if not found, check spam folder)")
    messages.info(request, "A verification email has been sent to your email address.(if not get check your spam folder)")
    print( "A verification email has been sent to your email address.")
    return redirect('users:profile')

from django.utils.http import urlsafe_base64_decode

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()

        login(request, user)

        messages.success(request, "Your email has been successfully verified.")
        print( "Your email has been successfully verified.")

    else:
        messages.error(request, "The verification link is invalid or expired.")
    return redirect(reverse('users:profile'))


