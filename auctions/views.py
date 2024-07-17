from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Watchlist, Comment


def index(request):
    listings = Listing.objects.filter(winner_id=None)
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings":listings,
        "type": request.GET.get("type", False),
        "message": request.GET.get("message", False),
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing_id)
    watchlist = {}
    if request.user != "AnonymousUser":
        user = request.user.id
        watchlist = Watchlist.objects.filter(user=user, listing=listing)
    else:
        watchlist = 0
    

    highest_bid = False
    for bid in bids:
        if bid.bid > highest_bid:
            highest_bid = bid.bid
            
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid":highest_bid,
        "type": request.GET.get("type", False),
        "message": request.GET.get("message", False),
        "watchlist":watchlist,
        "comments":comments,
    })

@login_required(login_url="auctions:login")
def close_listing(request, listing_id):
    if request.method == "POST":
        bids = Bid.objects.filter(listing=listing_id)
        listing = Listing.objects.get(id=listing_id)
        highest_bid = False
        try:
            for bid in bids:
                if not highest_bid:
                    highest_bid = bid
                elif bid.bid > highest_bid.bid:
                    highest_bid = bid
            listing.winner_id = highest_bid.user
            listing.save()
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=success&message=Closing listing success.")
        except:
            listing.winner_id = request.user
            listing.save()
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=anounce&message=Listing is closed without winner.")

        # TODO get highest bidder and set as winner_id for listing
    return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=fail&message=How did you get here.")

@login_required(login_url="auctions:login")
def bid(request,listing_id):
    if request.method == "POST":
        highest_bet = False
        listing = Listing.objects.get(id=listing_id)
        bids = Bid.objects.filter(listing=listing_id)
        bidvalue = request.POST.get("bid")
        for bid in bids:
            if bid.bid > highest_bet:
                highest_bet = bid.bid
        if float(bidvalue) > float(highest_bet):
            highest_bet = bidvalue
            newbid = Bid(user=request.user, listing=listing, bid=highest_bet)
            newbid.save()
            listing.current_bid = bidvalue
            listing.save()
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=success&message=Bid placed successfully")
        else:
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=fail&message=Bid is to low")

@login_required(login_url="auctions:login")  
def watchlistadd(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user
        watchlist = Watchlist.objects.filter(user=user, listing=listing)
        try:
            if(len(watchlist) == 1):
                watchlist[0].delete()
                return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=success&message=listing is removed from your watchlist")
            else:
                newWatchlist = Watchlist(user=user, listing=listing)
                newWatchlist.save()
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=success&message=listing is added to your watchlist")
        except:
            return HttpResponseRedirect(f"{reverse("auctions:listing", kwargs={"listing_id":listing_id})}?type=fail&message=something went wrong")
@login_required(login_url="auctions:login")
def watchlist(request):
    user = request.user
    watchlist_items = Watchlist.objects.filter(user=user)
    listings = []
    for item in watchlist_items:
        if item.listing.winner_id == None:
            listings.append(item.listing)
    return render(request, "auctions/index.html", {
        "title": "Watchlist",
        "listings": listings,
    })

@login_required(login_url="auctions:login")
def winnings(request):
    listings = Listing.objects.filter(winner_id=request.user).exclude(user_id=request.user)

    return render(request, "auctions/index.html",{
        "title": "Winnings",
        "listings": listings,
    })

@login_required(login_url="auctions:login")
def create_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title").capitalize()
        description = request.POST.get("description").capitalize()
        starting_bid = request.POST.get("starting_bid")
        image_url = request.POST.get("image_url")
        category = request.POST.get("category").capitalize()
        try:
            if image_url == "":
                image_url = False
            NewListing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, user_id=user)
            NewListing.save()
            return HttpResponseRedirect(f"{reverse("auctions:index")}?type=success&message=New listing added successfully")
        except:
            return HttpResponseRedirect(f"{reverse("auctions:index")}?type=fail&message=oops something went wrong")
    categories = Listing.objects.values("category").distinct()
    return render(request, "auctions/create_listing.html",{
        "categories":categories,
    })

def category(request):
    category = request.GET.get("category", "None").capitalize()
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html",{
        "title":category,
        "listings":listings,
    })

@login_required(login_url="auctions:login")
def comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment")
        listing = Listing.objects.get(id=listing_id)
        NewComment = Comment(listing=listing, user=user, comment=comment)
        NewComment.save()
        return HttpResponseRedirect(reverse("auctions:listing", kwargs={"listing_id":listing_id}))




@login_required(login_url="auctions:login")
def reset(request):
    listings = Listing.objects.all()

    for listing in listings:
        listing.winner_id = None
        listing.save()
            
    return HttpResponseRedirect(f"{reverse("auctions:index")}?type=anounce&message=closed listings are open again")

