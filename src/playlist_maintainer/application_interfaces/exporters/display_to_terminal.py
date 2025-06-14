from playlist_maintainer.models.PlaylistDetails import PlaylistDetails
from playlist_maintainer.models.PlaylistItems import PlaylistItems


def display_playlist_to_terminal(
    playlist_details: PlaylistDetails | None,
    playlist_items: PlaylistItems | None,
    limit: int = -1
    ):
    """
    Display playlist details and items in the terminal
    """
    if not playlist_details and not playlist_items:
        print('-' * 80)
        print('-' * 80)
        print('-' * 80)
        return
    
    videos = []
    if playlist_items:
        videos = playlist_items.videos if playlist_items.videos else []
    if playlist_details:
        header = f"\n--- Playlist: {playlist_details.title}"
        if videos:
            header += f" ({len(videos)} items)"
        header += " ---"
        print(header)
    
    display_limit = min(limit, len(videos))
    if limit == -1:
        limit = len(videos)
    if limit < -1:
        raise ValueError("limit must be a positive interger or -1 to display the full video list")
    for i, video in enumerate(videos[:display_limit]):
        print(f"{i+1}. {video.title}")    


    if (display_limit > 0 and len(videos) > display_limit):
        print(f"... and {len(videos) - display_limit} more items (use --limit to show more or --limit -1 to show all) ...")
    print('-' * 80, "\n")
