from . import views
from django.urls import path

app_name='moviereviewapp'
urlpatterns = [

    path('', views.index,name='index'),
    path('movie/<int:movie_id>/',views.detail,name='detail'),
    path('add/',views.add_movie,name='add_movie'),
    path('update/<int:id>/', views.update, name='update'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('addreview/<int:id>/', views.add_review, name="add_review"),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('search/',views.SearchResult,name='SearchResult'),


]