class PlaylistItem:
    def __init__(self, title: str, artist: str, duration_str: str, youtube_url: str):
        self.title = title
        self.artist = artist
        self.duration_str = duration_str
        self.youtube_url = youtube_url

    def __repr__(self):
        return f"PlaylistItem(title='{self.title}', artist='{self.artist}', duration_str='{self.duration_str}')"

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration_str})"