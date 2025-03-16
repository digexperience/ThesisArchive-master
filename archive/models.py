from email.policy import default
from math import e
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.db import models

def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    token = models.CharField(
        max_length=100, null=True, blank=True, editable=False
    )
    is_verified = models.BooleanField(default=False)    


    def __str__(self):
        return f"{self.first_name}"

    def date_pretty(self):
        return self.date.strftime('%B %Y')

class ThesisUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    author1 = models.CharField(max_length=200, null=True, blank=True)
    author2 = models.CharField(max_length=200, null=True, blank=True)
    author3 = models.CharField(max_length=200, null=True, blank=True)
    author4 = models.CharField(max_length=200, null=True, blank=True)
    abstract = models.TextField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    date_finished = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file_thesis = models.FileField(upload_to='thesis_files/', null=True, blank=True)
    thesis_cover = models.ImageField(upload_to='thesis_covers/', null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True, default='Pending')
    ethical_review = models.FileField(upload_to='certificates/', blank=True, null=True)
    statistician_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    grammarian_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
    
    def date_pretty(self):
        return self.date.strftime('%B %Y')

    def formatted_date_finished(self):
        """
        Converts 'YYYY-MM' into 'Month Year', e.g., '2002-01' -> 'January 2002'
        """
        if self.date_finished:
            try:
                date_object = datetime.strptime(self.date_finished, "%Y-%m")
                return date_object.strftime("%B %Y")
            except ValueError:
                return "Invalid Date Format"
        return "No Date Provided"