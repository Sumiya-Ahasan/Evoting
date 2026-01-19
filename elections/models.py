from django.db import models
from django.utils import timezone
from accounts.models import Voter, District

class Election(models.Model):
    name = models.CharField(max_length=200, default="General Election")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Symbol(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)

    is_party_nomination = models.BooleanField(default=False)
    party_name = models.CharField(max_length=150, blank=True)

    education = models.CharField(max_length=200, blank=True)
    yearly_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_properties = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    any_police_case = models.BooleanField(default=False)
    dual_citizen = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("EC_RECOMMENDED", "EC_RECOMMENDED"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    district = models.ForeignKey(District, on_delete=models.PROTECT)

    preferred_symbol_name = models.CharField(max_length=100, blank=True)
    assigned_symbol = models.ForeignKey(Symbol, on_delete=models.SET_NULL, null=True, blank=True)

    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Candidate: {self.voter.full_name} ({self.status})"

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("election", "voter")

    def __str__(self):
        return f"{self.voter.nid} -> {self.candidate.voter.full_name}"
