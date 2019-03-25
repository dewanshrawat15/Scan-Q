from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserRegisterForm, EditProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json
import datetime
import hashlib
from django.http import HttpResponse, JsonResponse
from .models import extended_user, teacher_user, student_list
from .forms import ExtendedUserForm, TeacherUserForm

def home(request):
	return render(request, 'sec/home.html', {})

def faq(request):
	return render(request, 'sec/faq.html', {})

def capture(request, key):
	if request.method == 'POST':
		stu_data = json.loads(request.body)
		temp_username = stu_data.get('username', None)
		dummy_user = User.objects.get(username=temp_username)
		stu_code = dummy_user.pk
		corr_teacher = teacher_user.objects.get(sha_digest=key)		
		curr_date = str(datetime.datetime.now().date())
		stripped_date = ''.join(e for e in curr_date if e.isalnum())
		sub_name = corr_teacher.subject_name
		try:
			record = student_list.objects.get(digest=key, student_code=stu_code)
		except student_list.DoesNotExist:
			record = False
		if not record:
			student_list.objects.create(student_code=stu_code, digest=key, subject=sub_name, att_date=stripped_date)
		else:
			record.attendance = record.attendance + 1
			record.att_date = stripped_date
			record.save()
		corr_teacher.count = corr_teacher.count - 1
		corr_teacher.save()
		li_att_stu = student_list.objects.filter(digest=key, att_date=stripped_date)
		li_att_name = []
		for i in li_att_stu:
			code = i.student_code
			corr_user = User.objects.get(pk=code)
			name = corr_user.get_full_name()
			li_att_name.append(name)
		li_att_name = list(li_att_name)
		data = JsonResponse(li_att_name, safe=False)
		print(li_att_name)
		return HttpResponse('<h1>Attendance Recorded</h1>')
	else:
		return HttpResponse('<h1>Hey kid, Go back, you cannot hack</h1>')

@login_required
def qr(request, key):
	y = request.user.pk
	temp = extended_user.objects.get(user_code=y)
	if temp.teacher == True:
		base = 'http://127.0.0.1:8000/capture/'
		url = base + key + '/attend'
		url = str(url)
		return render(request, 'sec/display.html', {'lecture_url': url})
	else:
		return HttpResponse('<h1>How long are you gonna try kid?</h1>')

@login_required
def teacher(request):
	y = request.user.pk
	temp = extended_user.objects.get(user_code=y)
	if temp.teacher == True:
		if request.method == 'POST':
			form_temp = TeacherUserForm(request.POST)
			if form_temp.is_valid:
				form = form_temp.save(commit=False)
				sub_name = form_temp.cleaned_data.get('subject_name')
				cl_name = form_temp.cleaned_data.get('class_name')
				count = form_temp.cleaned_data.get('count')
				code = y
				comp_str = cl_name + sub_name + str(code)
				comp_str = comp_str.lower()
				stripped_string = ''.join(e for e in comp_str if e.isalnum())
				key = hashlib.sha256(stripped_string.encode())
				key = key.hexdigest()
				try:
					record = teacher_user.objects.get(sha_digest=key)
				except teacher_user.DoesNotExist:
					record = False
				if not record:
					teacher_user.objects.create(class_name=cl_name, subject_name=sub_name, teacher_code=code, sha_digest=key, count=count)
				else:
					record.lectures = record.lectures + 1
					record.count = count
					record.save()
				return redirect('qr', key=key)
		else:
			form_temp = TeacherUserForm()
		return render(request, 'sec/gen.html', {'form': form_temp})
	else:
		return HttpResponse('<h1>Access Denied</h1>')

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
		ex_form = ExtendedUserForm(request.POST)
		if form.is_valid() and ex_form.is_valid():
			form.save(request)
			username = form.cleaned_data.get('username')
			typ = ex_form.cleaned_data.get('teacher')
			print(typ)
			temp = User.objects.get(username=username)
			extended_user.objects.create(user_code=temp.pk, teacher=typ)
			messages.success(request, f'Account created for { username }!')
			return redirect('profile')
	else:
		form = UserRegisterForm()
		ex_form = ExtendedUserForm()
	args['form'] = form
	return render(request, 'sec/register.html', {'form': form, 'ex_form': ex_form}, args)