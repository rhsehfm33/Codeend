import json
import copy

from copy import deepcopy

from utils.api.tests import APITestCase
from .models import Board
from comment.models import Comment

SETUP_BOARD_DATA = {"title": "setup", "category": "Announcement", "content": "<p>setup</p>"}
SETUP_COMMENT_DATA = {"content": "setup"}

TEST_BOARD_DATA = {"title": "test", "category": "Free", "content": "<p>test</p>"}
TEST_COMMENT_DATA = {"board_id": "1", "content": "setup"}

class CommentAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_user("test_user_username", "test_user_password")
        self.board_data = Board.objects.create(created_by=self.user, **SETUP_BOARD_DATA)
        self.comment_data = Comment.objects.create(created_by=self.user, board=self.board_data, **SETUP_COMMENT_DATA)
        self.url = self.reverse("comment_api")
        
    def test_create_comment(self):
        resp = self.client.post(self.url, TEST_COMMENT_DATA)
        self.assertSuccess(resp)

    def test_create_comment_validation(self):
        wrong_comment_data = copy.deepcopy(TEST_COMMENT_DATA)
        del wrong_comment_data["content"]
        resp = self.client.post(self.url, wrong_comment_data)
        self.assertDictEqual(resp.data, {"error": "invalid-content", "data": "content: This field is required."})

        wrong_comment_data = copy.deepcopy(TEST_COMMENT_DATA)
        del wrong_comment_data["board_id"]
        resp = self.client.post(self.url, wrong_comment_data)
        self.assertDictEqual(resp.data, {"error": "invalid-board_id", "data": "board_id: This field is required."})

    def test_update_comment(self):
        update_comment_data = {"id": self.comment_data.id, "content": "updated"}
        resp = self.client.put(self.url, update_comment_data)
        self.assertContains(resp, "\"content\": \"updated\"")

        # Use this when you want to know the json structrue
        # print(json.dumps(resp.data))

    def test_delete_comment(self):
        resp = self.client.delete(self.url + "?id=" + str(self.comment_data.id))
        self.assertSuccess(resp)