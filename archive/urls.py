from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("thesis_upload/", views.ThesisUploadPage, name="thesis_upload"),
    path("myuploads/", views.MyUploads, name="myuploads"),
    path("profile/", views.ProfilePage, name="profile"),
    path("compare/", views.CompareResearch, name="compare"),
    path("title-generator/", views.TitleGenerator, name="title-generator"),
    path('approved-thesis/', views.approved_thesis_list, name='approved_thesis_list'),
    
    # Admin
    path("admin_page/", views.AdminPage, name="admin_page"),
    path("pending_uploads/", views.PendingUploads, name="pending_uploads"),
    path("approved_uploads/<str:pk>", views.ApprovedUploads, name="approved_uploads"),

    # Email Verification
    path("verify/<str:token>/", views.Verify, name="verify"),

    # Terms and Conditions
    path("terms/", views.Terms, name="terms"),

    # Authentication
    path("password_change/", views.ChangePassword, name="password_change"),
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]