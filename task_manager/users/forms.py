from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
