from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .decorators import unauthenticated_user



