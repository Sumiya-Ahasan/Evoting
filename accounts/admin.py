from django.contrib import admin
from .models import District, Upazila, Voter, ElectionCommissionerProfile

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Upazila)
class UpazilaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "district")
    list_filter = ("district",)
    search_fields = ("name", "district__name")
    ordering = ("district__name", "name")

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("nid", "full_name", "gender", "blood_group", "district", "upazila", "dob")
    list_filter = ("district", "upazila", "gender", "blood_group")
    search_fields = ("nid", "full_name", "father_name", "mother_name")
    ordering = ("district__name", "upazila__name")
    list_per_page = 25

@admin.register(ElectionCommissionerProfile)
class ElectionCommissionerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "district")
    list_filter = ("district",)
    search_fields = ("user__username", "district__name")
