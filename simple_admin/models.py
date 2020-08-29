from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

PLAN_CHOICES = (('wp', 'Weekly Plan'), ('mp', 'Monthly Plan'), ('yp', 'Yearly Plan'))

class CustomUser(AbstractUser):
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(('is_active'), default=True)
	savings_plan = models.CharField(max_length=50, choices=PLAN_CHOICES)
	def __str__(self):
		return self.username