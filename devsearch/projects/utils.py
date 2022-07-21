from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator

def searchProjects(request):
  search_query = ''
  sort_by = "-vote_ratio"

  if request.GET.get('sort_by'):
    sort_by = request.GET.get('sort_by')
    
  
  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')
  
  tags = Tag.objects.filter(name__iexact=search_query)

  projects = Project.objects.distinct().filter(
    Q(title__icontains=search_query) |
    Q(owner__name__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(tags__in=tags)
    ).order_by(sort_by, '-vote_total', 'title')

  if sort_by == 'vote_ratio':
    sort_by = 'Least Popular'
  elif sort_by == '-created':
    sort_by = 'Newest'
  elif sort_by == 'created':
    sort_by = 'Oldest'
  else:
    sort_by = 'Most Popular'
  

  return projects, search_query, sort_by

def paginateProjects(request, projects):
  page = 1

  # pagination
  if request.GET.get('page'):
    page = request.GET.get('page')
  
  paginator = Paginator(projects, 6)
  projects = paginator.page(page)

  return paginator, projects, page

def createOrder(request, projects):
  
  def getVoteRatio(project):
    return project.get('vote_ratio')

  if request.GET.get('sort_by') == 'least_popular':
    print('PROJECTS: ', projects)
    # projects.sort(reverse=True, key=createOrder)
  
  elif request.GET.get('sort_by') == 'newest':
    pass

  elif request.GET.get('sort_by') == 'oldest':
    pass

  return projects