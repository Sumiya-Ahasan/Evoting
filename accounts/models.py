from django.db import models
from django.contrib.auth.models import User


class District(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Upazila(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="upazilas")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("district", "name")

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class Voter(models.Model):
    nid = models.CharField(max_length=30, unique=True)
    dob = models.DateField()
    full_name = models.CharField(max_length=200)

    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)

    gender = models.CharField(
        max_length=20,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True
    )
    blood_group = models.CharField(
        max_length=5,
        choices=[("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("O+","O+"),("O-","O-"),("AB+","AB+"),("AB-","AB-")],
        blank=True
    )

    district = models.ForeignKey(District, on_delete=models.PROTECT)
    upazila = models.ForeignKey(Upazila, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.full_name} ({self.nid})"


class ElectionCommissionerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return f"EC: {self.user.username} - {self.district.name}"
