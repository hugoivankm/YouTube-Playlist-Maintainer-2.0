from playlist_maintainer.application_interfaces.file_exporters.exporter_utils import format_item_line

def export_to_text(items: list, output_filepath: str):
    """
    Exports playlist items to a plain text file.

    Args:
        items (list): A list of playlist item dictionaries (from YouTube API).
        output_filepath (str): The path to the output text file (e.g., "playlist.txt").
    """
    
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(format_item_line(item) + '\n')
            print(f"Successfully exported playlist to text file: {output_filepath}")
    except IOError as e:
            print(f"Error during the export of textfile {output_filepath}: {e}")
    