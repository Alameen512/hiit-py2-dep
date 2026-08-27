from projectapp import views
from django.urls import path
urlpatterns = [ 
    path("", views.home, name="home" ),
    path("profile", views.profile, name = "profile"),
    path("about", views.about, name="about" ),
    path("posts", views.posts, name="posts" ),
    path("posts/add/", views.add_post, name="add_post" ),
    path("post/<str:pk>/", views.post, name="post" ),
    path("post/<str:pk>/edit/", views.edit_post, name="edit_post" ),
    path("user/form/", views.display_form, name = "user_form"),
    path("user/create/", views.create_user, name = "create_user"),
    path("user/custom_create/", views.custom_create_user, name = "custom_create_user"),
    path("user/students/", views.student_list, name = "student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<int:id>/edit/", views.student_update, name="student_update"),
    path("students/<int:id>/delete/", views.student_delete, name="student_delete"),
    path("submit/form/", views.submit_form, name = "submit_form"),
    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name = "logout")
]