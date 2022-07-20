from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from . import views

urlpatterns = [
  path('', views.getRoutes),
  path('projects/', views.getProjects),
  path('project/<str:pk>/', views.getProject),
  path('project/<str:pk>/vote', views.projectVote),

  path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]