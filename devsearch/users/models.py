from django.db import models
import uuid

# !! https://docs.djangoproject.com/en/4.0/ref/contrib/auth/ !!!
from django.contrib.auth.models import User



# Create your models here.

# !!!https://docs.djangoproject.com/en/4.0/topics/signals/!!!


class Profile(models.Model):
  # attributes
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,)
  name = models.CharField(max_length = 200, blank = True, null = True)
  email = models.EmailField(max_length=500, blank=True, null=True)
  username = models.CharField(max_length = 200, blank = True, null = True)
  username = models.CharField(max_length = 200, blank = True, null = True)
  short_intro = models.CharField(max_length = 200, blank = True, null = True)
  location = models.CharField(max_length = 200, blank = True, null = True)
  bio = models.TextField(max_length=500, blank=True, null=True)
  profile_image = models.ImageField(null = True, blank=True, upload_to='profiles/', default='profiles/user-default.png' )
  social_github= models.CharField(max_length = 200, blank = True, null = True)
  social_linkedIn= models.CharField(max_length = 200, blank = True, null = True)
  social_twitter= models.CharField(max_length = 200, blank = True, null = True)
  social_youtube= models.CharField(max_length = 200, blank = True, null = True)
  social_website= models.CharField(max_length = 200, blank = True, null = True)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  def __str__(self):
    return str(self.user.username)

class Skill(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=50)
  description = models.TextField(max_length=500, null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

  def __str__(self):
    return str(self.name)


