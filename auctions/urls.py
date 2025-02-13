from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("add-comment", views.add_comment, name="add_comment"),
    path("delete-comment", views.delete_comment, name="delete_comment"),
    path("<str:username>/watchlist", views.watchlist, name="watchlist"),
    path("<str:username>/listing/<str:title>", views.listing, name="listing"),
]
