from calendar import c
from dataclasses import is_dataclass
from lib2to3.pgen2 import driver
from multiprocessing import context
from operator import inv
import re
import tempfile
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import compare_documents
import logging

import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import PyPDF2
from difflib import SequenceMatcher

from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from pytz import timezone

from django.http import JsonResponse

import requests 
from django.db.models import Q

from .models import *
from .forms import *
from .utils import *


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from dotenv import load_dotenv
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models.functions import ExtractYear

load_dotenv()

import os
from openai import OpenAI

client = OpenAI(
  api_key='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'
)

@login_required(login_url='login')
def Home(request):
    if request.user.is_superuser:
        return redirect('admin_page')
    return render(request, "archive/home.html")

@login_required(login_url='login')
def approved_thesis_list(request):
    five_years_ago = now() - timedelta(days=5 * 365)

    # Initial QuerySet: Only approved theses within the last 5 years
    thesis = ThesisUpload.objects.filter(status='Approved', date__gte=five_years_ago)

    # Get distinct categories and years for filtering
    categories = ThesisUpload.objects.values("category").distinct()
    years = ThesisUpload.objects.annotate(year=ExtractYear('date')).values("year").distinct().order_by("year")

    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        category = request.POST.get('category', '').strip()

        # Apply filters based on user input
        if search:
            thesis = thesis.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(date_finished__icontains=search)
            )
        if category:
            thesis = thesis.filter(category=category)

    context = {'thesis': thesis, 'category': categories, 'years': years}
    return render(request, 'archive/thesis_archive.html', context)

@login_required(login_url='login')
def ThesisUploadPage(request):
    thesis = ThesisUpload.objects.all()
    categories = ThesisUpload.objects.values_list("category", flat=True).distinct()
    form = ThesisForm()
    
    if request.method == 'POST':
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.user = request.user
            thesis.save()
            return redirect('home')

    context = {'thesis': thesis, 'form': form, 'categories': categories}
    return render(request, 'archive/upload_thesis.html', context)

@login_required(login_url='login')
def MyUploads(request):
    thesis = ThesisUpload.objects.filter(user=request.user)
    categories = ThesisUpload.objects.values("category").distinct()
    if request.method == 'POST':
        search = request.POST.get('search')
        category = request.POST.get('category')
        if search and category:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search)).filter(user=request.user)
            thesis = thesis.filter(category=category)
            thesis = thesis.filter(status='Approved')
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search)).filter(user=request.user)
        elif category:
            thesis = ThesisUpload.objects.filter(category=category).filter(user=request.user)
            thesis = thesis.filter(status='Approved')
        else:
            thesis = ThesisUpload.objects.filter(user=request.user)
            thesis = thesis.filter(status='Approved')
    context = {'thesis': thesis, 'category': categories}
    return render(request, 'archive/user_uploads.html', context)

@login_required(login_url='login')
def ProfilePage(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print(form.errors)
        if form.is_valid():
            form.save(commit=False).user = request.user
            form.save()
            return redirect('profile')
    context = {'form': form, 'profile': profile}
    return render(request, 'archive/profile.html', context)

ROMAN_TO_INT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}
WORDS_TO_INT = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5}

def download_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name
    return None

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def extract_chapters(text):
    chapter_pattern = r'(CHAPTER\s+\b(\d+|ONE|TWO|THREE|FOUR|FIVE|I|II|III|IV|V)\b)'
    chapters = re.split(chapter_pattern, text, flags=re.IGNORECASE)

    chapter_data = {}
    current_chapter = None

    for i in range(len(chapters)):
        part = chapters[i].strip()
        if i % 3 == 1:
            chapter_number = part.upper().replace("CHAPTER ", "").strip()

            if chapter_number in ROMAN_TO_INT:
                chapter_number = ROMAN_TO_INT[chapter_number]
            elif chapter_number in WORDS_TO_INT:
                chapter_number = WORDS_TO_INT[chapter_number]
            elif chapter_number.isdigit():
                chapter_number = int(chapter_number)
            else:
                continue

            current_chapter = f"CHAPTER {chapter_number}"
            chapter_data[current_chapter] = ""
        elif current_chapter:
            chapter_data[current_chapter] += part + " "

    return chapter_data

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding)

def compare_text(text1, text2):
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return round(similarity * 100, 2)

