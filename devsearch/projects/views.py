from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Project, Tag, Review
from .utils import searchProjects, paginateProjects
from .forms import ProjectForm, ReviewForm
from django.contrib import messages


# Create your views here.
def projects(request):
  projects, search_query = searchProjects(request)

  # paginator, projects = projects, page = paginateProjects(request, projects)
  page = 1

  # pagination
  if request.GET.get('page'):
    page = request.GET.get('page')
  
  paginator = Paginator(projects, 6)
  projects = paginator.page(page)

  context = {
    'projects': projects,
    'paginator': paginator,
    'search_query': search_query,
    'page': page
    }
  return render(request, 'projects/projects.html', context)


def project(request, pk):

  project = Project.objects.get(id=pk)
  
  form = ReviewForm()

  if request.method == 'POST':
    form = ReviewForm(request.POST)
    review = form.save(commit=False)
    review.project = project
    if request.user:
      review.owner = request.user.profile
    review.save()

    project.getVoteCount

    messages.success(request, "your review was successfully submitted")
    return redirect('project', pk=project.id)

  context = {
    "project": project,
    'form': form,
    }

  return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
  profile = request.user.profile
  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.owner = profile
      project.save()
      return redirect('projects')

  form = ProjectForm()
  context = {'form': form}
  return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
  profile = request.user.profile
  project = profile.project_set.objects.get(id=pk)
  form = ProjectForm(instance=project)

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
      form.save()
      return redirect('projects')


  context = {'form': form}
  return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
  profile = request.user.profile
  project = profile.project_set.objects.get(id=pk)

  if request.method == 'POST':
    project.delete()
    return redirect('projects')

  context = {
    'project': project
  }
  return render(request, 'projects/confirmation.html', context)