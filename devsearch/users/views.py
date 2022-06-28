from django.shortcuts import render
from .models import Profile

# Create your views here.
def profiles(request):
  profiles = Profile.objects.all()
  
  context = {
    'profiles': profiles
  }
  return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)
  skills = profile.skill_set.exclude(description__exact="")
  subSkills = profile.skill_set.filter(description__exact="")

  print(subSkills)
  # for skill in profile.skill_set.all():
  #   print('-' + skill.name)

  context = {
    'profile': profile,
    'skills': skills,
    'subSkills': subSkills
  }

  return render(request, 'users/user-profile.html', context)