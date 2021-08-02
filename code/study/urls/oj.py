from django.conf.urls import url

from ..views.oj import StudyAPI, StudyListAPI

urlpatterns = [
    url(r"^study/?$", StudyAPI.as_view(), name="study_api"),
    url(r"^studies/?$", StudyListAPI.as_view(), name="study_list_api")
]
