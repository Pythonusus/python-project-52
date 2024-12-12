from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusesIndexView.as_view(), name='statuses_index'),
]

