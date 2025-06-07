from playlist_maintainer.models.PlaylistItem import PlaylistItem


class PlaylistItems:
    """
    Represents a collection of PlaylistItem objects associated with a specific playlist ID.
    """
    def __init__(self, playlist_id: str, videos: list[PlaylistItem]):
        if not isinstance(videos, list) or not all(isinstance(v, PlaylistItem) for v in videos):
            raise TypeError("Videos must be a list of PlaylistItem objects.")
        self.playlist_id = playlist_id
        self.videos = videos

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, index):
        return self.videos[index]

    def __iter__(self):
        return iter(self.videos)

    def __repr__(self):
        return f"PlaylistItems(playlist_id='{self.playlist_id}', num_videos={len(self.videos)})"

    def __str__(self):
        return (f"Videos for Playlist ID: {self.playlist_id}\n"
                f"Total videos: {len(self.videos)}")