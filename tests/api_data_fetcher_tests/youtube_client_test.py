"""
Manual tests just to visualize in the terminal
"""

import os
import sys

from playlist_maintainer.api_data_fetcher import youtube_client
from . import config

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TEST_PLAYLIST_ID = "PLF3zXdEnM3eU2TSmpJwldiXU_geOQhDkF"


try:
    config.load_environment_variables("dev.env")    
        
    client = youtube_client.YouTubeClient(os.getenv("YOUTUBE_API_KEY"))
    
    print("YouTube Client initialized successfully.") 
    
    # --- Get Playlist Details ---
    print(f"\n--- Getting details for playlist: {TEST_PLAYLIST_ID} ---")
    playlist_details = client.get_playlist_details(TEST_PLAYLIST_ID)
    print(f"Playlist Title: {playlist_details.get('title')}")
    print(f"Playlist Description: {playlist_details.get('description', 'N/A')[:99]}...")
    print(f"Published At: {playlist_details.get('published_at')}")
    
    # --- Get All Playlist Videos ---
    print(f"\n--- Getting items for playlist: {TEST_PLAYLIST_ID} ---")
    playlist_data = client.get_playlist_items(TEST_PLAYLIST_ID)
    
    print(f"Retrieved {len(playlist_data['videos'])} videos from playlist.")
    print("Last 4 videos:")
    for i, video in enumerate(playlist_data['videos'][-6:]):
        print(f"  {len(playlist_data['videos']) - 4 + i + 1}. Pos: {video['position']}, Title: {video['title']}, ID: {video['id']}")
        
    
except ValueError as ve:
    print(f"Configuration Error or Invalid Input: {ve}")
except HttpError as he:
    print(f"YouTube API Error: {he}")
    print(f"Status: {he.resp.status}, Content: {he.content.decode()}")
except RuntimeError as re:
    print(f"Application Error: {re}")
except Exception as e:
            print(f"An unexpected error occurred: {e}")
            