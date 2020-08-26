from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(('is_active'), default=False)

	def __str__(self):
		return self.username