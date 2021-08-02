from django.db import models

from account.models import User
from utils.models import RichTextField
from utils.constants import Choices

class StudyStatusCategory(Choices):
    Recruiting = "Recruiting"
    Recruited = "Recruited"

class StudyTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "study_tag"

class Study(models.Model):
    title = models.TextField()
    content = RichTextField()
    subject = models.TextField()
    purpose = models.TextField()
    schedule = models.TextField()
    curriculum = models.TextField()
    max_students = models.IntegerField()
    reason = models.TextField()
    notice = models.TextField()
    tags = models.ManyToManyField(StudyTag)
    status = models.TextField()
    price = models.BigIntegerField()
    students = models.ManyToManyField(User, related_name="learning")
    created_by = models.ForeignKey(User, related_name="teaching", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "study"
        ordering = ("-create_time",)
    