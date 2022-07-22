from .models import Profile, Skill
from django.db.models import Q

def searchProfiles(request):
  search_query = ''
  sort_by = '-review_count'

  if request.GET.get('sort_by'):
    sort_by=request.GET.get('sort_by')


  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')
    
  skills = Skill.objects.filter(name__iexact=search_query)

  profiles = Profile.objects.distinct().filter(
    Q(name__icontains=search_query) |
    Q(short_intro__icontains=search_query) |
    Q(skill__in=skills)
    ).order_by(sort_by, '-name')
  
  # profiles = sortProfiles(profiles, sort_by)

  return profiles, search_query, sort_by