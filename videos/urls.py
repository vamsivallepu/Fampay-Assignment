from django.urls import path
from .views import GetStoredVideosView, VideoDashboardView

urlpatterns = [
    path('videos/', GetStoredVideosView.as_view(), name='videos'),
    path('dashboard/', VideoDashboardView.as_view(), name="dashboard"),
]