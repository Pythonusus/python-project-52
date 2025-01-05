from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]


class UserUpdateForm(UserForm):
    """
    Form for updating a user.
    Built in UserUpdateForm from django.contrib.auth.forms is not used
    because it doesn't allow to update password together with user profile,
    which is required by client specification.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]

    def clean_username(self):
        """
        Validate the username field to ensure uniqueness regardless of case.
        Using clean_username implementation from UserCreationForm.
        The only difference is that we exclude current instance from the query.

        Returns:
            str: The validated username if it's unique (case-insensitive).

        Raises:
            ValidationError: If another user already exists with the same
            username (ignoring case), excluding the current instance.
        """
        username = self.cleaned_data.get("username")
        if (
            username
            and self._meta.model.objects.filter(
                username__iexact=username
            ).exclude(pk=self.instance.pk).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username
