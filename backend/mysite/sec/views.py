from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserRegisterForm, EditProfile
from django.contrib.auth import authenticate, login
import json
from django.http import HttpResponse, JsonResponse
# from .models import User_Self
# Create your views here.

def home(request):
	return render(request, 'sec/home.html', {})

def faq(request):
	return render(request, 'sec/faq.html', {})

@login_required
def profile(request):
	return render(request, 'sec/profile.html', {})

@login_required
def edit(request):
	if request.method == 'POST':
		form = EditProfile(request.POST, instance = request.user)
		if form.is_valid():
			user = form.save()
			return redirect('profile')
		else:
			messages.error(request, 'Please correct the following errors.')
	else:
		form = EditProfile(instance = request.user)
	return render(request, 'sec/edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    response = render(request, 'sec/password_change.html', {
        'form': form
    })
    response.set_cookie('password_changed', 'true')
    return response 

def login_api(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		username = data.get('username', None)
		password = data.get('password', None)
		per_user = authenticate(username=username, password=password)
		if per_user is not None:
			response_validity = {"boolean": True, "username": per_user.username,"name": per_user.get_full_name(), "email": per_user.email}
		else:
			response_validity = {"boolean": False}
		return HttpResponse(JsonResponse(response_validity, safe=False))

def register(request):
	args = {}
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save(request)
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for { username }!')
			return redirect('profile')
	else:
		form = UserRegisterForm()
	args['form'] = form
	return render(request, 'sec/register.html', {'form': form}, args)