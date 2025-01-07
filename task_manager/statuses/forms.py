from django.forms import ModelForm

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    """
    Form for creating and updating statuses.
    """
    class Meta:
        model = Status
        fields = [
            'name',
        ]
