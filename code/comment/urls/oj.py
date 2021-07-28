from django.conf.urls import url

from ..views.oj import CommentAPI

urlpatterns = [
    url(r"^comment/?$", CommentAPI.as_view(), name="comment_api")
]
