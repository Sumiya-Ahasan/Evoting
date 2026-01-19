from .models import Voter, ElectionCommissionerProfile

def auth_context(request):
    voter_id = request.session.get("voter_id")
    voter = None
    if voter_id:
        voter = Voter.objects.filter(id=voter_id).select_related("district", "upazila").first()

    ec_profile = None
    if request.user.is_authenticated:
        ec_profile = ElectionCommissionerProfile.objects.filter(user=request.user).select_related("district").first()

    return {
        "voter_logged_in": bool(voter),
        "voter_obj": voter,

        "auth_logged_in": request.user.is_authenticated,
        "auth_user": request.user if request.user.is_authenticated else None,

        "ec_logged_in": bool(ec_profile),
        "ec_profile": ec_profile,
        "is_admin_user": bool(request.user.is_authenticated and request.user.is_superuser),
    }
