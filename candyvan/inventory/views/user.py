from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from ..forms import LoginForm


def login(request):
    # TODO: Make Error Message indication box
    if request.session.get("user_id"):
        return redirect("sell")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['user_id'] = user.id
                return redirect("login")
    else:
        form = LoginForm()

    return render(request, 'inventory/login.html', {'form': form})


def logout(request):
    empty = object()
    if request.session.get("user_id", empty) is not empty:
        del request.session['user_id']

    return redirect("login")
