from  django.db import models

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

class SurmandlUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, relation, password=None):
        if not email:
            msg = "Users must have a valid email address"
            raise ValueError(msg)

        user = self.model(
            email = SurmandlUserManager.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            relation = relation,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, relation, password):

        user = self.create_user(email, first_name=first_name, last_name=last_name, relation=relation, password=password)
        user.is_admim = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


USERNAME_FIELD = "email"
REQUIRED_FIELDS = ["first_name", "last_name", "relation",]

class SurmandlUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)

    USERNAME_FIELD = USERNAME_FIELD
    REQUIRED_FIELDS = REQUIRED_FIELDS

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = SurmandlUserManager()

    def get_full_name(self):
        return "%s, %s %s" % (self.email, self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)




