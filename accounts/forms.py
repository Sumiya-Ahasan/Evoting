from django import forms

class VoterLoginForm(forms.Form):
    nid = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter NID"})
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
