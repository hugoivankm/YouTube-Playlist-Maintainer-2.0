class PlaylistDetails:
    """
    Represents the metadata of a YouTube playlist itself.
    """
    def __init__(self,
                 id: str,
                 title: str,
                 description: str,
                 published_at: str,
                 channel_id: str,
                 channel_title: str):
        self.id = id
        self.title = title
        self.description = description
        self.published_at = published_at
        self.channel_id = channel_id
        self.channel_title = channel_title

    def __repr__(self):
        return (f"Playlist(id='{self.id}', title='{self.title}', "
                f"channel_title='{self.channel_title}')")

    def __str__(self):
        return (f"Playlist: {self.title}\n"
                f"Channel: {self.channel_title} (ID: {self.channel_id})\n"
                f"Published: {self.published_at}\n"
                f"Description: {self.description[:100]}..." if self.description else "No description.")
