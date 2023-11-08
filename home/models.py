import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.functional import cached_property


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
        return reverse("home:worker-detail", kwargs={"pk": self.pk})

    def check_if_online(self) -> bool:
        last_login = self.last_login
        if last_login:
            now = timezone.now()
            if now - last_login <= datetime.timedelta(seconds=settings.SESSION_EXPIRE_SECONDS):
                return True
        return False


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    teammates = models.ManyToManyField(Worker, related_name="teams")

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

    @cached_property
    def get_completion(self) -> int:
        total = self.tasks.all()
        completed = total.filter(
            is_completed=True
        )
        if total.count() == 0:
            return 0
        return int(round((completed.count() / total.count())/5.0 * 100, 0)*5.0)


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
