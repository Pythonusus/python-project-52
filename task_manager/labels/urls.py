from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.LabelsIndexView.as_view(), name='labels_index'),
]
