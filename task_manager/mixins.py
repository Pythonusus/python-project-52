from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager import texts

OWNER_MAPPING = {
    'user': lambda x: x.id,
    'author': lambda x: x.author.id,
}


class OwnershipRequiredMixin(PermissionRequiredMixin):
    """
    Checks if the user is authenticated and has appropriate permissions.
    For users: allows managing only their own profiles.
    For tasks: allows managing only tasks authored by the user.
    """
    ownership_field = None  # 'user' for users, 'author' for tasks
    permission_denied_redirect_url = None     # 'users_index' or 'tasks_index'
    permission_denied_message = None

    def get_owner(self):
        """
        Returns the owner of the model object based on the ownership_field.
        Maps ownership fields to their corresponding values.
        """
        obj = self.get_object()

        return OWNER_MAPPING[self.ownership_field](obj)

    def has_permission(self):
        """
        Overriding has_permission method from PermissionRequiredMixin.
        Checks if the user has permission to manage the object.
        """
        return self.get_owner() == self.request.user.id

    def handle_no_permission(self):
        """
        Overriding handle_no_permission method from AccessMixin.
        If the user is not authenticated, redirects to the login page.
        If the user has no permission, redirects to the specified index page.
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return super().handle_no_permission()

        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse_lazy(self.permission_denied_redirect_url))
