from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

User._meta.get_field('email')._unique = True

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    mobile_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.user.username} Account"

class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    result = models.IntegerField(default=-1)
    def __str__(self):
        return f"Date:{self.date}/ result:{self.result}"