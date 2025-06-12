from playlist_maintainer.application_interfaces.exporters.exporter_utils import format_item_line

def export_to_text_file(items: list | dict, output_filepath: str, playlist_title: str = "YouTube Playlist"):
    """
    Exports playlist items to a plain text file.

    Args:
        items (list): A list of playlist item dictionaries (from YouTube API).
        output_filepath (str): The path to the output text file (e.g., "playlist.txt").
    """
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(playlist_title)
            f.write('\n\n')
            for item in items:
                line = format_item_line(item)
                f.write(line + '\n')
            print(f"Successfully exported playlist to text file: {output_filepath}")
    except IOError as e:
            print(f"Error during the export of textfile {output_filepath}: {e}")
    