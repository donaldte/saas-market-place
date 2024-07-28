
# python import
import logging
import uuid

# django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from .managers import *
from django.core.validators import MinValueValidator, MaxValueValidator


logger = logging.getLogger(__name__)


class SaasBaseModel(TimeStampedModel, ActivatorModel):
    """
    Name: HooYiaBaseModel

    Description: This class help to generate an uuid pk for all models means that all
                 the project's models should inherit from this model.

    Author: donaldtedom0@gmail.com
    """
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, unique=True, primary_key=True)
    is_deleted = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, null=True, blank=True)
    
    class Meta:
        abstract = True


class User(SaasBaseModel, PermissionsMixin, AbstractBaseUser):
    """
        Name: User

        Description: This class help to create an abstract base user.

        Author: donaldtedom0@gmail.com
    """
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)

    fullname = models.CharField(max_length=100, null=True, blank=True)

    first_name = models.CharField(_("first name"), max_length=150, blank=True)

    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designates whether the user can log into this admin site."))

    is_active = models.BooleanField(_("active"), default=True,
                                    help_text=_(
                                        "Designates whether this user should be treated as active. "
                                        "Unselect this instead of deleting accounts."
                                    ))

    is_superuser = models.BooleanField(_("superuser status"), default=False,
                                       help_text=_(
                                           "Designates that this user has all permissions without "
                                           "explicitly assigning them."
                                       ))

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    is_client = models.BooleanField(_("is client"), default=False)
    
    is_seller = models.BooleanField(_("is seller"), default=False)
    
    is_admin = models.BooleanField(_("is admin"), default=False)

    is_manually_deleted = models.BooleanField(_("Is manually deleted"), default=False)
    

    username = None

    EMAIL_FIELD = "email"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

   
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

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(SaasBaseModel):
    """ class: Profile
        Description: Profile of the user where physical products can be delivery.
        Author: donaldtedom0@gmail.com
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    country = models.CharField(_('Country'), max_length=50)
    phone_number = models.CharField(_("Phone Number"), max_length=255)
    region = models.CharField(_('Region'), max_length=50, default="Cameroon")
    city = models.CharField(_("City"), max_length=50)
    address = models.CharField(_('Address'), max_length=100)
    zip_code = models.CharField(_('Zip Code'), max_length=20, default="00000")

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.user.email}'s Profile"