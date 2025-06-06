def display_playlist_to_terminal(
    playlist_details: str | None,
    playlist_items: str | None,
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
    if type(playlist_items) is dict:
        videos = playlist_items['videos']
    elif type(playlist_items) is list:
        videos = playlist_items
    else:
        raise TypeError(f"Parameter playlist_items must be a dictionary or a list")
    
    if playlist_details:
        header = f"\n--- Playlist: {playlist_details['title']}"
        if videos:
            header += f" ({len(videos)} items)"
        header += " ---"
        print(header)
    
    display_limit = min(limit, len(videos))
    if limit == -1:
        limit = len(videos + 1)
    if limit < -1:
        raise ValueError("limit must be a positive interger or -1 to display the full video list")
    for i, video in enumerate(videos[:display_limit]):
        print(f"{i+1}. {video['title']}")    

    if (len(videos) > display_limit):
        print(f"... and {len(videos) - display_limit} more items (use --limit to show more) ...")
    print('-' * 80, "\n")
