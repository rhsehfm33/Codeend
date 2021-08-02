import json
import copy

from copy import deepcopy

from utils.api.tests import APITestCase
from .models import Study, StudyTag

SETUP_STUDY_DATA = {"title": "setup", "content": "<p>setup's content</p>", "subject": "algorithm", "purpose": "enhance algorithm",
                    "schedule": "once a week", "curriculum": "c++ algorithm", "max_students": 5, "reason": "I want to earn money",
                    "notice": "You need a computer", "tags": ["algorithm", "c++"], "status": "Recruited", "price": 500000000}


TEST_STUDY_DATA = {"title": "test", "content": "<p>test's content</p>", "subject": "algorithm", "purpose": "enhance algorithm",
                    "schedule": "once a week", "curriculum": "c++ algorithm", "max_students": 5, "reason": "I want to earn money",
                    "notice": "You need a computer", "tags": ["algorithm", "c++"], "status": "Recruiting", "price": 500000000}

STUDY_URL = "/api/study"
STUDIES_URL = "/api/studies"

class StudyAPITest(APITestCase):
    def setUp(self):
        data = copy.deepcopy(SETUP_STUDY_DATA)
        self.user = self.create_user("test_user_username", "test_user_password")
        tags = data.pop("tags")
        self.study_data = Study.objects.create(created_by=self.user, **data)

        for tag in tags:
            try:
                tag = StudyTag.objects.get(name=tag)
            except StudyTag.DoesNotExist:
                tag = StudyTag.objects.create(name=tag)
            self.study_data.tags.add(tag)

        self.url = self.reverse("study_api")

    def test_create_study(self):
        resp = self.client.post(self.url, TEST_STUDY_DATA)
        self.assertSuccess(resp)

    def test_create_study_validate_status(self):
        wrong_study_data = copy.deepcopy(TEST_STUDY_DATA)
        wrong_study_data["status"] = "wrong status"
        resp = self.client.post(self.url, wrong_study_data)
        self.assertFailed(resp)

    def test_get_study_teacher_true(self):
        resp = self.client.get(self.url + "?id=" + str(self.study_data.id) + "&teacher=True")
        self.assertContains(resp, "\"students\"")

    def test_get_study_teacher_false(self):
        resp = self.client.get(self.url + "?id=" + str(self.study_data.id) + "&teacher=False")
        self.assertFalse(self.assertContains(resp, "\"students\""))
    
    def test_get_study_validate_teacher(self):
        resp = self.client.get(self.url + "?id=" + str(self.study_data.id))
        self.assertFailed(resp)

    def test_delete_study(self):
        resp = self.client.delete(self.url + "?id=" + str(self.study_data.id))
        self.assertSuccess(resp)

    def test_update_study(self):
        SETUP_STUDY_DATA["id"] = self.study_data.id
        resp = self.client.put(self.url, SETUP_STUDY_DATA)
        self.assertSuccess(resp)

class StudyListAPITest(APITestCase):
    def setUp(self):
        data = copy.deepcopy(SETUP_STUDY_DATA)
        self.user = self.create_user("test_user_username", "test_user_password")
        tags = data.pop("tags")
        self.study_data = Study.objects.create(created_by=self.user, **data)

        for tag in tags:
            try:
                tag = StudyTag.objects.get(name=tag)
            except StudyTag.DoesNotExist:
                tag = StudyTag.objects.create(name=tag)
            self.study_data.tags.add(tag)

        self.url = self.reverse("study_list_api")
        
    def test_get_studies_search_keyword_title(self):
        for i in range(0, 3):
            self.client.post(STUDY_URL, TEST_STUDY_DATA)
        resp = self.client.get(self.url + "?limit=10&offset=10&keyword=test")
        self.assertContains(resp, "\"total\": 3")

    def test_get_studies_search_keyword_tag(self):
        for i in range(0, 3):
            self.client.post(STUDY_URL, TEST_STUDY_DATA)
        resp = self.client.get(self.url + "?limit=10&offset=10&keyword=test&tag=algorithm")
        self.assertContains(resp, "\"total\": 3")

    def test_get_studies_search_keyword_status(self):
        for i in range(0, 3):
            self.client.post(STUDY_URL, TEST_STUDY_DATA)
        resp = self.client.get(self.url + "?limit=10&offset=10&keyword=test&tag=algorithm&status=Recruiting")
        self.assertContains(resp, "\"total\": 3")

    def test_get_studies_check_total_students(self):
        self.study_data.students.add(self.user)
        resp = self.client.get(self.url + "?limit=10&offset=0&keyword=setup")
        self.assertContains(resp, "\"total_students\": 1")    