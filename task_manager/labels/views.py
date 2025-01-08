from django.views.generic import TemplateView

from task_manager import texts


class LabelsIndexView(TemplateView):
    template_name = 'labels/index.html'
    extra_context = {
        'base': texts.base,
    }
