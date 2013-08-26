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



