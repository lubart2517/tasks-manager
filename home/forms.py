from django import forms
from .models import Task, TaskType, Worker, Project


class TaskForm(forms.ModelForm):
    def __init__(self, team_id=0, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["assignees"] = forms.ModelMultipleChoiceField(
            queryset=Worker.objects.filter(teams__id=team_id),
            widget=forms.CheckboxSelectMultiple,
            required=True
        )

    class Meta:
        model = Task
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
