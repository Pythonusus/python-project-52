from django.forms import ModelForm

from task_manager.labels.models import Label


class LabelForm(ModelForm):
    """
    Form for creating and updating labels.
    """
    class Meta:
        model = Label
        fields = [
            'name',
        ]
