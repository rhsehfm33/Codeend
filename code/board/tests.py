import json

from copy import deepcopy

from utils.api.tests import APITestCase
from .models import Board, Comment

SETUP_BOARD_DATA = {"title": "setup", "category": "Announcement", "content": "<p>setup</p>"}
SETUP_COMMENT_DATA = {"content": "setup"}

TEST_BOARD_DATA = {"title": "test", "category": "Free", "content": "<p>test</p>"}

class BardAPITest(APITestCase):
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

    def test_get_board(self):
        resp = self.client.get(self.url + "?id=" + str(self.board_data.id))
        self.assertSuccess(resp)
        
        # Use this when you want to know the json structrue
        # print(json.dumps(resp.data))
