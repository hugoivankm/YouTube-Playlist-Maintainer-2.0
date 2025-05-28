from typing import List, Dict, Any

class Printer:
    @staticmethod
    def terminal_playlist_printer(playlist: Dict[str, Any]):
        """Print to terminal """
        videos: List[Dict[str, Any]] = playlist['videos']
        for video in videos:
            print(f"{video['position']} {video['title']}")
            