from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

auct_status = [
    ('AC','active'),
    ('PA','paused'),
    ('FI','finished')
]

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Auction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.URLField()
    status = models.CharField(max_length=2,choices=auct_status,default='AC')
    created_date = models.DateTimeField(default=now,editable=False)
    def __str__(self):
        return f"{self.title} by : {self.user.username}"

class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bidders")
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE, related_name="auctions")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    won = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} bids : {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commentusers")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name="comment_auctions")
    date = models.DateField(default=now,editable=False)
    message = models.TextField()

    def __str__(self):
        return f"{self.user.username} comment: {self.message}" 

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)