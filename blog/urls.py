from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('',views.userLogin,name='user_login'),
    path('signup/',views.userSignUp,name='user_signup'),
    path('logout/',views.userLogout,name='user_logout'),
    path('about/',views.aboutPage,name='about'),
    path('<int:user_id>/profile/',views.profile,name='profile'),
    path('<int:user_id>/',views.home_page,name='home_page'),
    path('<int:user_id>/search_results/',views.searchResults,name='search_results'),
    path('<int:user_id>/watching/',views.watching,name='watching'),
    path('<int:user_id>/watched/',views.watched,name='watched'),
    path('<int:user_id>/not_watched/',views.notWatched,name='not_watched'),
    path('<int:user_id>/<int:blog_post_id>/',views.blog_post,name='blog_post'),
    path('/<int:blog_post_id>/completed',views.completed,name='completed'),
    path('/<int:blog_post_id>/watching',views.watching_btn,name='watching_btn'),
    path('<int:user_id>/create_new_post',views.createNewPost,name='create_new_post')
]


