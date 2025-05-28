import os
import sys
current_script_dir = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.dirname(os.path.dirname(current_script_dir))

if src_directory not in sys.path:
    sys.path.insert(-1, src_directory)

from playlist_maintainer.api_data_fetcher import youtube_client
from playlist_maintainer.configs import settings

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from playlist_maintainer.utils.printer import Printer

try:
    
    TEST_PLAYLIST_ID = "PLF4zXdEnM3eU2TSmpJwldiXU_geOQhDkF"
    
    settings.load_environment_variables("dev.env")    
        
    client = youtube_client.YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
    
    playlist = client.get_playlist_items(TEST_PLAYLIST_ID)
    
    Printer.terminal_playlist_printer(playlist)
except ValueError as ve:
    print(f"Configuration Error or Invalid Input: {ve}")
except HttpError as he:
    print(f"YouTube API Error: {he}")
    print(f"Status: {he.resp.status}, Content: {he.content.decode()}")
except RuntimeError as re:
    print(f"Application Error: {re}")
except Exception as e:
            print(f"An unexpected error occurred: {e}")



