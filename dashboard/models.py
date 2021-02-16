from django.conf import settings
from django.db import models

class Zip(models.Model):
    """ 
    Model representing the zip code
    """
    zip_zipcode = models.CharField(max_length=10)
    zip_city = models.CharField(max_length=200)
    zip_state = models.CharField(max_length=30)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.zip_zipcode


class Company(models.Model):
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name

class Client(models.Model):
    client_first_name = models.CharField(max_length=200)
    client_last_name = models.CharField(max_length=200)
    client_email = models.CharField(max_length=200)
    
class Skill(models.Model):
    skill_name = models.CharField(max_length=200)

    def __str__(self):
        return self.skill_name

class Query(models.Model):
    query_content = models.CharField(max_length=200)
    query_timestamp = models.DateTimeField()
    query_location = models.CharField(max_length=200)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)

class Job(models.Model):
    job_title = models.CharField(max_length=200)
    job_summary = models.TextField()
    job_salary = models.DecimalField(max_digits=11, decimal_places=2)
    job_link = models.TextField()
    job_date_posted = models.IntegerField()
    job_description = models.TextField()
    
    zip_id = models.ForeignKey(Zip, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete= models.CASCADE)

    def __str__(self):
        return self.job_title

class Query_Job(models.Model):
    job_id = models.ForeignKey(Job, on_delete= models.CASCADE)
    query_id = models.ForeignKey(Query, on_delete= models.CASCADE)

class Query_Skill(models.Model):
    skill_id = models.ForeignKey(Skill, on_delete= models.CASCADE)
    query_id = models.ForeignKey(Query, on_delete= models.CASCADE)

