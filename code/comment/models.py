import board
from django.db import models

from account.models import User
from utils.models import RichTextField
from utils.constants import Choices
from board.models import Board

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    board = models.ForeignKey(Board, related_name="comment", on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "comment"