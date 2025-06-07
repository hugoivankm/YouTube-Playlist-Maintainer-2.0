from fpdf import FPDF
from playlist_maintainer.application_interfaces.exporters.exporter_utils import format_item_line
import sys
import os

def export_to_pdf(items: list, output_filepath: str, playlist_title: str = "YouTube Playlist"):
    """
    Exports playlist items to a PDF file.

    Args:
        items (list): A list of PlaylistItem
        output_filepath (str): The path to the output PDF file (e.g., "playlist.pdf").
        playlist_title (str): The title of the playlist to display in the PDF header.
    """   
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    regular_font_filename = "NotoSansJP-Regular.ttf"
    bold_font_filename = "NotoSansJP-Bold.ttf"
    
    base_font_dir = os.path.join(os.getcwd(), "assets", "fonts", "Noto_Sans_JP", "static")
    
    font_regular_path = os.path.join(base_font_dir, regular_font_filename)
    font_bold_path = os.path.join(base_font_dir, bold_font_filename)
    
    if not os.path.exists(font_regular_path):
        print(f"ERROR: Font file not found at: {font_regular_path}") 
        print(f"Please ensure '{regular_font_filename}' is in '{os.path.relpath(base_font_dir, os.getcwd())}'")
        sys.exit(1)
    if not os.path.exists(font_bold_path):
        print(f"ERROR: Font file not found at: {font_bold_path}")
        print(f"Please ensure '{bold_font_filename}' is in '{os.path.relpath(base_font_dir, os.getcwd())}'")
        sys.exit(1)
        
    try:
        pdf.add_font("NotoSansJP", "", font_regular_path) 
        pdf.add_font("NotoSansJP", "B", font_bold_path)
        pdf.set_font("NotoSansJP", 'B', 16) 
    except Exception as font_e:
        print(f"ERROR: Could not load font 'Noto Sans JP' from '{regular_font_filename}': {font_e}")
        print("File might be corrupted or not a valid TTF.")
        sys.exit(1)
    
    pdf.cell(0, 10, txt=playlist_title, ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("NotoSansJP", size=10)
    
    items_per_page = 100
    try:
        for i, item in enumerate(items):
            if i > 0 and i % items_per_page == 0:
                pdf.add_page()
            line_text = format_item_line(item)
            pdf.multi_cell(0, 5, txt=line_text, ln=1)
        output_filepath_resolved = os.path.join(os.getcwd(), output_filepath)
        pdf.output(output_filepath_resolved, 'F')
        print(f"Successfully exported playlist to PDF file: {output_filepath}")
    except Exception as e:
        print(f"Error generating PDF file {output_filepath}: {e}")