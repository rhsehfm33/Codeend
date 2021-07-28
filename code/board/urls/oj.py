from django.conf.urls import url

from ..views.oj import BoardAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="board_api")
    # url(r"^comment/?$", CommentAPI.as_view(), name="comment_api")
]
