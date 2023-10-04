from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        related_name="workers",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ["position"]

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> str:
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    teammates = models.ManyToManyField(Worker)

    def __str__(self) -> str:
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    team = models.ForeignKey(
        Team,
        related_name="projects",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    TASK_PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Middle", "Middle"),
        ("Low", "Low"),
    ]
    priority = models.CharField(
        max_length=255,
        choices=TASK_PRIORITY_CHOICES,
        default="Low",
    )
    task_type = models.ForeignKey(
        TaskType,
        related_name="tasks",
        on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    project = models.ForeignKey(
        Project,
        related_name="tasks",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.name}"
