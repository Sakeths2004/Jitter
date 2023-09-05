from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meeme
from .forms import MeemeForm,ProfilePicForm,SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.contrib.auth.models import User
def home(request):
    if request.user.is_authenticated:
        form = MeemeForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meeme = form.save(commit=False)
                meeme.user = request.user
                meeme.save()
                messages.success(request, "Your Meeme has been sent!")
                return redirect('home')
        meemes = Meeme.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meemes": meemes, "form": form})
    else:
        meemes = Meeme.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meemes": meemes})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('home')
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username} "))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "You must be logged in to view this page!")        
        return redirect('home')
def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))
def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        meemes = Meeme.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile.html", {"profile": profile, "meemes": meemes})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('home')
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:  
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not your profile page!"))
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('home')
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:  
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not your profile page!"))
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('home')
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged In! Keep Meeming!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging In! Please Try Again...")
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out! Sorry to Meeme You Go...")
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user) 
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Meeme

@login_required(login_url='login')
def meeme_like(request):
    if request.method == 'POST':
        meeme_id = request.POST.get('meemeId')
        meeme = get_object_or_404(Meeme, id=meeme_id)

        if meeme.likes.filter(id=request.user.id).exists():
            meeme.likes.remove(request.user)
            is_liked = False
        else:
            meeme.likes.add(request.user)
            is_liked = True

        like_count = meeme.likes.count()
        data = {
            'like_count': like_count,
            'is_liked': is_liked
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request'})

        
def meeme_show(request,pk):
    meeme = get_object_or_404(Meeme,id=pk)
    if meeme:
        return render(request,"show_meeme.html",{'meeme':meeme})
    else:
        messages.success(request, ("That Meeme does not exist!"))
        return redirect('home')
def delete_meeme(request, pk):
    if request.user.is_authenticated:
        meeme = get_object_or_404(Meeme,id=pk)
        if request.user.username == meeme.user.username:
            meeme.delete()
            messages.success(request, ("The Meeme has been deleted!"))
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, ("You Don't Own That Meeme!"))
            return redirect('home')
    else:
        messages.success(request, ("Please Log In To Continue.."))
        return redirect(request.META.get('HTTP_REFERER'))
def edit_meeme(request, pk):
    if request.user.is_authenticated:
        meeme = get_object_or_404(Meeme,id=pk)
        if request.user.username == meeme.user.username:
            form = MeemeForm(request.POST or None, instance=meeme)
            if request.method == "POST":
                if form.is_valid():
                    meeme = form.save(commit=False)
                    meeme.user = request.user
                    meeme.save()
                    messages.success(request, "Your Meeme has been Updated!")
                    return redirect('home')
            else:
                return render(request, "edit_meeme.html", {'form':form,'meeme':meeme})
        else:
            messages.success(request, ("You Don't Own That Meeme!"))
            return redirect('home')
    else:
        messages.success(request, ("Please Log In To Continue.."))
        return redirect('home')
def search(request):
    if request.method=="POST":
        search = request.POST['search']
        searched = Meeme.objects.filter(body__contains = search)

        return render(request,'search.html',{'search':search, 'searched':searched})
    else:
        return render(request,'search.html',{})
def search_user(request):
    if request.method=="POST":
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)

        return render(request,'search_user.html',{'search':search, 'searched':searched})
    else:
        return render(request,'search_user.html',{})