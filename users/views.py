from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm

from .forms import customUserCreation


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.object.get(username=username)

        except:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profiles')
        else:
            messages.error(request, 'username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, 'User logged out successful')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = customUserCreation()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = customUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registered successful')
            login(request, user)
            return redirect('profiles')
        else:
            messages.warning(
                request, 'An error has occured during registration')

    return render(request, 'users/login_register.html', context)


def profies(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkils = profile.skill_set.filter(description="")
    context = {'profile': profile,
               'topSkills': topSkills, 'otherSkills': otherSkils}
    return render(request, "users/user-profile.html", context)
