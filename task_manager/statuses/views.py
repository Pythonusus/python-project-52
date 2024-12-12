from django.views.generic import TemplateView

import task_manager.texts as texts


class StatusesIndexView(TemplateView):
    template_name = 'statuses/index.html'
    extra_context = {
        'base': texts.base,
    }
