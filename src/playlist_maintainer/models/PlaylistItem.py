class PlaylistItem:
    def __init__(
        self,
        title: str,
        channel: str,
        duration: str,
        video_id: str,
        position: str,
        ):
        self.title = title
        self.channel = channel
        self.duration_str = duration
        self.video_id = video_id
        self.position = position

    def __repr__(self):
        return f"PlaylistItem(title='{self.title}', artist='{self.artist}', duration_str='{self.duration_str}')"

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration_str})"