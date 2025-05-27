import uuid

from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand


class Command(SuperUserCommand):
    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]

        if username is None:
            # Generate the UUID as the username field. It's also our primary key. Using this method means the user
            # doesn't need to create a GUID themselves.
            options[self.UserModel.USERNAME_FIELD] = uuid.uuid4()

        super().handle(*args, **options)
