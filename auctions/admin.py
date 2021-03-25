from django.contrib import admin
from .models import Auction,Category,Bid,Watchlist,Comment
# Register your models here.
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)