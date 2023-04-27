from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )
