from django.conf.urls import url

from ..views.oj import StudyTagAPI, StudyAPI, StudyListAPI

urlpatterns = [
    url(r"^study/tags/?$", StudyTagAPI.as_view(), name="study_tag_list_api"),
    url(r"^study/?$", StudyAPI.as_view(), name="study_api"),
    url(r"^studies/?$", StudyListAPI.as_view(), name="study_list_api")
]
