#!/usr/bin/python3
"""
markdown2html.py: A script to convert Markdown files to HTML with support for headings,
unordered lists, ordered lists, paragraphs, bold and emphasized text, and specific syntax processing.
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print("Missing {}".format(input_file), file=sys.stderr)
        sys.exit(1)

    html_lines = []
    with open(input_file, encoding="utf-8") as f:
        in_list = False
        for line in f:
            line = line.rstrip()

            # Check for Markdown headings
            match = re.match(r"^(#+) (.*)$", line)
            if match:
                heading_level = len(match.group(1))
                heading_text = match.group(2)
                html_lines.append("<h{0}>{1}</h{0}>".format(heading_level, heading_text))
                continue
            
            # Check for unordered lists
            if line.startswith("- "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append("<li>{}</li>".format(line[2:]))
                continue
            
            # Check for ordered lists
            if line.startswith("* "):
                if not in_list:
                    html_lines.append("<ol>")
                    in_list = True
                html_lines.append("<li>{}</li>".format(line[2:]))
                continue

            # Close list if the current line is empty
            if in_list and not line:
                html_lines.append("</ul>" if line.startswith("- ") else "</ol>")
                in_list = False

            # Handle paragraph and other text
            if line:
                line = parse_special_syntax(line)
                html_lines.append("<p>{}</p>".format(line))
            elif in_list:
                html_lines.append("</ul>" if line.startswith("- ") else "</ol>")
                in_list = False

    # Close any unclosed list at the end
    if in_list:
        html_lines.append("</ul>" if line.startswith("- ") else "</ol>")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

def parse_special_syntax(line):
    """
    Parse special syntax for bold, emphasized text, MD5 conversion, and character removal.
    """
    # Convert bold and emphasis
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    # Process MD5
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)

    # Remove 'c' characters from text in parentheses
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)

    return line

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)

    sys.exit(0)

