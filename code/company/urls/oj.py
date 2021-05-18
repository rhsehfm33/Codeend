from django.conf.urls import url

from ..views.oj import CompanyAPI

urlpatterns = [
    url(r"^company/?$", CompanyAPI.as_view(), name="company_api"),
]
