from django.db import models
from .utils.models_abstract import Model

# Create your models here.
class Jobs(Model):
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
    email = models.EmailField(max_length = 200)

    def __str__(self) -> str:
        return "jobId: " + str(self.id)

class JobDetails(Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE)
    date_range = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    max_salary = models.BigIntegerField()
    min_salary = models.BigIntegerField()
    experience = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return "fullTimeId: " + str(self.job_id)
    
class Perks(Model):
    # perk_id = models.UUIDField()
    perk = models.CharField(max_length= 300, unique=True)

    def __str__(self) -> str:
        return "perkId: "+ str(self.id)

class AddOns(Model):
    job_id = models.ForeignKey(Jobs, on_delete = models.CASCADE)
    perk_id = models.ForeignKey(Perks, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.job_id)

class Internship(Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE)
    stipend = models.CharField(max_length = 20)
    date_range = models.CharField(max_length = 100)
    duration = models.IntegerField()
    currency = models.CharField(max_length = 100)
    is_pre_placement_offer = models.BooleanField()

    def __str__(self) -> str:
        return "internId: "+str(self.job_id)

class Company(Model):
    name = models.CharField(max_length = 100, unique=True)
    description = models.CharField(max_length = 400)
    city = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200)
    
    def __str__(self) -> str:
        return "companyId: "+str(self.id)

class Sector(Model):
    # sector_id = models.UUIDField(primary_key = True)
    industry = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return "sectorId: "+str(self.id)

class CompanySector(Model):
    sector_id = models.ForeignKey(Sector, on_delete= models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return "companySectorId: "+str(self.id)

class Status(Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE)
    date_posted = models.DateTimeField()
    to_date = models.DateTimeField()
    application_received = models.IntegerField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "jobId: "+str(self.job_id)

class Spoc(Model):
    company_id = models.OneToOneField(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    phone_no = models.BigIntegerField()
    email = models.EmailField(max_length = 200)
    
    def __str__(self) -> str:
        return "companyId: "+str(self.company_id)

class Files(Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    upload_file = models.BinaryField()
    
    def __str__(self) -> str:
        return str(self.job_id)

class CompanyDetails(Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    image = models.BinaryField()

    def __str__(self) -> str:
        return str(self.company_id)

class ImageTest(Model):
    name = models.CharField(max_length=100)
    image = models.BinaryField()

    def __str__(self) -> str:
        return self.name