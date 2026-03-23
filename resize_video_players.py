#!/usr/bin/env python3
"""
Make video players smaller in the notebook - better for VS Code viewing.
"""

import json
import re
from pathlib import Path

def create_smaller_video_cell(video_path, thumbnail_path):
    """Create a markdown cell with smaller video player."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "\n",
            "<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0; max-width: 500px;'>\n",
            "  <p style='margin: 0 0 8px 0; font-weight: bold; color: #2c3e50;'>📹 Video for this section</p>\n",
            f"  <video width='480' controls poster='{thumbnail_path}'>\n",
            f"    <source src='{video_path}' type='video/mp4'>\n",
            "    Your browser does not support the video tag.\n",
            "  </video>\n",
            f"  <p style='margin: 5px 0 0 0; font-size: 0.85em;'><a href='{video_path}' target='_blank'>Open in new window</a></p>\n",
            "</div>\n",
            "\n",
            "---"
        ]
    }

def process_notebook(notebook_path):
    """Update video player cells to be smaller."""
    print(f"Resizing video players in: {notebook_path}\n")

    # Load notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    updated_count = 0

    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])

            # Find video player cells
            if '<video' in source and 'width=\'100%\'' in source:
                # Extract video and thumbnail paths
                video_match = re.search(r'<source src=\'([^\']+)\'', source)
                thumbnail_match = re.search(r'poster=\'([^\']+)\'', source)

                if video_match and thumbnail_match:
                    video_path = video_match.group(1)
                    thumbnail_path = thumbnail_match.group(1)

                    # Create new smaller cell
                    new_cell = create_smaller_video_cell(video_path, thumbnail_path)
                    cells[i] = new_cell
                    updated_count += 1

                    print(f"✓ Updated cell {i}")

    # Update notebook
    notebook['cells'] = cells

    # Save
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  ✓ Video players resized: {updated_count}")
    print(f"  New size: 480px wide (instead of 100% width)")
    print(f"{'='*60}")

def main():
    notebook_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course/notes/bash-course-complete.ipynb')

    if not notebook_path.exists():
        print(f"Error: Notebook not found: {notebook_path}")
        return

    process_notebook(notebook_path)

if __name__ == '__main__':
    main()
