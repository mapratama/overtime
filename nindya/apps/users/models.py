from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)

from django.db import models
from django.utils import timezone

from nindya.apps.overtimes.models import Overtime
from nindya.core.validators import validate_mobile_phone
from nindya.core.notifications import send_activated_user_notification

from model_utils import Choices


class CustomUserManager(UserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        now = timezone.now()
        user = self.model(email=email, is_active=True, is_staff=False,
                          last_login=now, is_superuser=False,
                          date_joined=now, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    email and password are required.
    """
    # Name, email and mobile needs to be case insensitive indexed in postgres
    email = models.EmailField(unique=True, null=True,
                              max_length=254, db_index=True)
    name = models.CharField('Nama', max_length=255, blank=True)
    no_file = models.CharField('No File', max_length=255, blank=True)
    mobile_number = models.CharField('Nomor Ponsel', max_length=30, unique=True,
                                     null=True, blank=True,
                                     validators=[validate_mobile_phone])
    TYPE = Choices(
        (1, 'admin', 'Admin'),
        (2, 'user', 'User'),
        (3, 'coordinator', 'Coordinator'),
        (4, 'manager', 'Manager'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, default=TYPE.user)

    position = models.CharField('Jabatan', max_length=255, blank=True, null=True)

    DEPARTMENT = Choices(
        (1, 'teknas', 'Teknas'),
        (2, 'keuangan', 'Keuangan'),
        (3, 'produksi', 'Produksi'),
    )
    department = models.PositiveSmallIntegerField(choices=DEPARTMENT, null=True, blank=True)
    push_notification_key = models.CharField(blank=True, default='', max_length=254)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('aktif', default=True)
    date_joined = models.DateTimeField('Tanggal Terdaftar', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.name or self.email or 'User #%d' % (self.id)

    # def save(self, *args, **kwargs):
    #     user_is_active = self.is_active
    #     print user_is_active
    #     user = super(User, self).save(*args, **kwargs)
    #     print user
    #     if user:
    #         print 'masuk'
    #         if user.is_active and user.is_active != user_is_active:
    #             send_activated_user_notification()
    #     return user

    def get_short_name(self):
        return self.email

    def get_overtimes(self):
        if self.type == User.TYPE.coordinator:
            return Overtime.objects.all()
        elif self.type == User.TYPE.manager:
            return Overtime.objects.exclude(status=Overtime.STATUS.bid)
        else:
            return self.overtimes.all()


def cached_auth_preprocessor(user, request):
    if not user.is_authenticated():
        return user
    return user
