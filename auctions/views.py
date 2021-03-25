from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Comment,Bid,Watchlist,Category
from .forms import AuctionForm,CommentForm,BidForm,CategoryForm

def index(request):
    return render(request, "auctions/index.html",{"auctions":Auction.objects.filter(status='AC').order_by('-created_date')})


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

@login_required
def create_listing(request):
    if request.method =="POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionForm()
    
    return render(request,"auctions/create_listing.html",{"form":form})

def view_listing(request,list_id):
    listing = Auction.objects.get(pk=list_id)
    comments = Comment.objects.filter(auction=list_id)
    bids = Bid.objects.filter(auction=listing).count()
    user_list = listing.user.id
    # Check if user has won the listing
    try:
        user_won = Bid.objects.filter(user=request.user,auction=listing).latest('price')
    except:
        user_won = None
    #Declare if listing is mine
    is_mine = False
    if(user_list==request.user.id):
        is_mine=True
    #Declare if I won this listing
    is_winner = False
    if(user_won):
        is_winner = user_won.won
    print(user_won)
    #Declare if the Bid is valid
    is_valid = True
    #Declare if is in Watchlist
    is_watchlist = False
    try:
        watchlist = Watchlist.objects.get(user=request.user,auction=listing)
    except:
        watchlist = None
    if(watchlist):
        is_watchlist = True

    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if(bid_form.is_valid()):
            bid = bid_form.save(commit=False)
            if(bids>0):
                if(float(request.POST['price']) <= listing.start_bid):
                    is_valid=False
                    bid_form = BidForm()
                                
            else:
                if(float(request.POST['price']) < listing.start_bid):
                    is_valid=False
                    bid_form = BidForm()
            if(is_valid):    
                bid.user = request.user
                bid.auction = listing
                bid.save()
                listing.start_bid = bid.price
                listing.save()
                return HttpResponseRedirect(reverse("view_list",args=(list_id,)))   
    else:
        bid_form = BidForm()
    return render(request, "auctions/view_listing.html",{
        "list":listing,
        "is_mine":is_mine,
        "comments":comments,
        "status":listing.status,
        "is_winner":is_winner,
        "bid_form":bid_form,
        "is_valid":is_valid,
        "is_watchlist":is_watchlist,
        "bids": bids
    })

@login_required
def remove_listing(request,list_id):
    listing = Auction.objects.get(pk=list_id)
    try:
        user_won = Bid.objects.filter(auction=listing).latest('price')
    except:
        user_won = None
    user_list = listing.user.id
    if(request.user.id == user_list):
        if request.method == "POST":
            listing.status = 'FI'
            listing.save()
            user_won.won = True
            user_won.save()
            return HttpResponseRedirect(reverse("index"))

@login_required
def add_comment(request,list_id):
    listing = Auction.objects.get(pk=list_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if(form.is_valid()):
            comment = form.save(commit=False)
            comment.user = request.user
            comment.auction = listing
            comment.save()
            return HttpResponseRedirect(reverse("view_list",args=(list_id,)))
    else:
        form = CommentForm()
    return render(request,'auctions/add_comment.html',{'form': form,'id':listing.id})
@login_required
def view_watchlist(request):
    user_watch = Watchlist.objects.filter(user=request.user)
    return render(request,"auctions/view_watchlist.html",{
        "watchlist":user_watch
    })

@login_required
def add_watchlist(request,list_id):
    if request.method == 'POST':
        listing = Auction.objects.get(pk=list_id)
        watchlist = Watchlist.objects.create(user=request.user,auction=listing)
        return HttpResponseRedirect(reverse("view_list",args=(list_id,)))

@login_required
def remove_watchlist(request,list_id):
    if request.method == 'POST':
        listing = Auction.objects.get(pk=list_id)
        watchlist = Watchlist.objects.get(user=request.user,auction=listing)
        watchlist.delete()
        return HttpResponseRedirect(reverse("view_list",args=(list_id,)))

@login_required
def view_category(request):
    categories = Category.objects.all()
    if request.method == "GET":
        category_sel = request.GET.get('categories','')
        if(category_sel):
            if category_sel == 'all':
                listings = Auction.objects.filter(status='AC') 
            else:
                listings = Auction.objects.filter(status='AC',category=category_sel)
        else:
            listings = Auction.objects.filter(status='AC')
    return render(request,"auctions/categories.html",{
        "categories":categories,
        "listings": listings
    })