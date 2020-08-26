from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=200)

	class Meta:
		model = CustomUser
		fields = ('id', 'username', 'email', 'password1', 'password2')


class EditUserForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("username", "email")

class SendEmailForm(forms.Form):
	subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
	message = forms.CharField(widget=forms.Textarea)
	users = forms.ModelMultipleChoiceField(label="To", queryset=CustomUser.objects.all(), widget=forms.SelectMultiple())


class EmailForm(forms.Form):
	text = forms.CharField(label="Email Body", widget=forms.Textarea)