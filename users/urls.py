from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import SigninView, SignupView, ProfileView, EditProfileView, send_verification_email, verify_email, \
    CustomPasswordChangeView, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.contrib.auth.views import LogoutView, PasswordChangeView
app_name = "users"

urlpatterns = [
    path("signin/", SigninView.as_view(), name="signin"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signout/", LogoutView.as_view(next_page="/"), name="signout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('verify_email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Add media URL patterns if in development mode
if settings.DEBUG:  # Ensures this only runs in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
