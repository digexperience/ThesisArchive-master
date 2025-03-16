from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.models import Group



admin.site.unregister(Group)
admin.site.register(ThesisUpload)
admin.site.register(Profile)

admin.site.site_header = "Admin Portal"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Admin Portal"