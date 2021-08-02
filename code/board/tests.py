import json
import copy

from copy import deepcopy

from utils.api.tests import APITestCase
from .models import Board
from comment.models import Comment
from problem.tests import ProblemCreateTestBase, DEFAULT_PROBLEM_DATA

SETUP_BOARD_DATA = {"title": "setup", "category": "Question", "content": "<p>setup</p>"}
SETUP_COMMENT_DATA = {"content": "setup"}

TEST_BOARD_DATA = {"title": "test", "category": "Free", "content": "<p>test</p>"}

class BoardAPITest(APITestCase):
    def setUp(self):
        self.problem = ProblemCreateTestBase.add_problem(DEFAULT_PROBLEM_DATA, self.create_super_admin())
        self.user = self.create_user("test_user_username", "test_user_password")
        self.board_data = Board.objects.create(created_by=self.user, problem=self.problem, **SETUP_BOARD_DATA)
        self.comment_data = Comment.objects.create(created_by=self.user, board=self.board_data, **SETUP_COMMENT_DATA)
        self.url = self.reverse("board_api")
        TEST_BOARD_DATA["problem_id"] = self.problem._id

    def test_create_board(self):
        resp = self.client.post(self.url, TEST_BOARD_DATA)
        self.assertSuccess(resp)
        
        # Use this when you want to know the json structrue
        # print(json.dumps(resp.data))

    def test_create_board_validate_title(self):
        wrong_board_data = copy.deepcopy(TEST_BOARD_DATA)
        del wrong_board_data["title"]
        resp = self.client.post(self.url, wrong_board_data)
        self.assertFailed(resp)

    def test_get_board(self):
        resp = self.client.get(self.url + "?id=" + str(self.board_data.id))
        self.assertSuccess(resp)

    def test_delete_board(self):
        resp = self.client.delete(self.url + "?id=" + str(self.board_data.id))
        self.assertSuccess(resp)

    def test_update_board(self):
        TEST_BOARD_DATA["id"] = self.board_data.id
        resp = self.client.put(self.url, TEST_BOARD_DATA)
        self.assertSuccess(resp)

class BoardListAPITest(APITestCase):
    def setUp(self):
        self.problem = ProblemCreateTestBase.add_problem(DEFAULT_PROBLEM_DATA, self.create_super_admin())
        self.user = self.create_user("test_user_username", "test_user_password")
        self.board_data = Board.objects.create(created_by=self.user, problem=self.problem, **SETUP_BOARD_DATA)
        self.comment_data = Comment.objects.create(created_by=self.user, board=self.board_data, **SETUP_COMMENT_DATA)
        self.url = self.reverse("board_api")
        TEST_BOARD_DATA["problem_id"] = self.problem._id

    def test_get_boards_pagination(self):
        for i in range(1, 3):
            self.client.post(self.url, TEST_BOARD_DATA)
        resp = self.client.get(self.url + "s?limit=10&offset=0")
        
        self.assertContains(resp, "\"total\": 3")

    def test_get_boards_search_keyword(self):
        for i in range(1, 20):
            self.client.post(self.url, TEST_BOARD_DATA)
        resp = self.client.get(self.url + "s?limit=10&offset=10&keyword=test")
        self.assertContains(resp, "\"total\": 19")

    def test_get_boards_search_category(self):
        for i in range(1, 6):
            self.client.post(self.url, TEST_BOARD_DATA)
            self.client.post(self.url, SETUP_BOARD_DATA)
        resp = self.client.get(self.url + "s?limit=10&offset=0&category=Free")
        self.assertContains(resp, "\"total\": 5")

    def test_get_boards_check_total_comments(self):
        resp = self.client.get(self.url + "s?limit=10&offset=0&category=" + self.board_data.category)
        self.assertContains(resp, "\"total_comments\": 1")