#!/usr/bin/python3

"""
markdown2html.py: A script to convert Markdown files to HTML, supporting headings.
"""

import sys
import os

def markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to an HTML file, parsing heading syntax.

    Arguments:
    input_file -- the name of the Markdown file to be converted
    output_file -- the name of the output HTML file
    """
    try:
        with open(input_file, 'r') as md_file:
            html_content = ""
            for line in md_file:
                line = line.rstrip()
                if line.startswith("#"):
                    heading_level = len(line.split()[0])
                    if 1 <= heading_level <= 6:
                        line_content = line[heading_level:].strip()
                        html_content += f"<h{heading_level}>{line_content}</h{heading_level}>\n"
                else:
                    html_content += line + "<br>\n"

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        exit(1)
    
    markdown_to_html(input_file, output_file)
    exit(0)

