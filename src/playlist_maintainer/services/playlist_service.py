import re
import os
import datetime

from enum import Enum

from playlist_maintainer.configs.config import get_app_config
from playlist_maintainer.api_data_fetcher.youtube_client import YouTubeClient
from playlist_maintainer.application_interfaces.exporters.export_to_pdf import export_to_pdf
from playlist_maintainer.application_interfaces.exporters.export_to_text import export_to_text


class PlaylistService:
    def __init__(self):
        config =  get_app_config()
        self.api_client = YouTubeClient(config.youtube_api_key)
             
    def _get_playlist_id_from_url(self, url: str) -> str | None:
        """
        Extracts playlist ID from a YouTube playlist URL.
        Returns None if no playlist ID is found.
        """
        match = re.search(r'(?:list=)([a-zA-Z0-9_-])', url)
        if match:
            return match.group(1)
        return None
    
    def _extract_playlist_id(self, identifier: str) -> str:
        """
        Determines the playlist ID, either by extracting it from a URL or
        assuming the identifier itself is the ID.
        """
        playlist_id = self._get_playlist_id_from_url(identifier)
        if playlist_id:
            return playlist_id
        
        if not identifier:
            raise ValueError("Playlist indentifier cannot be empty.")
         
        pattern =  r'^[a-zA-Z0-9_-]+$'
        if not re.match(pattern, identifier):
            raise ValueError("A Valid YouTube Playlist identifier contains just alphanumeric characters, with '-' or '_'")
        
        if len(identifier) < 20:
            print(f"WARNING: Identifier '{identifier}' looks too short to be a valid YouTube playlist ID. Atempting to use it as is.")
        
        return identifier
    
    class ValidFileTypes(Enum):
        PDF = 'pdf'
        TXT = 'txt'
        
        @classmethod
        def has_value(cls, key):
            return key in cls._value2member_map_
        
    def export_playlist_to_file(
        self,
        playlist_identifier: str,
        output_format: str,
        filename: str | None,
        output_dir_path: str | None = None
    ):
        """
        Fetches playlist items and exports them to a file
        """
        playlist_id = self._extract_playlist_id(playlist_identifier)
        try:
            playlist_items = self.api_client.get_playlist_items(playlist_id)
        except Exception as e:
            print(f"ERROR(Service): Failed to fetch playlist items for ID '{playlist_id}': {e}")
            raise
        
        if not output_dir_path:
            output_dir_path = os.getcwd()
        
        if not self.ValidFileTypes.has_value(output_format.lower()):
            raise ValueError("Invalid output file format")
        
        if not filename:
            filename = "playlist"
        
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
        filename = filename + timestamp
        
        _pattern = r'^[a-zA-Z0-9_-.]+$'
        if not re.match(_pattern, filename):
            raise ValueError("A Valid filename for ytpl contains just alphanumeric characters, plus '-', '_' and '.'")
         
        os.makedirs(output_dir_path, exist_ok=True) 
        expanded_output_dir_path = os.path.expanduser(output_dir_path)
        full_output_file_path = os.join(expanded_output_dir_path, f"{filename}_{output_format.lower()}")
        
        try:
            # TODO: Properly retrieve playlist title
            provisional_playlist_title = "Playlist"
            if output_format == 'pdf':
                export_to_pdf(playlist_items, full_output_file_path)
            elif output_format == 'txt':
                export_to_text(playlist_items, full_output_file_path)
            else:
                raise ValueError(f"Unsupported export format: {output_format}")   
        except Exception as e:
            print(f"ERROR(Service): Failed to export {output_format} file to '{full_output_file_path}': {e}")
            raise
    
    
    
    