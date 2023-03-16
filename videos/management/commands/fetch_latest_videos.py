import time
from dotenv import dotenv_values
from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone
from videos.models import Video

class Command(BaseCommand):

    def handle(self, *args, **options):
        API_KEY_INDEX=0
        config=dotenv_values('.env')
        YOUTUBE_API_KEYS=config['YOUTUBE_API_KEYS'].split(',')
        
        while True:
            try:
                youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEYS[API_KEY_INDEX])

                search_query = 'Cricket' # predefined search query
                max_results = 20 # number of videos to fetch per API call

                # call the YouTube API to search for videos
                search_response = youtube.search().list(
                    q=search_query,
                    type='video',
                    order='date',
                    part='id,snippet',
                    maxResults=max_results
                ).execute()

                # create a list of videos
                videos = []
                for search_result in search_response.get('items', []):
                    video_id = search_result['id']['videoId']
                    # If fetched video is already in database, then skip
                    available_ids=[list(item)[0] for item in list(Video.objects.values_list('id'))]
                    if video_id in available_ids:
                        continue
                    
                    video_title = search_result['snippet']['title']
                    video_description = search_result['snippet']['description']
                    video_published_at = datetime.fromisoformat(search_result['snippet']['publishedAt'].replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
                    video_thumbnail_url = search_result['snippet']['thumbnails']['default']['url']
                    videos.append(Video(
                        id=video_id,
                        title=video_title,
                        description=video_description,
                        published_at=video_published_at,
                        thumbnail_url=video_thumbnail_url,
                    ))

                # bulk create the videos in the database
                Video.objects.bulk_create(videos)

                print(f'fectched {len(videos)} unique videos')

                # wait for 10 seconds before making the next API call
                time.sleep(10)
            except HttpError as e:
                error = e.response.json()
                # if quota exceeds for one api key, increment the API_KEY_INDEX
                if error["error"]["errors"][0]["reason"] == "quotaExceeded":
                    if API_KEY_INDEX < len(API_KEY_LIST) - 1:
                        API_KEY_INDEX += 1
                        continue
                    else:
                        raise e
                else:
                    raise e