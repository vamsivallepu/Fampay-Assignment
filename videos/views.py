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


class GetStoredVideosView(View):
    """
        A view that retrieves and displays stored videos.
        Methods:
            get: Retrieves the videos and renders the HTML template.
        Usage:
            Create an instance of this class and add it to the appropriate URL
            pattern in your Django project's urls.py file.
    """

    def get(self, request):
        """
        Retrieve the videos and render the HTML template.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            HttpResponse: The rendered HTML template displaying the videos.
        """
        videos = Video.objects.order_by('-published_at')
        paginator = Paginator(videos, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'videos.html', {'page_obj': page_obj})


class VideoDashboardView(View):
    """
    A view that displays the videos dashboard
    Methods:
        get: Retrieves and filters videos, orders them, and paginates them before rendering the HTML template.
    Usage:
        Create an instance of this class and add it to the appropriate URL
        pattern in your Django project's urls.py file.
    """

    def get(self, request):
        """
        Retrieve and filter videos, order them, and paginate them before rendering the HTML template.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            HttpResponse: The rendered HTML template displaying the dashboard.
        """
        # Get all the videos from the database
        videos = Video.objects.all()

        # Apply filters if provided in the query parameters
        search_query = request.GET.get('search')
        if search_query:
            videos = videos.filter(Q(title__icontains=search_query) | Q(
                description__icontains=search_query))

        # Order the videos if a sort_by parameter is provided in the query string
        sort_by = request.GET.get('sort_by')
        if sort_by:
            videos = videos.order_by(sort_by)

        # Paginate the videos
        paginator = Paginator(videos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Render the HTML template with the paginated videos
        return render(request, 'dashboard.html', {'page_obj': page_obj})
