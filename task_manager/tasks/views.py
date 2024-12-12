from django.views.generic import TemplateView

import task_manager.texts as texts


class TasksIndexView(TemplateView):
    template_name = 'tasks/index.html'
    extra_context = {
        'base': texts.base,
    }
