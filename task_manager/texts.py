"""
Texts for i18n.
"""
from django.utils.translation import gettext_lazy as _

# Texts for the base layout
base = {
    'task_manager': _('Task Manager'),
    'logo_alt': _('Logo'),
    'users': _('Users'),
    'login': _('Login'),
    'registration': _('Registration'),
    'logout': _('Logout'),
    'statuses': _('Statuses'),
    'labels': _('Labels'),
    'tasks': _('Tasks'),
    'author': _('Author'),
}

# Texts for the index page
index = {
    'welcome': _('Welcome to the Task Manager!'),
    'description': _(
        'This is a simple task manager for life build with Django.'
    ),
    'possibilities': _(
        'You can create tasks with statuses and labels'
        'for them and assign them to users.'
    ),
    'see_more': _('See more'),
    'login_or_register': _('Please, login or register to continue.'),
}

# Texts for user models
user_model = {
    'first_name': _('First name'),
    'last_name': _('Last name'),
}

# Texts for the user creation page
create_user = {
    'registration': _('Registration'),
    'register': _('Register'),
    'register_success': _('User registered successfully'),
}

# Texts for the user update page
update_user = {
    'edit_user': _('Edit user'),
    'update': _('Update'),
    'update_success': _('User updated successfully'),
}

# Texts for the user deletion page
delete_user = {
    'delete_user': _('Delete user'),
    'delete_confirm': _('Are you sure you want to delete this user?'),
    'delete_anyway': _('Delete anyway'),
    'delete_success': _('User deleted successfully'),
}

# Texts for the authentication
auth = {
    'permission_required': _('Permission required'),
    'auth_required': _('Authentication required'),
}

# Texts for the users index page
users_index = {
    'users': _('Users'),
    'id': _('ID'),
    'username': _('Username'),
    'full_name': _('Full name'),
    'created_at': _('Created at'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

# Texts for the login page
login = {
    'login_button': _('Log in'),
    'login_success': _('You are logged in'),
}

# Texts for logout
logout = {
    'logout_info': _('You are logged out'),
}

# Texts for the status models
status_model = {
    'name': _('Name'),
    'created_at': _('Created at'),
}

# Texts for the statuses index page
statuses_index = {
    'statuses': _('Statuses'),
    'create_status': _('Create status'),
    'id': _('ID'),
    'name': _('Name'),
    'created_at': _('Created at'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

# Texts for the statuses create page
create_status = {
    'create_status': _('Create status'),
    'create': _('Create'),
    'create_success': _('Status created successfully'),
}

# Texts for the statuses update page
update_status = {
    'update_status': _('Update status'),
    'update': _('Update'),
    'update_success': _('Status updated successfully'),
}

# Texts for the statuses delete page
delete_status = {
    'delete_status': _('Delete status'),
    'delete_confirm': _('Are you sure you want to delete this status?'),
    'delete_anyway': _('Delete anyway'),
    'delete_success': _('Status deleted successfully'),
    'delete_error': _('Status cannot be deleted because it is in use'),
}

# Texts for the tasks model
task_model = {
    'name': _('Name'),
    'description': _('Description'),
    'status': _('Status'),
    'labels': _('Labels'),
    'author': _('Author'),
    'executor': _('Executor'),
    'created_at': _('Created at'),
}

# Texts for the tasks index page
tasks_index = {
    'tasks': _('Tasks'),
    'create_task': _('Create task'),
    'id': _('ID'),
    'name': _('Name'),
    'status': _('Status'),
    'label': _('Label'),
    'author': _('Author'),
    'executor': _('Executor'),
    'created_at': _('Created at'),
    'self_tasks': _('Self tasks'),
    'filter': _('Filter'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

# Texts for the tasks create page
create_task = {
    'create_task': _('Create task'),
    'create': _('Create'),
    'create_success': _('Task created successfully'),
}

# Texts for the tasks update page
update_task = {
    'update_task': _('Update task'),
    'update': _('Update'),
    'update_success': _('Task updated successfully'),
}

# Texts for the tasks delete page
delete_task = {
    'delete_task': _('Delete task'),
    'delete_confirm': _('Are you sure you want to delete this task?'),
    'delete_anyway': _('Delete anyway'),
    'delete_success': _('Task deleted successfully'),
    'delete_error': _('Task can be deleted only by the author'),
}

# Texts for the task view page
task_view = {
    'task_view': _('Task view'),
    'status': _('Status'),
    'labels': _('Labels'),
    'author': _('Author'),
    'executor': _('Executor'),
    'created_at': _('Created at'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

# Texts for the labels models
label_model = {
    'name': _('Name'),
    'created_at': _('Created at'),
}

# Texts for the labels index page
labels_index = {
    'labels': _('Labels'),
    'create_label': _('Create label'),
    'id': _('ID'),
    'name': _('Name'),
    'created_at': _('Created at'),
    'edit': _('Edit'),
    'delete': _('Delete'),
}

# Texts for the labels create page
create_label = {
    'create_label': _('Create label'),
    'create': _('Create'),
    'create_success': _('Label created successfully'),
}

# Texts for the labels update page
update_label = {
    'update_label': _('Update label'),
    'update': _('Update'),
    'update_success': _('Label updated successfully'),
}

# Texts for the labels delete page
delete_label = {
    'delete_label': _('Delete label'),
    'delete_confirm': _('Are you sure you want to delete this label?'),
    'delete_anyway': _('Delete anyway'),
    'delete_success': _('Label deleted successfully'),
    'delete_error': _('Label cannot be deleted because it is in use'),
}

# Texts for the 404 error page
error404 = {
    'error404': _('404 error'),
    'page_not_found': _('Page not found'),
}

# Texts for the 500 error page
error500 = {
    'error500': _('500 error'),
    'internal_server_error': _('Internal server error'),
}
