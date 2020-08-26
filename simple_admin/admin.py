from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm, EditUserForm, SendEmailForm
from .models import CustomUser
from django.urls import path
from django.contrib.admin.sites import AdminSite
from django.http import HttpResponseRedirect
from django.shortcuts import render

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_filter = ['created_at',]
	list_display = ['username', 'email', 'created_at', 'is_active']

	actions = ['activate_users', 'deactivate_users', 'send_email']

	def activate_users(self, request, queryset):
		queryset.update(is_active=True)

	def deactivate_users(self, request, queryset):
		queryset.update(is_active=False)


	def send_email(self, request, queryset):
		form = SendEmailForm(initial={'users':queryset})
		return render(request, 'send_email.html', {'form':form})

admin.site.unregister(Group)
admin.site.site_header = "Savests Custom Admin"