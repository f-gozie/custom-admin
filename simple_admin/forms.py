from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

PLAN_CHOICES = (('wp', 'Weekly Plan'), ('mp', 'Monthly Plan'), ('yp', 'Yearly Plan'))

class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=200)
	savings_plan = forms.ChoiceField(widget=forms.RadioSelect, choices=PLAN_CHOICES)

	class Meta:
		model = CustomUser
		fields = ('id', 'username', 'email', 'password1', 'password2', 'savings_plan')


class EditUserForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("username", "email")

# class ChoosePlanForm(forms.Form):
# 	savings_plan = forms.ChoiceField(widget=forms.RadioSelect, choices=PLAN_CHOICES)

# 	class Meta:
# 		model = CustomUser
# 		fields = ("savings_plan")

class SendEmailForm(forms.Form):
	subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
	message = forms.CharField(widget=forms.Textarea)
	users = forms.ModelMultipleChoiceField(label="To", queryset=CustomUser.objects.all(), widget=forms.SelectMultiple())


class EmailForm(forms.Form):
	text = forms.CharField(label="Email Body", widget=forms.Textarea)