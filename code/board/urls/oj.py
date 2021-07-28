from django.conf.urls import url

from ..views.oj import BoardAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="board_api")
]
