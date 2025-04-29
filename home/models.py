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


class Pokemon(models.Model):
    poke_id     = models.PositiveIntegerField(unique=True, help_text="ID from PokéAPI")
    name        = models.CharField(max_length=100)
    sprite      = models.URLField(blank=True, null=True)
    types       = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    health      = models.IntegerField(default=0)

    def __str__(self):
        return f"#{self.poke_id} {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collection = models.ManyToManyField(
        Pokemon,
        blank=True,
        related_name="owners",
        help_text="All Pokémon this user owns"
    )
    currency = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Trade(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_trades")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_trades")
    offered_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="offered_in_trades")
    requested_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="requested_in_trades")
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade from {self.sender.username} to {self.receiver.username}"