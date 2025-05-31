def format_item_line(item: dict)-> str:
    """
    Helper function to format a single playlist item into a text line.
    Expected format: "{position}. {title}"
    
    Args:
        item (dict): A dictionary containing a youtube playlist item representing a video with at least
        a position and title keys.
    """

    try:
        position = item['position']
        title = item['title']
        return f"{position}. {title}"
    except KeyError as e:
        print(f"Warning: Missing expected key in item data for formatting: {e}. Item: {item.get('snippet', {})}")
        return f"Error formatting item: Missing {e}"