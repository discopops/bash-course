#!/usr/bin/env python3
"""
Generate thumbnails and embed video players in the notebook.
"""

import json
import subprocess
from pathlib import Path

def generate_thumbnail(video_path, thumbnail_path, timestamp="00:00:02"):
    """Generate a thumbnail from a video at the specified timestamp."""
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-ss', timestamp,
        '-vframes', '1',
        '-vf', 'scale=640:-1',  # Width 640, maintain aspect ratio
        '-y',  # Overwrite
        str(thumbnail_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def create_video_player_cell(video_path, thumbnail_path):
    """Create a markdown cell with embedded video player and thumbnail."""
    # Create relative paths for the notebook
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "\n",
            "<div style='background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin: 10px 0;'>\n",
            "  <h3 style='margin-top: 0; color: #2c3e50;'>📹 Video for this section</h3>\n",
            f"  <video width='100%' controls poster='{thumbnail_path}'>\n",
            f"    <source src='{video_path}' type='video/mp4'>\n",
            "    Your browser does not support the video tag.\n",
            "  </video>\n",
            f"  <p style='margin-bottom: 0; font-size: 0.9em; color: #7f8c8d;'><a href='{video_path}' target='_blank'>Open video in new window</a></p>\n",
            "</div>\n",
            "\n",
            "---"
        ]
    }

def process_notebook_with_videos(notebook_path, videos_path, thumbnails_path):
    """Add video players with thumbnails to notebook."""
    print(f"Processing notebook: {notebook_path}")
    print(f"Videos directory: {videos_path}")
    print(f"Thumbnails directory: {thumbnails_path}\n")

    # Create thumbnails directory
    thumbnails_path.mkdir(exist_ok=True)

    # Load notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    new_cells = []
    updated_count = 0
    thumbnail_count = 0

    i = 0
    while i < len(cells):
        cell = cells[i]

        # Check if this is a video link cell (the ones we added before)
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])

            # If it's an old video link cell, replace it
            if '📹' in source and 'Watch this section video' in source:
                # Extract the video path from the link
                import re
                match = re.search(r'\((\.\./videos/[^)]+\.mp4)\)', source)

                if match:
                    video_path = match.group(1)
                    # Get the video filename to create thumbnail name
                    video_name = Path(video_path).stem
                    chapter_folder = Path(video_path).parent.name

                    # Create safe thumbnail filename
                    thumbnail_filename = f"{chapter_folder}.jpg"
                    thumbnail_path = thumbnails_path / thumbnail_filename
                    thumbnail_rel_path = f"../thumbnails/{thumbnail_filename}"

                    # Generate thumbnail if it doesn't exist
                    full_video_path = notebook_path.parent / video_path.replace('../', '')

                    if not thumbnail_path.exists() and full_video_path.exists():
                        print(f"Generating thumbnail: {thumbnail_filename}")
                        if generate_thumbnail(full_video_path, thumbnail_path):
                            print(f"  ✓ Created thumbnail")
                            thumbnail_count += 1
                        else:
                            print(f"  ⚠️  Failed to create thumbnail")

                    # Create new video player cell
                    video_cell = create_video_player_cell(video_path, thumbnail_rel_path)
                    new_cells.append(video_cell)
                    updated_count += 1
                    print(f"  ✓ Updated cell {i} with video player\n")
                else:
                    # Keep the cell as is
                    new_cells.append(cell)
            else:
                # Not a video cell, keep as is
                new_cells.append(cell)
        else:
            # Not markdown, keep as is
            new_cells.append(cell)

        i += 1

    # Update notebook
    notebook['cells'] = new_cells

    # Save notebook
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)

    print("="*60)
    print(f"Summary:")
    print(f"  ✓ Video players embedded: {updated_count}")
    print(f"  ✓ Thumbnails generated: {thumbnail_count}")
    print(f"  Total cells in notebook: {len(new_cells)}")
    print("="*60)

def main():
    base_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course')
    notebook_path = base_path / 'notes' / 'bash-course-complete.ipynb'
    videos_path = base_path / 'videos'
    thumbnails_path = base_path / 'thumbnails'

    if not notebook_path.exists():
        print(f"Error: Notebook not found: {notebook_path}")
        return

    if not videos_path.exists():
        print(f"Error: Videos directory not found: {videos_path}")
        return

    process_notebook_with_videos(notebook_path, videos_path, thumbnails_path)
    print(f"\n✓ Thumbnails saved to: {thumbnails_path}")

if __name__ == '__main__':
    main()
