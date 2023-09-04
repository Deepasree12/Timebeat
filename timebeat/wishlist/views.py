from django.shortcuts import render,redirect


from user.views import *
from .models import *
from user. models import *
from store.models import *
from .models import *
from django.views import View
from django.http import HttpResponseBadRequest
import uuid

# Create your views here.
# @login_required(login_url='signin')//add in wishlist
def add_to_wishlist(request):
    # item=get_object_or_404()
    return redirect(request,'wishlist.html')