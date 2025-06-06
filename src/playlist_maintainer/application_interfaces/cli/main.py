import os
import sys
current_script_dir = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.dirname(os.path.dirname(current_script_dir))

if src_directory not in sys.path:
    sys.path.insert(-1, src_directory)

from playlist_maintainer.api_data_fetcher import youtube_client
from playlist_maintainer.configs import config
from playlist_maintainer.application_interfaces.exporters.display_to_terminal import display_playlist_to_terminal

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


try:
    TEST_PLAYLIST_ID = "PLF4zXdEnM3eU2TSmpJwldiXU_geOQhDkF"
    config.load_environment_variables("dev.env")        
    client = youtube_client.YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
    
    items = client.get_playlist_items(TEST_PLAYLIST_ID)
    details = client.get_playlist_details(TEST_PLAYLIST_ID)
    
    display_playlist_to_terminal(details, items , 10)
    
except ValueError as ve:
    print(f"Configuration Error or Invalid Input: {ve}")
except HttpError as he:
    print(f"YouTube API Error: {he}")
    print(f"Status: {he.resp.status}, Content: {he.content.decode()}")
except RuntimeError as re:
    print(f"Application Error: {re}")
except Exception as e:
            print(f"An unexpected error occurred: {e}")

