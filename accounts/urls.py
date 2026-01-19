from django.urls import path
from .views import (
    voter_login, voter_logout,
    ec_login, ec_logout, ec_dashboard,
    ec_recommend, ec_reject
)

urlpatterns = [
    path("voter-login/", voter_login, name="voter_login"),
    path("voter-logout/", voter_logout, name="voter_logout"),

    path("ec-login/", ec_login, name="ec_login"),
    path("ec-logout/", ec_logout, name="ec_logout"),
    path("ec-dashboard/", ec_dashboard, name="ec_dashboard"),

    path("ec-recommend/<int:candidate_id>/", ec_recommend, name="ec_recommend"),
    path("ec-reject/<int:candidate_id>/", ec_reject, name="ec_reject"),
]
