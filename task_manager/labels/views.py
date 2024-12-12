from django.views.generic import TemplateView

import task_manager.texts as texts


class LabelsIndexView(TemplateView):
    template_name = 'labels/index.html'
    extra_context = {
        'base': texts.base,
    }
