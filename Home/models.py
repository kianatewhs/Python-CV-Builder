from django.db import models

# Create your models here.

class DemoModel(models.Model):
    name = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    career_summary = models.TextField(max_length=1000,null=True, blank=True)
    skills = models.TextField(max_length=1000,null=True, blank=True)
    work_experience = models.TextField(max_length=1000,null=True, blank=True)
    eductional_summary = models.TextField(max_length=1000,null=True, blank=True)
    certification = models.TextField(max_length=1000,null=True, blank=True)
    personal_details = models.TextField(max_length=1000,null=True, blank=True)
    declaration = models.TextField(max_length=1000,null=True, blank=True)

# id - DemoAdmin
# password - password123 
