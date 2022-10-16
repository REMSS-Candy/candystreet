from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from ..forms import LoginForm


def login_view(request):
    # TODO: Make Error Message indication box
    if request.user.is_authenticated:
        return redirect("sell")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("login")
    else:
        form = LoginForm()

    return render(request, 'inventory/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("login")
