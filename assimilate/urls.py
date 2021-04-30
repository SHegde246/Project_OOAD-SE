from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static 
from . import views
from django.contrib.auth import views as auth_views



#from django.urls import re_path

urlpatterns = [

	path('',views.first_page, name='first_page'),

	
	path('register',views.register,name='register'),
	
	
	#added
	#path('register',views.register.as_view(),name='register'),
	
	
	path('registered',views.registered,name='registered'),


	#path('home_page', views.home_page, name='home_page'),
	#re_path(r'(login/)?.*home_page$', views.home_page, name='home_page'),
	path('home_page/', views.home_page, name='home_page'),


	path('post_list/', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	
	
	path('browse/', views.browse, name="browse"),


	path('login',views.LoginView.as_view(),name="login"),    #removed the '/' before login
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),


	path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
	
	
	path('edit_logs/', views.edit_logs, name="edit_logs"),
	
	path('search', views.search, name='search'),
	
]
