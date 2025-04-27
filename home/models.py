from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = [
        ('user', 'User'),
        ('bug', 'Bug'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} by {self.reporter.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starter_pokemon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Pokemon(models.Model):
    poke_id     = models.PositiveIntegerField(unique=True, help_text="ID from PokéAPI")
    name        = models.CharField(max_length=100)
    sprite      = models.URLField(blank=True, null=True)
    types       = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    health      = models.IntegerField(default=0)

    def __str__(self):
        return f"#{self.poke_id} {self.name}"
