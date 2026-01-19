from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

from accounts.models import Voter
from .models import Candidate, Election, Vote
from .forms import NominationForm


def _get_active_election():
    return Election.objects.filter(is_active=True).order_by("-created_at").first()


def nomination_check(request):
    eligible = None
    voter = None
    message = None

    if request.method == "POST":
        nid = request.POST.get("nid", "").strip()
        voter = Voter.objects.filter(nid=nid).first()
        if voter:
            eligible = True
            message = "Eligible: voter found in database."
            request.session["nom_voter_id"] = voter.id
        else:
            eligible = False
            message = "Not eligible: NID not found."
            request.session.pop("nom_voter_id", None)

    return render(request, "elections/nomination_check.html", {
        "eligible": eligible, "voter": voter, "message": message
    })


def nomination_submit(request):
    voter_id = request.session.get("nom_voter_id")
    if not voter_id:
        return redirect("nomination_check")

    voter = get_object_or_404(Voter, id=voter_id)

    if Candidate.objects.filter(voter=voter).exists():
        return render(request, "elections/nomination_form.html", {"already": True, "voter": voter})

    form = NominationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        c = form.save(commit=False)
        c.voter = voter
        c.district = voter.district
        c.status = "PENDING"
        c.save()
        request.session.pop("nom_voter_id", None)
        return render(request, "elections/nomination_form.html", {"success": True, "voter": voter})

    return render(request, "elections/nomination_form.html", {"form": form, "voter": voter})


def ballot(request):
    voter_id = request.session.get("voter_id")
    if not voter_id:
        return redirect("voter_login")

    voter = get_object_or_404(Voter, id=voter_id)
    election = _get_active_election()
    if not election:
        return render(request, "elections/ballot.html", {"error": "No active election right now."})

    my_vote = Vote.objects.filter(election=election, voter=voter).select_related(
        "candidate", "candidate__voter", "candidate__assigned_symbol"
    ).first()

    # only FINAL approved candidates show in ballot
    candidates = Candidate.objects.filter(
        status="APPROVED",
        district=voter.district
    ).select_related("voter", "assigned_symbol")

    return render(request, "elections/ballot.html", {
        "voter": voter,
        "election": election,
        "candidates": candidates,
        "my_vote": my_vote,
        "error": None,
    })


def cast_vote(request, candidate_id):
    if request.method != "POST":
        return redirect("ballot")

    voter_id = request.session.get("voter_id")
    if not voter_id:
        return redirect("voter_login")

    voter = get_object_or_404(Voter, id=voter_id)
    election = _get_active_election()
    if not election:
        return redirect("ballot")

    if Vote.objects.filter(election=election, voter=voter).exists():
        return redirect("ballot")

    candidate = get_object_or_404(Candidate, id=candidate_id, status="APPROVED")

    if candidate.district_id != voter.district_id:
        return redirect("ballot")

    Vote.objects.create(election=election, voter=voter, candidate=candidate)
    return redirect("ballot")


def my_result(request):
    voter_id = request.session.get("voter_id")
    if not voter_id:
        return redirect("voter_login")

    voter = get_object_or_404(Voter, id=voter_id)
    election = _get_active_election()
    if not election:
        return render(request, "elections/my_result.html", {"error": "No active election."})

    candidate = Candidate.objects.filter(voter=voter, status="APPROVED").select_related("assigned_symbol").first()
    if not candidate:
        return render(request, "elections/my_result.html", {"not_candidate": True, "voter": voter, "election": election})

    total_votes = Vote.objects.filter(election=election, candidate=candidate).count()

    return render(request, "elections/my_result.html", {
        "voter": voter,
        "election": election,
        "candidate": candidate,
        "total_votes": total_votes,
    })


def results_page(request):
    return render(request, "elections/results.html")


def results_data(request):
    election = _get_active_election()
    if not election:
        return JsonResponse({"labels": [], "counts": [], "election": ""})

    qs = (
        Vote.objects.filter(election=election)
        .values("candidate__voter__full_name")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )
    labels = [x["candidate__voter__full_name"] for x in qs]
    counts = [x["cnt"] for x in qs]
    return JsonResponse({"labels": labels, "counts": counts, "election": election.name})


def voter_area_check(request):
    area = None
    voter = None
    message = None

    if request.method == "POST":
        nid = request.POST.get("nid", "").strip()
        voter = Voter.objects.filter(nid=nid).select_related("district", "upazila").first()
        if voter:
            area = f"{voter.upazila.name}, {voter.district.name}"
            message = "Area found."
        else:
            message = "NID not found."

    return render(request, "elections/voter_area_check.html", {"area": area, "voter": voter, "message": message})
