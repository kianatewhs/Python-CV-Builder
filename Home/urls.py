from django.contrib import admin
from django.urls import path
from .views import upload_file, LoginPage, SignupPage, resume_view, doc_resume_view
from Home import views

urlpatterns = [
    path('',LoginPage,name='LoginPage'),
    path('login/',LoginPage,name='LoginPage'),
    path('signup/',SignupPage,name='SignupPage'),
    path('upload/', upload_file ,name='upload_file'),
    path('resume/',resume_view, name='resume_view'),
    path('doc_resume/',doc_resume_view, name='doc_resume_view'),
    # path('upload_page/',upload_page, name='upload_page'),
    
]