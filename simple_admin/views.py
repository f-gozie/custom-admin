from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from .forms import SignUpForm, EmailForm, SendEmailForm
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


def index(request):
	return render(request, 'index.html', {})


def signup(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('index')
	return render(request, 'registration/signup.html', {'form':form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff:
            	return redirect('admin:index')
            else:
            	return redirect('index')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'registration/login.html')


@login_required
def logout(request):
	auth.logout(request)
	return render(request, "index.html")


@staff_member_required
def broadcast_mail(request):
	form = EmailForm()
	from_email = None
	if request.user.is_authenticated:
		if request.method == "POST":
			form = EmailForm(request.POST)
			if form.is_valid():
				subject = "Broadcast Message to All Users"
				broadcast_message = form.cleaned_data.get('text')
				from_email = request.user.email
				user_email_list = [ p.email for p in CustomUser.objects.all() ]
				send_mail(subject, broadcast_message, from_email, user_email_list)
				return redirect('index')
			else:
				print(form.errors)
	return render(request, 'broadcast.html', {'form': form})


def time_threshold(num):
	num = int(num)
	thresh = datetime.now(tz=timezone.utc) - timedelta(hours=num)
	return thresh


@staff_member_required
def custom_admin(request):
	if request.user.is_staff:
		users_in_past_24_hours = CustomUser.objects.filter(created_at__gt=time_threshold(24))
		users_in_past_week = CustomUser.objects.filter(created_at__gt=time_threshold(168))
		users_in_past_month = CustomUser.objects.filter(created_at__gt=time_threshold(730))
		context = {"users_in_past_24_hours": users_in_past_24_hours, "users_in_past_week": users_in_past_week, "users_in_past_month": users_in_past_month}
	else:
		return redirect('unauthorized')
	return render(request, 'admin_dashboard.html', context)


@require_POST
@staff_member_required
def toggle_user_status_true(request, user_id):
	user = get_object_or_404(CustomUser, id=user_id)
	user.is_active = True
	user.save()

	return redirect('custom_admin')


@require_POST
@staff_member_required
def toggle_user_status_false(request, user_id):
	user = get_object_or_404(CustomUser, id=user_id)
	user.is_active = False
	user.save()
	
	return redirect('custom_admin')


def unauthorized(request):
	return render(request, 'unauthorized.html', {})


class SendUsersEmails(FormView):
	template_name = 'send_email.html'
	form_class = SendEmailForm
	success_url = reverse_lazy('admin:simple_admin_customuser_changelist')

	def form_valid(self, form):
		users = form.cleaned_data.get('users')
		subject = form.cleaned_data.get('subject')
		message = form.cleaned_data.get('message')
		from_email = "fagozie43@gmail.com"
		send_mail(subject, message, from_email, users)
		confirm_message = "{} user(s) mailed successfully!".format(form.cleaned_data['users'].count())
		messages.success(self.request, confirm_message)
		return super(SendUsersEmails, self).form_valid(form)