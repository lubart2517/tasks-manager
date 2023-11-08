from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("workers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/complete", views.task_complete, name="task-complete"),
    path("teams/<int:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
]

app_name = "home"
