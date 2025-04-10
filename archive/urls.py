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
    path('approved-thesis/<int:year>/', views.approved_thesis_list_by_year, name='approved_thesis_list_by_year'),
    path('approved-thesis/old/', views.approved_thesis_list_by_old_year, name='approved_thesis_list_by_old_year'),
    
    # Admin
    path("admin_page/", views.AdminPage, name="admin_page"),
    path("pending_uploads/", views.PendingUploads, name="pending_uploads"),
    path("approved_uploads/<str:pk>", views.ApprovedUploads, name="approved_uploads"),
    path("backup/", views.backup_database, name="backup_database"),
    path("restore/", views.restore_database, name="restore_database"),
    path('backup-list/', views.list_backups, name='backup_page'),
    path('backup/delete/<str:filename>/', views.delete_backup, name='delete_backup'),
    path('backup/rename/<str:filename>/', views.rename_backup, name='rename_backup'),

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