from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid"),
    path("listings/<int:listing_id>/watchlist", views.watchlistadd, name="watchlist_add"),
    path("listings/watchlist", views.watchlist, name="watchlist"),
    path("listings/winnings", views.winnings, name="winnings"),
    path("reset", views.reset, name="BULLSHIT"),
]
