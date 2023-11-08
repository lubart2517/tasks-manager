from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views import generic
from django.contrib import messages
from .models import Project, Team, Worker, Task
from .forms import TaskForm, ProjectForm
from django import forms

def index(request):


    tasks = Task.objects.all().order_by("deadline").select_related(
        "task_type",
        "project"
    )
    tasks_styles = {
        "Bug": "ni-html5 text-danger",
        "New feature": "ni-cart text-info",
        "Breaking change": "ni-credit-card text-warning",
        "Refactoring": "ni-key-25 text-primary",
        "QA": "ni-bell-55 text-success"
    }
    tasks_with_style = [(task, tasks_styles[task.task_type.name]) for task in tasks]
    teams = Team.objects.all()
    workers = Worker.objects.all()
    projects = Project.objects.all().select_related("team").prefetch_related("tasks")
    context = {
        "projects": projects,
        "teams": teams,
        "workers": workers,
        "tasks": tasks_with_style,
    }

    # Page from the theme 
    return render(request, 'pages/index.html', context=context)


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class ProjectDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Project
    queryset = (Project.objects.
                select_related("team").
                prefetch_related(
                    "tasks__task_type",
                    "team__teammates__position"
                ).all())

    form_class = TaskForm

    def get_success_url(self) -> str:
        return reverse("home:project-detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs) -> dict:
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        form = TaskForm(self.object.team.id, initial={
            "project": self.object
        })
        form.fields["project"].widget = forms.HiddenInput()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if not request.user.is_authenticated:
            return self.form_invalid(form)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ProjectDetailView, self).form_valid(form)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = (Task.objects.
                select_related(
                    "task_type",
                    "project",
                    "project__team"
                    ).prefetch_related("assignees__position").all())


def task_complete(request: dict, pk: int):
    task = Task.objects.get(id=pk)
    if request.user in task.assignees.all():
        task.is_completed = True
        task.save()
        messages.success(request, 'Changes successfully saved.')
        return HttpResponseRedirect(reverse("home:task-detail", args=(pk,)))
    else:
        messages.error(request, "Only task assignees can do it")
        return HttpResponseRedirect(reverse("home:task-detail", args=(pk,)))



def team_detail_view(request: dict, pk: int) -> str:
    team = Team.objects.get(id=pk)
    context = {
        "projects": team.projects.all(),
        "team": team,
    }

    # Page from the theme
    return render(request, 'home/team_detail.html', context=context)


class TeamDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.all()

    form_class = ProjectForm

    def get_success_url(self) -> str:
        return reverse("home:team-detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs) -> dict:
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        form = ProjectForm( initial={
            "team": self.object
        })
        form.fields["team"].widget = forms.HiddenInput()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if not request.user.is_authenticated:
            return self.form_invalid(form)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(TeamDetailView, self).form_valid(form)

