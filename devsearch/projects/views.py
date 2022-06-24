from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


# Create your views here.
def projects(request):
  msg = 'You are on the projects page'
  num = 10
  projects = Project.objects.all()
  context = {
    'msg': msg, 
    'num':10,
    'projects': projects
    }
  return render(request, 'projects/projects.html', context)


def project(request, pk):

  project = Project.objects.get(id=pk)

  context = {
    "project": project,
    # "tags": project.tags.all(),
    }

  return render(request, 'projects/single-project.html', context)

def createProject(request):
  
  if request.method == 'POST':
    form = ProjectForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('projects')


  form = ProjectForm()
  context = {'form': form}
  return render(request, 'projects/project_form.html', context)

def updateProject(request, pk):
  project = Project.objects.get(id=pk)
  form = ProjectForm(instance=project)

  if request.method == 'POST':
    form = ProjectForm(request.POST, instance=project)
    if form.is_valid():
      form.save()
      return redirect('projects')


  context = {'form': form}
  return render(request, 'projects/project_form.html', context)

def deleteProject(request, pk):
  project = Project.objects.get(id=pk)

  if request.method == 'POST':
    project.delete()
    return redirect('projects')

  context = {
    'project': project
  }
  return render(request, 'projects/confirmation.html', context)