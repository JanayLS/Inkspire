from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.gallery_feed, name='gallery_feed'),
    path('upload/', views.upload_artwork, name='upload_artwork'),
    path('comment/<int:artwork_id>/', views.add_comment, name='add_comment'),
    path('like/<int:artwork_id>/', views.like_artwork, name='like_artwork'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete-like/<int:like_id>/', views.delete_like, name='delete_like'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
]