from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/',views.profile_list,name='profile_list'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('login/',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'), 
    path('update_user/',views.update_user,name='update_user'), 
    path('meeme/like/', views.meeme_like, name='meeme_like'),
    path('meeme_show/<int:pk>',views.meeme_show,name='meeme_show'),
    path('unfollow/<int:pk>',views.unfollow,name='unfollow'),
    path('follow/<int:pk>',views.follow,name='follow'),
    path('profile/followers/<int:pk>',views.followers,name='followers'),
    path('profile/follows/<int:pk>',views.follows,name='follows'),
    path('delete_meeme/<int:pk>',views.delete_meeme,name='delete_meeme'),
    path('edit_meeme/<int:pk>',views.edit_meeme,name='edit_meeme'),
    path('search/',views.search,name='search'),
    path('search_user/',views.search_user,name='search_user'),
]
