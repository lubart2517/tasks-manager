from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("workers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("teams/<int:pk>/", views.team_detail_view, name="team-detail"),
]

app_name = "home"
