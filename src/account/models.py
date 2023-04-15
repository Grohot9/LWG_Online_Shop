from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First name"), max_length=150)
    last_name = models.CharField(_("Last name"), max_length=150)
    email = models.EmailField(_("Email address"), unique=True)
    phone_number = PhoneNumberField(_("Phone number"), null=True, blank=True)
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)
    groups = models.ManyToManyField(Group, related_name="account_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="account_users", blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_working_time(self):
        return f"Time on site: {timezone.now() - self.date_joined}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.ForeignKey(
        "account.Role", on_delete=models.CASCADE, related_name="users"
    )


class Role(models.Model):
    class ROLES_CHOICES(models.TextChoices):
        CUSTOMER = "Customer", "Customer"
        SUPERVISOR = "Supervisor", "Supervisor"

    name = models.CharField(
        max_length=50, choices=ROLES_CHOICES.choices, default=ROLES_CHOICES.CUSTOMER
    )
    description = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)

    def assign_permissions(self):
        if self.name == "Supervisor":
            permissions = [
                "view_product",
                "add_product",
                "edit_product",
                "delete_product",
            ]
        else:
            permissions = ["view_product"]

        for permission in permissions:
            permission = Permission.objects.get(codename=permission)
            self.permissions.add(permission)

    def __str__(self):
        return f"{self.name}"
