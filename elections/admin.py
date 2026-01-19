from django.contrib import admin
from .models import Election, Symbol, Candidate, Vote

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("-created_at",)

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("voter", "district", "status", "is_party_nomination", "party_name", "assigned_symbol", "submitted_at")
    list_filter = ("status", "district", "is_party_nomination")
    search_fields = ("voter__full_name", "voter__nid", "party_name", "district__name")
    ordering = ("district__name", "-submitted_at")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("voter", "candidate", "election", "created_at")
    list_filter = ("election", "candidate__district")
    search_fields = ("voter__nid", "candidate__voter__full_name")
    ordering = ("-created_at",)
