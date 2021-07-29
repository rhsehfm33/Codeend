import json
import copy

from copy import deepcopy

from utils.api.tests import APITestCase
from .models import Board
from comment.models import Comment

SETUP_BOARD_DATA = {"title": "setup", "category": "Announcement", "content": "<p>setup</p>"}
SETUP_COMMENT_DATA = {"content": "setup"}


TEST_BOARD_DATA = {"title": "test", "category": "Free", "content": "<p>test</p>"}

class BoardAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_user("test_user_username", "test_user_password")
        self.board_data = Board.objects.create(created_by=self.user, **SETUP_BOARD_DATA)
        self.comment_data = Comment.objects.create(created_by=self.user, board=self.board_data, **SETUP_COMMENT_DATA)
        self.url = self.reverse("board_api")

    def test_create_board(self):
        resp = self.client.post(self.url, TEST_BOARD_DATA)
        self.assertSuccess(resp)

        # Use this when you want to know the json structrue
        # print(json.dumps(resp.data))

    def test_create_board_validation(self):
        wrong_board_data = copy.deepcopy(TEST_BOARD_DATA)
        del wrong_board_data["title"]
        resp = self.client.post(self.url, wrong_board_data)
        self.assertDictEqual(resp.data, {"error": "invalid-title", "data": "title: This field is required."})

    def test_get_board(self):
        resp = self.client.get(self.url + "?id=" + str(self.board_data.id))
        self.assertSuccess(resp)

        # Use this when you want to know the json structrue
        # print(json.dumps(resp.data))

    def test_delete_board(self):
        resp = self.client.delete(self.url + "?id=" + str(self.board_data.id))
        self.assertSuccess(resp)

    def test_update_board(self):
        id = self.board_data.id
        TEST_BOARD_DATA["id"] = id
        resp = self.client.put(self.url, TEST_BOARD_DATA)
        self.assertSuccess(resp)

    def test_get_boards_pagination(self):
        for i in range(1, 3):
            self.client.post(self.url, TEST_BOARD_DATA)
        resp = self.client.get(self.url + "s?limit=10&offset=0")
        
        self.assertContains(resp, "\"total\": 3")

    def test_get_boards_keyword_search(self):
        for i in range(1, 20):
            self.client.post(self.url, TEST_BOARD_DATA)
        resp = self.client.get(self.url + "s?limit=10&offset=10&keyword=test")
        print(json.dumps(resp.data))
        self.assertContains(resp, "\"total\": 19")