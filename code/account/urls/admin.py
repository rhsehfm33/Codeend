from django.conf.urls import url

from ..views.admin import UserAdminLoginAPI, UserAdminAPI, GenerateUserAPI

urlpatterns = [
    url(r"^admin_login$", UserAdminLoginAPI.as_view(), name="user_admin_login_api"),
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
]
