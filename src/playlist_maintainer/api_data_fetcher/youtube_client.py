
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeClient:
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, youtubeApiKey):
        """
        Initializes the YouTube Data API client.
        """
        if not youtubeApiKey:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set")
        self._api_key = youtubeApiKey
        try:
            self.youtube = build(
                    self.API_SERVICE_NAME,
                    self.API_VERSION,
                    developerKey=self._api_key
                ) 
        except Exception as e:
            raise RuntimeError(f"Failed to build YouTube API client: {e}")
        
    def __enter__(self):
        """Returns a Youtube API client object"""
        return self

    def __exit__(self):
        """Ensures clean up in cluster manager"""
        if self.youtube:
            self.close()
    
    def close(self):
        """Handles closing the connections with the YouTube Data API"""
        if self.youtube:
            self.youtube.close()
    
    def get_playlist_items(self, playlist_id: str) -> dict:
        """
        Retrieves all video items from a given YouTube playlist, handling pagination.

        Args:
            playlist_id (str): The ID of the YouTube playlist.

        Returns:
            dict: A dictionary containing playlist id and a list of video details.
                  Example:
                  {
                      "playlist_id": "...",
                      "videos": [
                          {"id": "...", "title": "...", "channel_title": "...", "position": 0},
                          ...
                      ]
                  }
        Raises:
            HttpError: If an API request fails.
            ValueError: If playlist_id is invalid or no items are found.
        """
        all_videos = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response.get('items', []):
                    video_snippet = item.get('snippet', {})
                    video_id = video_snippet.get('resourceId',{}).get('videoId')
                    
                    if video_id:
                        all_videos.append({
                            "id": video_id,
                            "title": video_snippet.get('title'),
                            "channel_title": video_snippet.get('channelTitle'),
                            "position": video_snippet.get('position')
                        })
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break;       
        
                if not all_videos:
                    raise ValueError(f"No videos found for playlist ID: {playlist_id}. Check if the ID is correct and playlist is public.")
                
            return {
                "playlist_id": playlist_id,
                "videos": all_videos
            }
                
        except HttpError as e:
            if e.resp.status == 404:
                raise ValueError(f"Playlist with ID '{playlist_id}' not found or is private. Error: {e}")
            elif e.resp.status == 400:
                 raise ValueError(f"Bad request for playlist ID '{playlist_id}'. Error: {e}")
            else:
                raise HttpError(f"YouTube API error getting playlist items: {e}", e.resp)
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while fetching playlist items: {e}")
    
    def get_playlist_details(self, playlist_id: str) -> dict:
        """
        Retrieves the actual title and other metadata of a YouTube playlist.

        Args:
            playlist_id (str): The ID of the YouTube playlist.

        Returns:
            dict: A dictionary containing playlist details (e.g., id, title, description).
        Raises:
            HttpError: If an API request fails.
            ValueError: If playlist_id is invalid or playlist not found.
        """
        try:
           request = self.youtube.playlists().list(
               part="snippet",
               id=playlist_id
           )
           response = request.execute()
           if not response.get('items'):
               raise ValueError(f"Playlist with ID '{playlist_id}' not found or no details available.")
           
           playlist_snippet = response['items'][0]['snippet']
           return {
               "id": playlist_id,
               "title": playlist_snippet.get('title'),
               "description": playlist_snippet.get('description'),
               "published_at": playlist_snippet.get('publishedAt'),
               "channel_id": playlist_snippet.get('channelId'),
               "channel_title": playlist_snippet.get('channelTitle')
           }

        except HttpError as e:
            if e.resp.status == 404:
                raise ValueError(f"Playlist with ID '{playlist_id}' not found or is private. Error: {e}")
            else:
                raise HttpError(f"YouTube API error getting playlist details: {e}", e.resp)
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while fetching playlist details: {e}")
