# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from apps.authentication.models import User
from apps.home.models import Supplier 

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect("/index")
                elif user.is_manager:
                    login(request, user)
                    return redirect("/manager/")
                elif user.is_warteam:
                    login(request, user)
                    return redirect("/war/")
                elif user.is_opsteam:
                    login(request, user)
                    return redirect("/op")
                elif user.is_supplier:
                    login(request, user)
                    return redirect("/supplier")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})    
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            retype_password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if raw_password == retype_password:
                user = User.objects.create_user(
                        username=username, password=retype_password,
                        email=email, is_supplier=True
                    )
                Supplier.objects.create(user=user, name=username, address=email)
                
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/supplier")
            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

