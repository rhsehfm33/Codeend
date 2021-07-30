import board
from django.db import models

from account.models import User
from problem.models import Problem
from utils.models import RichTextField
from utils.constants import Choices

class BoardCategory(Choices):
    Free = "Free"
    Question = "Question"

class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    title = models.TextField()
    category = models.TextField()
    content = RichTextField()
    views = models.BigIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "board"
        ordering = ("-create_time",)
    