from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .utils import searchProfiles
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

def loginUser(request):
  page = "login"
  if request.user.is_authenticated:
    return redirect('profiles')

  if request.method == "POST":
    username = request.POST['username'].lower()
    password = request.POST['password']

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'Username does not exist')

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect(request.GET['next'] if 'next' in request.GET else 'account')
    else:
      messages.error(request, "Username or password is incorrect")

  context = {
    'page': page
  }
  return render(request, 'users/login_register.html', context)

def logoutUser(request):
  logout(request)
  messages.info(request, "User was logged out")
  return redirect('login') 

def registerUser(request):
  page = 'register'
  form = CustomUserCreationForm()

  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()

      messages.success(request, "User account has been created")
      login(request, user)
      return redirect('edit-account')
    
    else:
      messages.error(request, 'An error has occurred during registation')

  context = {
    'page': page,
    'form': form
    }
  return render(request, 'users/login_register.html', context)

#######################################
#
#  PROFILES
#
######################################

# Create your views here.
def profiles(request):
  profiles, search_query, sort_by = searchProfiles(request)
  
  # paginator, projects = projects, page = paginateProjects(request, projects)
  page = 1

  # pagination
  if request.GET.get('page'):
    page = request.GET.get('page')
  
  paginator = Paginator(profiles, 4)
  profiles = paginator.page(page)

  context = {
    'profiles': profiles,
    'paginator': paginator,
    'page': page,
    'search_query': search_query,
    'sort_by': sort_by
  }
  return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)
  skills = profile.skill_set.exclude(description__exact="")
  subSkills = profile.skill_set.filter(description__exact="")
  profile.getProjectData

  context = {
    'profile': profile,
    'skills': skills,
    'subSkills': subSkills
  }

  return render(request, 'users/user-profile.html', context)

@login_required(login_url="login")
def userAccount(request):
  profile = request.user.profile
  profile.getProjectData

  context = {
    'profile': profile
    }
  return render(request, 'users/account.html', context)

@login_required(login_url="login")
def editAccount(request):
  profile = request.user.profile
  form = ProfileForm(instance=profile)

  if request.method=='POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    
    if form.is_valid():
      form.save();

      return redirect('account')

    else:
      messages.error(request, "Please fill out your name, email, and username")
   
  context = {
    'form': form
  }
  return render(request, 'users/profile_form.html', context)

#######################################
#
#  SKILLS
#
######################################

@login_required(login_url="login")
def addSkill(request):
  page = 'add-skill'
  profile = request.user.profile
  skillForm = SkillForm()

  if request.method == 'POST':
    skillForm = SkillForm(request.POST)
    if skillForm.is_valid():
      newSkill = skillForm.save(commit=False)
      newSkill.owner = profile
      newSkill.save()
      return redirect('account')



  context = {
    'page': page,
    'profile': profile,
    'skill_form': skillForm
  }

  return render(request, 'users/account.html', context)

@login_required(login_url="login")
def deleteSkill(request, pk):
  page = 'delete'
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)

  if request.method == 'POST':
    skill.delete()
    return redirect('account')

  context = {
    'skill': skill,
    'page': page,
    'profile': profile,
  }
  return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editSkill(request, pk):
  page = 'edit-skill'
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  skillForm = SkillForm(instance = skill)

  if request.method == 'POST':
    skillForm = SkillForm(request.POST, instance=skill)
    if skillForm.is_valid():
      skillForm.save()
      return redirect('account')

  context = {
    'skill': skill,
    'page': page,
    'profile': profile,
    'skill_form': skillForm
  }
  return render(request, 'users/account.html', context)

##################################
#
# #########  MESSAGES  #########
#
#################################

@login_required(login_url="login")
def inbox(request):
  profile = request.user.profile
  profileMessages = profile.messages.all()
  unreadCount = len(list(filter(lambda a: not a.is_read, profileMessages)))

  context = {
    'profile': profile,
    'profileMessages': profileMessages,
    'unreadCount': unreadCount
  }

  return render(request, 'users/inbox.html', context)

@login_required(login_url="login")
def showMessage(request, pk):
  currentMessage = Message.objects.get(id=pk)

  if not currentMessage.is_read:
    currentMessage.is_read = True
    currentMessage.save()

  context = {
    'currentMessage': currentMessage
  }

  return render(request, 'users/message.html', context)

@login_required(login_url="login")
def sendMessage(request, pk):
  recipient = Profile.objects.get(id=pk)
  sender = request.user.profile
  form = MessageForm()

  if request.method == 'POST':
    form = MessageForm(request.POST)

    if form.is_valid():
      newMessage = form.save(commit=False)

      newMessage.recipient = recipient
      newMessage.sender = sender
      newMessage.name = sender.name
      newMessage.save()

      return redirect('user-profile', pk)


  context = {
    'recipient': recipient,
    'form': form
  }

  return render(request, 'users/message_form.html', context)