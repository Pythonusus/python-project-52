from django.utils.translation import gettext_lazy as _


base = {
    'task_manager': _('Task Manager'),
    'logo_alt': _('Logo'),
    'users': _('Users'),
    'login': _('Login'),
    'register': _('Register'),
    'logout': _('Logout'),
    'statuses': _('Statuses'),
    'labels': _('Labels'),
    'tasks': _('Tasks'),
    'author': _('Author'),
}


create_user = {
    'registration': _('Registration'),
    'register': _('Register'),
    'register_success': _('User registered successfully'),
}


update_user = {
    'edit_user': _('Edit user'),
    'update': _('Update'),
    'update_success': _('User updated successfully'),
}

delete_user = {
    'delete_user': _('Delete user'),
    'delete_confirm': _('Are you sure you want to delete this user?'),
    'delete_anyway': _('Delete anyway'),
    'delete_success': _('User deleted successfully'),
}

auth = {
    'permission_required': _('Permission required'),
    'auth_required': _('Authentication required'),
}

users_index = {
    'users': _('Users'),
    'id': _('ID'),
    'username': _('Username'),
    'full_name': _('Full name'),
    'created_at': _('Created at'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

login = {
    'login_button': _('Log in'),
    'login_success': _('You are logged in'),
}

logout = {
    'logout_info': _('You are logged out'),
}
