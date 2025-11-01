from user.forms import SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import UserInfoSerializer
from django.contrib.auth import get_user_model

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "events")
            return redirect(next_url)
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, "frontend/login.html", context)

def SignupView(request):
    form = SignupForm()
    context = {"form": form}

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("mylogin")

    context = {"form": form}
    return render(request, "frontend/signup.html", context)


def DummyView(request):
    return redirect("mylogin")


def LogoutView(request):
    logout(request)
    return redirect("mylogin")

class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class=UserInfoSerializer
    
    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)