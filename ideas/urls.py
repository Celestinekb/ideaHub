from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('ideas/', views.idea_list, name='idea_list'),
    path('submit/', views.submit_idea, name='submit_idea'),
    path('vote/<int:idea_id>/', views.vote_idea, name='vote_idea'),
    path('profile/', views.user_profile, name='profile'),
    path('delete/<int:idea_id>/', views.delete_idea, name='delete_idea'),
    path('signup/', views.signup, name='signup'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
]