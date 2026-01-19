from django.urls import path
from .views import (
    nomination_check, nomination_submit,
    ballot, cast_vote,
    my_result,
    results_page, results_data,
    voter_area_check
)

urlpatterns = [
    path("nomination-check/", nomination_check, name="nomination_check"),
    path("nomination-submit/", nomination_submit, name="nomination_submit"),

    path("ballot/", ballot, name="ballot"),
    path("cast-vote/<int:candidate_id>/", cast_vote, name="cast_vote"),

    path("my-result/", my_result, name="my_result"),

    path("results/", results_page, name="results"),
    path("results-data/", results_data, name="results_data"),

    path("voter-area-check/", voter_area_check, name="voter_area_check"),
]
