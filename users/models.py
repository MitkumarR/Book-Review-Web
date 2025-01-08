from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, username, password=None, **extra_fields):
        # if not email:
        #     raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)  # Unique username for identification
    email = models.EmailField(blank=False, null=False, unique=False)  # Non-unique email
    is_email_verified = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Handled securely by AbstractBaseUser
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )

    objects = CustomUserManager()

    # Make username the unique identifier
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']  # Email is still required, but not unique

    def __str__(self):
        return self.username
