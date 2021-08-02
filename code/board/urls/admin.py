from django.conf.urls import url

from ..views.admin import BoardAPI, BoardListAPI

urlpatterns = [
    url(r"^board/?$", BoardAPI.as_view(), name="admin_board_api"),
    url(r"^boards/?$", BoardListAPI.as_view(), name="admin_board_list_api")
]
