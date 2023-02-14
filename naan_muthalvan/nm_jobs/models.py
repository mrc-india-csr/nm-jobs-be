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
    phone_no = models.BigIntegerField(unique= True)
    email = models.EmailField(max_length = 200, unique=True)

    def __str__(self) -> str:
        return str(self.job_id)

class JobDetails(models.Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE, primary_key=True)
    date_range = models.CharField(max_length = 100)
    currency = models.CharField(max_length = 100)
    max_salary = models.BigIntegerField()
    min_salary = models.BigIntegerField()
    experience = models.IntegerField()

    def __str__(self) -> str:
        return str(self.job_id)

class Perks(models.Model):
    perk_id = models.IntegerField(primary_key= True)
    perks = models.CharField(max_length= 300)

    def __str__(self) -> str:
        return str(self.perk_id)

class AddOns(models.Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE, primary_key=True)
    perk_id = models.ForeignKey(Perks, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.job_id)

class Company(models.Model):
    company_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 300)
    
    def __str__(self) -> str:
        return str(self.company_id)

class CompanySector(models.Model):
    sector_id = models.IntegerField(primary_key = True)
    company_id = models.ForeignKey(Company, on_delete = models.CASCADE)

class Sector(models.Model):
    sector_id = models.OneToOneField(CompanySector, on_delete= models.CASCADE, primary_key=True)
    industry = models.CharField(max_length = 100)
    department = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return str(self.sector_id)

class Internship(models.Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE, primary_key=True)
    stipend = models.CharField(max_length = 20)
    date_range = models.CharField(max_length = 100)
    duration = models.IntegerField()
    currency = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return str(self.job_id)

class Status(models.Model):
    job_id = models.OneToOneField(Jobs, on_delete = models.CASCADE, primary_key= True)
    date_posted = models.DateTimeField()
    to_date = models.DateTimeField()
    application_received = models.IntegerField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.job_id)

class Spoc(models.Model):
    company_id = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key= True)
    name = models.CharField(max_length = 100)
    phone_no = models.BigIntegerField(unique=True)
    email = models.EmailField(max_length = 200, unique=True)
    
    def __str__(self) -> str:
        return str(self.company_id)

# class files(models.Model):
#     job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=200)
#     upload_file = models.FileField("jobs/"+str(job_id)+"/"+file_name)
    
#     def __str__(self) -> str:
#         return str(self.job_id)

# class CompanyDetails(models.Model):
#     company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=200)
#     image = models.ImageField("company/"+str(company_id)+"/"+file_name)

#     def __str__(self) -> str:
#         return str(self.company_id)