def generate_ai_comparison(text1, text2, chapter):
    max_length = 1000

    text1 = text1[:max_length]
    text2 = text2[:max_length]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are an AI that compares research chapters."},
            {"role": "user", "content": f"Compare the key points and topics of {chapter} in these two capstone project papers:\n\nDocument 1:\n{text1}\n\nDocument 2:\n{text2}\n\nProvide a concise comparison."}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def CompareResearch(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("thesis_ids")
        if len(selected_ids) != 2:
            messages.error(request, "Please select exactly two thesis documents.")
            return redirect("compare")

        thesis1 = get_object_or_404(ThesisUpload, id=selected_ids[0])
        thesis2 = get_object_or_404(ThesisUpload, id=selected_ids[1])

        if not thesis1.file_thesis or not thesis2.file_thesis:
            messages.error(request, "One or both files are missing.")
            return redirect("compare")

        # Convert relative URL to absolute URL
        thesis1_url = request.build_absolute_uri(thesis1.file_thesis.url)
        thesis2_url = request.build_absolute_uri(thesis2.file_thesis.url)

        thesis1_path = download_file(thesis1_url)
        thesis2_path = download_file(thesis2_url)

        if not thesis1_path or not thesis2_path:
            messages.error(request, "Error downloading files.")
            return redirect("compare")

        thesis1_text = extract_text_from_pdf(thesis1_path)
        thesis2_text = extract_text_from_pdf(thesis2_path)

        thesis1_chapters = extract_chapters(thesis1_text)
        thesis2_chapters = extract_chapters(thesis2_text)

        comparison_results = {}

        for i in range(1, 6):
            chapter = f"CHAPTER {i}"
            if chapter in thesis1_chapters and chapter in thesis2_chapters:
                summary1 = thesis1_chapters[chapter][:300] 
                summary2 = thesis2_chapters[chapter][:300]

                ai_comparison = generate_ai_comparison(thesis1_chapters[chapter], thesis2_chapters[chapter], chapter)

                comparison_results[chapter] = {
                    "thesis1_summary": summary1,
                    "thesis2_summary": summary2,
                    "ai_comparison": ai_comparison
                }

        return render(request, "archive/compare_result.html", {
            "thesis1": thesis1,
            "thesis2": thesis2,
            "comparison_results": comparison_results,
        })
    
    thesis = ThesisUpload.objects.filter(status="Approved")
    categories = ThesisUpload.objects.values("category").distinct()
    context = {'thesis': thesis, 'category': categories}
    return render(request, "archive/compare.html", context)

def TitleGenerator(request):
    titles_list = []
    category = ""

    if request.method == 'POST':
        category = request.POST.get('title')
        benificiary = request.POST.get('benificiaries')
        generate_number = request.POST.get('generate', 10)

        try:
            generate_number = int(generate_number)
            generate_number = max(5, min(generate_number, 20))  # Enforces range 5-20
        except ValueError:
            generate_number = 10  # Default to 10 if invalid input

        prompt = f"Generate {generate_number} capstone project titles that involve developing a system, software, or device in the category of {category} for {benificiary}. Ensure that at least 30% of the titles introduce creative variations."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Capstone titles with some inconsistency"},
                {"role": "user", "content": prompt}
            ]
        )

        data_response = response.choices[0].message.content
        titles_list = re.split(r'\d+\.\s', data_response)
        titles_list = [title.strip() for title in titles_list if title.strip()]

    context = {'ai_return': titles_list, 'category': category}
    return render(request, 'archive/title_generator.html', context)


# Admin Page
@login_required(login_url='login')
def AdminPage(request):
    if not request.user.is_superuser:
        return redirect('home')
    thesis = ThesisUpload.objects.all()
    thesis = thesis.filter(status='Approved')
    categories = ThesisUpload.objects.values("category").distinct()
    print(categories)
    if request.method == 'POST':
        search = request.POST.get('search')
        category = request.POST.get('category')
        print(search, category)
        if search and category:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            print(thesis)
            thesis = thesis.filter(category=category)
            thesis = thesis.filter(status='Approved')
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            thesis = thesis.filter(status='Approved')
        elif category:
            thesis = ThesisUpload.objects.filter(category=category)
            thesis = thesis.filter(status='Approved')
        else:
            thesis = ThesisUpload.objects.all()
            thesis = thesis.filter(status='Approved')
    context = {'thesis': thesis, 'category': categories}
    return render(request, 'archive/admin_archive/approve_archive.html', context)

@login_required(login_url='login')
def PendingUploads(request):
    thesis = ThesisUpload.objects.filter(status='Pending')
    categories = ThesisUpload.objects.values("category").distinct()
    print(categories)
    if request.method == 'POST':
        search = request.POST.get('search')
        category = request.POST.get('category')
        print(search, category)
        if search and category:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            print(thesis)
            thesis = thesis.filter(category=category)
            thesis = thesis.filter(status='Pending')
        elif search:
            thesis = ThesisUpload.objects.filter(Q(title__icontains=search) |
            Q(abstract__icontains=search) | 
            Q(date_finished__icontains=search))
            thesis = thesis.filter(status='Pending')
        elif category:
            thesis = ThesisUpload.objects.filter(category=category)
            thesis = thesis.filter(status='Pending')
        else:
            thesis = ThesisUpload.objects.filter(status='Pending')
    context = {'thesis': thesis, 'category': categories}
    return render(request, 'archive/admin_archive/thesis_archive.html', context)

@login_required(login_url='login')
def ApprovedUploads(request, pk):
    thesis = ThesisUpload.objects.get(id=pk)
    thesis.status = 'Approved'
    thesis.save()
    return redirect('pending_uploads')


logger = logging.getLogger(__name__)

def Register(request):
    form = CreateUserForm()
    host = request.get_host()
    random_id = create_rand_id()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print("Form Data:", request.POST)
        print("Form Errors:", form.errors)
        logger.debug(f"Form Data: {request.POST}")
        logger.debug(f"Form Errors: {form.errors}")

        if form.is_valid():
            user = form.save()
            messages.success(request, "Please verify your Email " + user.email)
            Profile.objects.create(user=user, email=user.email, token=random_id)
            send_email_token(user.email, random_id, host)
            return redirect('login')
            
    context = {'form': form}
    return render(request, 'archive/register.html', context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_page')
                userDetail = Profile.objects.filter(user=user)
                if userDetail:
                    if userDetail[0].is_verified == True:
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.info(request, 'Please verify your email address')
                        return redirect('login')
            else:
                messages.info(request, 'Username or Password is incorrect') 
    return render(request, 'archive/login.html')

def Logout(request):
    logout(request)
    return redirect('login')


def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'archive/change_password.html', {
        'form': form
    })

def Terms(request):
    return render(request, 'archive/termsandconditions.html')

def Verify(request, token):
    profile = Profile.objects.get(token=token)
    if profile:
        profile.is_verified = True
        profile.save()
        messages.success(request, 'Email verified')
        return redirect('login')
    else:
        messages.error(request, 'Email not verified')
        return redirect('login')
