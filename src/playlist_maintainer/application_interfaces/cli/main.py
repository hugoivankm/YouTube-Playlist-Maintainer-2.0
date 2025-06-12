import click
import os
import sys

from playlist_maintainer.services.playlist_service import PlaylistService
from playlist_maintainer.bootstrap import initialize_app

# ----------------------------------------------------------------------
# Main CLI Group
# ----------------------------------------------------------------------
@click.group(
    name="ytpl",
    help="A command-line tool to maintain and export YouTube playlists information.",
)
def ytpl():
    """
    The main entry point for the YouTube Playlist Maintainer CLI.
    """
    pass


# ----------------------------------------------------------------------
# 'export' Command
# ----------------------------------------------------------------------
@ytpl.command(name="export", help="Export a YouTube playlist to a file (PDF or TXT)")
@click.argument("playlist_identifier", type=str, nargs=1, metavar="PLAYLIST_IDENTIFIER")
@click.option(
    "--format",
    type=click.Choice(["pdf", "txt"], case_sensitive=False),
    default="txt",
    show_default=True,
    help="The format of the exported file",
)
@click.option(
    "--name",
    type=str,
    help='Optional: Base name for the output file (e.g., "my_playlist"). '
    "If not provided, the word playlist will be used."
    "A timestamp will always be appended to ensure uniqueness.",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default=os.path.join(os.getcwd(), "output"),
    show_default=True,
    help="Optional: Directory to save the exported file. "
    "Defaults to 'output' folder in the current working directory.",
)
@click.option(
    "--env",
    type=str,
    default=None,
    show_default=True,
    help='Specify the environment as an alphanumeric string you might also include \
         ".", "-" , "_"(e.g., "test.env", "your-env", "prod"). '
         'Overrides APP_ENV environment variable. Defaults to ".env" if neither set.'  
)
def export_command(
    playlist_identifier,
    format,
    name,
    path,
    env):
    """
    Exports a YouTube playlist to a PDF or TXT file.

    PLAYLIST_IDENTIFIER can be the YouTube playlist ID or a full playlist URL.
    """
    initialize_app(env)
    try:
        YtplService = PlaylistService()
        YtplService.export_playlist_to_file(playlist_identifier, format, name, path)
    except ValueError as ve:
        click.echo(f"Error: {ve}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


# ----------------------------------------------------------------------
# 'show' Command
# ----------------------------------------------------------------------
@ytpl.command(
    name="show", help="Display YouTube playlist items directly in the terminal"
)
@click.argument("playlist_identifier", type=str, nargs=1, metavar="PLAYLIST_IDENTIFIER")
@click.option(
    "--limit",
    type=int,
    default=20,
    show_default=True,
    help="Number of playlist items to display (default: 20).",
)
@click.option(
    "--env",
    type=str,
    default=None,
    show_default=True,
    help='Specify the environment as an alphanumeric string you might also include \
         ".", "-" , "_"(e.g., "test1", "your-env", "prod"). '
         'Overrides APP_ENV environment variable. Defaults to ".env" if neither set.'  
)
def show_command(playlist_identifier, limit, env):
    """
    Fetches and displays a YouTube playlist items directly in the terminal.

    PLAYLIST_IDENTIFIER can be the YouTube playlist ID or a full playlist URL.
    """
    initialize_app(env)
    try: 
        YtplService = PlaylistService()
        YtplService.show_playlist_in_terminal(playlist_identifier, limit)
    except ValueError as ve:
        click.echo(f"Error: {ve}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    ytpl()
