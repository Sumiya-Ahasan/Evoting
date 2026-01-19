from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import VoterLoginForm
from .models import Voter, ElectionCommissionerProfile
from elections.models import Candidate


def voter_login(request):
    form = VoterLoginForm(request.POST or None)
    error = None

    if request.method == "POST" and form.is_valid():
        nid = form.cleaned_data["nid"].strip()
        dob = form.cleaned_data["dob"]

        voter = Voter.objects.filter(nid=nid, dob=dob).first()
        if not voter:
            error = "Invalid NID or Date of Birth."
        else:
            request.session["voter_id"] = voter.id
            return redirect("ballot")

    return render(request, "accounts/voter_login.html", {"form": form, "error": error})


def voter_logout(request):
    request.session.pop("voter_id", None)
    return redirect("home")


def ec_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "Invalid username or password."
        else:
            login(request, user)
            return redirect("ec_dashboard")
    return render(request, "accounts/ec_login.html", {"error": error})


@require_POST
def ec_logout(request):
    logout(request)
    return redirect("home")


@login_required
def ec_dashboard(request):
    profile = ElectionCommissionerProfile.objects.filter(user=request.user).select_related("district").first()
    if not profile:
        return render(request, "accounts/ec_dashboard.html", {"error": "You are not assigned as a Zilla EC. Create an EC profile from Admin panel."})

    nominations = Candidate.objects.filter(district=profile.district).order_by("-submitted_at")
    return render(request, "accounts/ec_dashboard.html", {"profile": profile, "nominations": nominations})


@require_POST
@login_required
def ec_recommend(request, candidate_id):
    profile = ElectionCommissionerProfile.objects.filter(user=request.user).select_related("district").first()
    if not profile:
        return redirect("ec_dashboard")

    c = get_object_or_404(Candidate, id=candidate_id, district=profile.district)
    if c.status == "PENDING":
        c.status = "EC_RECOMMENDED"
        c.save()
    return redirect("ec_dashboard")


@require_POST
@login_required
def ec_reject(request, candidate_id):
    profile = ElectionCommissionerProfile.objects.filter(user=request.user).select_related("district").first()
    if not profile:
        return redirect("ec_dashboard")

    c = get_object_or_404(Candidate, id=candidate_id, district=profile.district)
    if c.status in ["PENDING", "EC_RECOMMENDED"]:
        c.status = "REJECTED"
        c.save()
    return redirect("ec_dashboard")
