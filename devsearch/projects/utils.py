from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator

def searchProjects(request):
  search_query = ''
  
  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')
  
  tags = Tag.objects.filter(name__iexact=search_query)

  projects = Project.objects.distinct().filter(
    Q(title__icontains=search_query) |
    Q(owner__name__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(tags__in=tags)
    )

  return projects, search_query

def paginateProjects(request, projects):
  page = 1

  # pagination
  if request.GET.get('page'):
    page = request.GET.get('page')
  
  paginator = Paginator(projects, 6)
  projects = paginator.page(page)

  return paginator, projects, page