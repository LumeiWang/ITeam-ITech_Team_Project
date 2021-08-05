from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('category/<slug:category_name_slug>/add_news/', views.add_news, name='add_news'),
    path('register/', views.register, name='register'), 
    path('register_official/', views.register_official, name='register_official'), 
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('category/<slug:category_name_slug>/<str:title>/comment/', views.show_comment, name='show_comment'),
    path('category/<slug:category_name_slug>/<str:title>/news/', views.show_news, name='show_news'),
    path('category/<slug:category_name_slug>/<str:title>/add_comment/', views.add_comment, name='add_comment'),
    path('user/', views.user_info, name='user_info'),
    path('user/<str:data>/delete/', views.delete, name='delete'),
    path('category/', views.category, name='category'),
    path('allpages/', views.allpages, name='allpages'),
]