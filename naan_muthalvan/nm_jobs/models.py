from django.db import models

# Create your models here.
class Jobs(models.Model):
    job_id = models.IntegerField(primary_key=True)
    job_type = models.CharField(max_length = 100)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    category = models.CharField(max_length = 100)
    link = models.CharField(max_length = 500)
    number_of_openings = models.IntegerField()
    work_type = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    posted_by = models.CharField(max_length = 100)
    phone_no = models.BigIntegerField()
    email = models.CharField(max_length = 200)

    def __str__(self) -> str:
        return str(self.job_id)

class JobDetails(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    date_range = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    max_salary = models.BigIntegerField()
    min_salary = models.BigIntegerField()
    experience = models.IntegerField()

    def __str__(self) -> str:
        return str(self.job_id)

class AddOns(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    perk_id = models.IntegerField()

    def __str__(self) -> str:
        return str(self.perk_id)


class Perks(models.Model):
    perk_id = models.ForeignKey(AddOns, on_delete=models.CASCADE)
    perks = models.CharField(max_length= 300)

    def __str__(self) -> str:
        return str(self.perk_id)