from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .account_manager import AccountManager
from django.utils.translation import gettext_lazy as _


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # required
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", 'first_name', 'last_name', 'phone_number']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        # db_name = "accounts"
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.city} {self.state}'

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfile")
        ordering = ["-id"]
