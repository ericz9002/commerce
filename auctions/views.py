from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, CommentForm, BidForm, CategoryForm
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from .models import User, Listing, Bid, Comment, Category
import pdb
from .serializers import ListingSerializer
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ValidationError
import datetime
import requests


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    if request.user.is_authenticated:
        for active_listing in active_listings:
            if active_listing in request.user.watchList.all():
                active_listing.in_watchlist = True
            else:
                active_listing.in_watchlist = False
    return render(request, "auctions/index.html", {
        "is_active": True, "listings": active_listings, "place_bid": True
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def inactive_listings(request):
    inactive_listings = Listing.objects.filter(is_active=False)
    if request.user.is_authenticated:
        for inactive_listing in inactive_listings:
            if inactive_listing in request.user.watchList.all():
                inactive_listing.in_watchlist = True
            else:
                inactive_listing.in_watchlist = False
    return render(request, "auctions/index.html", {"active": False, "listings": inactive_listings, "place_bid":True})

def inactive_listing(request, listing_id):
    pass


@login_required 
def create_listing(request):
    print(f"in create_listing, request.method is {request.method}")
    if request.method == "POST":
        form = ListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.price = form.cleaned_data["price"]
            listing.image = form.cleaned_data["image"]
            listing.creator = request.user
            listing.save()
            for str_category in form.cleaned_data["category"]:
                category = Category.objects.get(name=str_category)
                listing.category.add(category)

            return HttpResponseRedirect(reverse("index"))
        else:
            print(f"form.errors is {form.errors}")
            return render(request, "auctions/create-listing.html", {"ListingForm": form})
    else:
        return render(request, "auctions/create-listing.html", {"ListingForm": ListingForm()})
    
def listing(request, username, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, creator__username=username)
    serialized_listing = ListingSerializer(listing)
    serialized_listing = json.dumps(serialized_listing.data)
    comments = Comment.objects.filter(listing=listing)
    if request.user.is_authenticated:
        if listing in request.user.watchList.all():
            listing.in_watchlist = True
        else:
            listing.in_watchlist = False
    print(f"serialized_listing is of type {type(serialized_listing)} and has value {serialized_listing}")
    return render(request, "auctions/listing.html", {
        "listing":listing, "serialized_listing": serialized_listing, "place_bid": True, "comments":comments, 
        "CommentForm": CommentForm(), "user":request.user
    })

def listing_layout(request, username, listing_id):
    print("here")
    listing = get_object_or_404(Listing, id=listing_id, creator__username=username)
    if listing.is_active:
        place_bid = True
    else:
        place_bid = False
    return render(request, "auctions/listing-layout.html", {"listing":listing, "place_bid": place_bid})


def add_comment(request):
    try:
        data = json.loads(request.body)  # Parse JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    form = CommentForm(data)
    if form.is_valid():
        comment = Comment()
        comment.comment = form.cleaned_data["comment"]
        comment.author = request.user
        listing = Listing.objects.get(title=data['listing']['title'], creator=data['listing']['creator'])
        comment.listing = listing
        comment.save()
        print('saved comment')
        html = render(request, "auctions/comment-layout.html", {"comment": comment})
        return html
    else:
        print(f"form.errors is {form.errors}")
        return render(request, "auctions/test.html", {"form":form})

def delete_comment(request):
    try:
        data = json.loads(request.body)  # Parse JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    id = data['comment_id']
    comment = Comment.objects.get(id=id)
    if request.user == comment.author:
        comment.delete()
        return JsonResponse({"comment_id": id, "message": "Comment deleted successfully."}, status=200)
    else:
        return JsonResponse({"error": "You are not authorized to delete this comment."}, status=403)

def bid(request, username, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, creator__username=username)
    if request.user.is_authenticated:
        if listing in request.user.watchList.all():
            listing.in_watchlist = True
        else:
            listing.in_watchlist = False
    serialized_listing = ListingSerializer(listing)
    serialized_listing = json.dumps(serialized_listing.data)
    bids = Bid.objects.filter(listing=listing)
    in_watchlist = listing in request.user.watchList.all()
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = Bid()
            bid.author = request.user
            bid.listing = Listing.objects.get(title=listing.title, creator__username=username)
            bid.amount = form.cleaned_data["amount"]
            try:
                bid.save()
            except ValidationError as e:
                form.add_error("amount", e)
                return render(request, "auctions/bid.html", {
                    "listing":listing, "serialized_listing": serialized_listing, "place_bid":False, 
                    "BidForm":form, "user":request.user, "bids":bids, "close_date":listing.close_date
                })
        return HttpResponseRedirect(reverse("bid", args=(username, listing.id)))
    else:
        print(f"serialized_listing is of type {type(serialized_listing)} and has value {serialized_listing}")
        return render(request, "auctions/bid.html", {
            "listing":listing, "serialized_listing": serialized_listing, "place_bid":False, "BidForm":BidForm(), 
            "user":request.user, "bids":bids, "close_date":listing.close_date
        })
    
def close(request, username, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id, creator__username=username)
        listing.is_active = False
        listing.close_date = datetime.datetime.now()
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(username, listing_id)))
    else:
        return JsonResponse({"error": "Method not allowed, make sure you make a post request"}, status=405)

def add_watchlist(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                listing = get_object_or_404(Listing, id=data['listing_id'])
            except Http404:
                msg = f"Could not find listing with id {data['listing_id']}"
                return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})
            if listing in request.user.watchList.all():
                msg = f"{listing.title} is already in your watchlist"
                return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})
            else:
                request.user.watchList.add(listing)
                msg = f"successfully added {listing.title} to watchlist"
                return render(request, "auctions/notification-layout.html", {"success": True, "notification_msg": msg})
        except json.JSONDecodeError:
            msg = f"Could not decode request body, Invalid JSON"
            return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})
    else:
        return JsonResponse({"error": "Method not allowed, make sure you make a post request"}, status=405)
    
def remove_watchlist(request):
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            try:
                listing = get_object_or_404(Listing, id=data['listing_id'])
            except Http404:
                msg = f"Could not find listing with id {data['listing_id']}"
                return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})     
            if listing not in request.user.watchList.all():
                msg = f"Could not remove {listing.title} because {listing.title} is not in your watchlist"
                return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})
            else:
                request.user.watchList.remove(listing)
                msg = f"successfully removed {listing.title} from your watchlist"
                return render(request, "auctions/notification-layout.html", {"success": True, "notification_msg": msg})       
        except json.JSONDecodeError:
            msg = f"Could not decode request body, Invalid JSON"
            return render(request, "auctions/notification-layout.html", {"success": False, "notification_msg": msg})
    else:
        return JsonResponse({"error": "Method not allowed, make sure you make a post request"}, status=405)

def watchlist(request, username):
    listings = request.user.watchList.all()
    for listing in listings:
        listing.in_watchlist = True
    return render(request, "auctions/watchlist.html", {"user":request.user, "listings":listings})

def categories(request):
    return render(request, "auctions/categories.html", {"CategoryForm": CategoryForm(), "categories":Category.objects.all()})

def category_data(request, category):
    listings = Listing.objects.filter(category__name=category, is_active=True)
    html = ""
    for listing in listings:
        endpoint = reverse("listing_layout", args=[listing.creator.username, listing.id])
        url = request.build_absolute_uri(endpoint)
        response = requests.get(url)
        if response.raise_for_status() == None:
            html += response.text
        else:
            return JsonResponse({"error": "Failed to fetch listing data"}, status=response.status_code)
    return HttpResponse(html)
