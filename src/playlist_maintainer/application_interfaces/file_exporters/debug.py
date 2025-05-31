# debug_fpdf_issue.py

from fpdf import FPDF
import sys

def debug_fpdf_multi_cell():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10) # Ensure you use the same font settings as your main code

    print("--- Starting FPDF multi_cell debugging ---")

    # *************************************************************************
    # *** IMPORTANT: REPLACE THIS LIST WITH YOUR ACTUAL PROBLEM DATA ***
    # *************************************************************************
    # Add a few lines that work, then the specific line that caused the failure.
    # Example:
    test_lines = [
        "0. Kore wa zombie desu ka (Full OP)",
        "1. Kill la Kill Opening 2",
        # Replace the next line with the EXACT problematic 'line_text' you identified
        # from your full script's debug output (the line before termination).
        # "3. THIS IS THE PROBLEMATIC LINE OF TEXT THAT CAUSED THE ISSUE. COPY ITS EXACT CONTENT HERE.",
        "4. A line that should appear after the problematic one (if it runs).",
    ]

    for i, line_text in enumerate(test_lines):
        print(f"\n--- Debugging line {i+1} ---")
        print(f"Content: '{line_text}' (Length: {len(line_text)})")

        # Additional checks for problematic characters (useful for fpdf2)
        if not line_text.isprintable():
            print(f"WARNING: Line {i+1} contains non-printable characters. This can cause issues with fpdf2.")
            # You might try sanitizing the string here to see if it helps:
            # line_text = ''.join(c for c in line_text if c.isprintable() or c in ('\n', '\t', '\r'))
            # print(f"  Sanitized content (if applied): '{line_text}'")

        try:
            print(f"Attempting pdf.multi_cell() for line {i+1}...")
            pdf.multi_cell(0, 5, txt=line_text)
            print(f"SUCCESS: Line {i+1} added to PDF.")
        except Exception as e:
            print(f"ERROR: EXCEPTION CAUGHT during multi_cell for line {i+1}: {e}")
            print(f"Problematic content was: '{line_text}'")
            sys.exit(1) # Exit immediately to show the error

        sys.stdout.flush() # Ensure prints appear immediately

    output_file = "debug_output.pdf"
    try:
        print(f"\n--- Attempting to save PDF to {output_file} ---")
        pdf.output(output_file)
        print("PDF saved successfully.")
    except Exception as e:
        print(f"ERROR: Exception caught during pdf.output: {e}")
        sys.exit(1)

if __name__ == "__main__":
    debug_fpdf_multi_cell()