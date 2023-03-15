from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from rest_framework import generics, serializers
from videos.models import Video
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .serializers import VideoSerializer


# View for JSON response
""" class GetStoredVideosView(generics.ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Video.objects.order_by('-published_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj, many=True)
        data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'results': serializer.data,
        }
        return JsonResponse(data, safe=False) """

# view for stored videos sorted in descending order by published time
class GetStoredVideosView(View):
    def get(self, request):
        videos = Video.objects.order_by('-published_at')
        paginator = Paginator(videos, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'videos.html', {'page_obj': page_obj})

# View to handle dashboard and filters
class VideoDashboardView(View):
    def get(self, request):
        # Get all the videos from the database
        videos = Video.objects.all()

        # Apply filters if provided in the query parameters
        search_query = request.GET.get('search')
        if search_query:
            videos = videos.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        sort_by = request.GET.get('sort_by')
        if sort_by:
            videos = videos.order_by(sort_by)

        # Paginate the videos
        paginator = Paginator(videos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'dashboard.html', {'page_obj': page_obj})

