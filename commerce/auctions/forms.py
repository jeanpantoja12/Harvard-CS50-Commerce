from django import forms
from .models import Auction,Comment,Bid


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ('user','status',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder' :'Enter Title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user','placeholder' :'Enter Description...','rows':5}),
            'start_bid': forms.NumberInput(attrs={'class':'form-control form-control-user','placeholder':'0'}),
            'image_url': forms.URLInput(attrs={'class':'form-control form-control-user'}),
            'category' : forms.Select(attrs={'class':'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user','auction')
        widgets = {
            'message': forms.Textarea(attrs={'class':'form-control form-control-user','placeholder':'Write your comment','rows':5})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('user','auction','won')
        widgets = {
            'price': forms.NumberInput(attrs={'class':'form-control form-control-user','placeholder':'0'})
        }