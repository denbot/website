import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class DenbotUserManager(models.Manager):
    def create_user(  # noqa: ANN201
        self, phone: str, date_of_birth: str = "1900-01-01", id: str = None
    ):
        """
        :rtype: DenbotUser
        """
        # Create a normal site user.

        if id is None:
            # To make it easier in code, we assume we won't get an ID and generate it
            # here. On the command line, the createsuperuser command had to be
            # overridden to prevent asking the user for this field.
            id = uuid.uuid4()
        if phone is None:
            raise Exception("User must have a phone number")
        if date_of_birth is None:
            raise Exception("User must have a date of birth")

        user = self.model(id=id, phone=phone, date_of_birth=date_of_birth)

        user.save(using=self._db)
        return user

    def create_superuser(  # noqa: ANN201
        self, phone: str, date_of_birth: str = "1900-01-01", id: str = None
    ):
        """
        :rtype: DenbotUser
        """
        # Create a user that can access the admin panels. This is usually done via
        # command line for development. We call the normal create_user endpoint to
        # de-duplicate field validation.

        user = self.create_user(
            phone=phone,
            date_of_birth=date_of_birth,
            id=id,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, primary_key: str):  # noqa: ANN201
        """
        :rtype: DenbotUser
        """
        return self.get(**{self.model.USERNAME_FIELD: primary_key})

    def get_or_create_user(self, phone: str):  # noqa: ANN201
        """
        :rtype: DenbotUser
        """
        try:
            return self.get(phone=phone)
        except self.model.DoesNotExist:
            user = self.create_user(phone=phone)
            return user


class DenbotUser(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    date_of_birth = models.DateField()

    phone = PhoneNumberField(unique=True)
    phone_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    last_login = models.DateTimeField(_("last login"), null=True, blank=True)

    objects = DenbotUserManager()

    REQUIRED_FIELDS = ["date_of_birth", "phone"]
    USERNAME_FIELD = "id"

    class Meta:
        indexes = [
            # We most often key off of the user's phone number and id
            models.Index(fields=["phone"], name="user_phone_idx"),
            models.Index(fields=["id"], name="user_id_idx"),
        ]

    @property
    def is_anonymous(self) -> bool:
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self) -> bool:
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
