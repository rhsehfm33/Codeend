from django.db import models

class Company(models.Model):
    name = models.TextField()
    number_of_workers = models.IntegerField(default=0)
    salary_man = models.IntegerField(default=0)

    class Mets:
        db_table = "company"