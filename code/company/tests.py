from copy import deepcopy
from unittest import mock

from company.models import Company
from utils.api.tests import APITestCase

DEFAULT_COMPANY_DATA1 = {"name": "codeend", "number_of_workers": 1000, "salary_man": 2800}
DEFAULT_COMPANY_DATA2 = {"name": "qingdao", "number_of_workers": 10, "salary_man": 2800}


# Create your tests here.
class CompanyAPITest(APITestCase):
    def setUp(self):
        self.data = deepcopy(DEFAULT_COMPANY_DATA1)
        self.url = self.reverse("company_api")

    def test_create_company(self):
        resp = self.client.post(self.url, data=self.data)
        self.assertSuccess(resp)

    def test_get_company(self):
        Company.objects.create(name=self.data["name"],
                                number_of_workers=self.data["number_of_workers"],
                                salary_man=self.data["salary_man"])

        self.url += "?name=" + self.data["name"]
        resp = self.client.get(self.url)
        self.assertSuccess(resp)