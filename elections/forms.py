from django import forms
from .models import Candidate

class NominationForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            "is_party_nomination",
            "party_name",
            "education",
            "yearly_income",
            "total_properties",
            "any_police_case",
            "dual_citizen",
            "preferred_symbol_name",
        ]
        widgets = {
            "is_party_nomination": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "party_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Party name (if any)"}),
            "education": forms.TextInput(attrs={"class": "form-control", "placeholder": "Education"}),
            "yearly_income": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Yearly income"}),
            "total_properties": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total properties"}),
            "any_police_case": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dual_citizen": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "preferred_symbol_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Preferred symbol"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("is_party_nomination") and not cleaned.get("party_name"):
            raise forms.ValidationError("Party name is required for party nomination.")
        return cleaned
