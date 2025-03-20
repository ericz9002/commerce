from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("inactive", views.inactive_listings, name="inactive_listings"),
    path("inactive/<int:listing_id>", views.inactive_listings, name="inactive_listing"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("add-comment", views.add_comment, name="add_comment"),
    path("delete-comment", views.delete_comment, name="delete_comment"),
    path("<str:username>/watchlist", views.watchlist, name="watchlist"),
    path("<str:username>/<int:listing_id>", views.listing, name="listing"),
    path("getListingLayout/<str:username>/<int:listing_id>", views.listing_layout, name="listing_layout"),
    path("<str:username>/<int:listing_id>/bid", views.bid, name="bid"),
    path("<str:username>/<int:listing_id>/close", views.close, name="close"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("<str:username>/watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category-data/<str:category>", views.category_data, name="category_data"),
]
