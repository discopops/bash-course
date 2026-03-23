#!/usr/bin/env python3
"""
Generate thumbnails for all video files.
"""

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

def main():
    videos_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course/videos')
    thumbnails_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course/thumbnails')

    thumbnails_path.mkdir(exist_ok=True)

    print("Generating thumbnails for all videos...\n")

    success_count = 0
    fail_count = 0

    # Process each chapter folder
    for chapter_folder in sorted(videos_path.iterdir()):
        if not chapter_folder.is_dir() or not chapter_folder.name.startswith('Chapter_'):
            continue

        # Find video file
        video_files = list(chapter_folder.glob('*.mp4'))

        if not video_files:
            print(f"⚠️  No video found in {chapter_folder.name}")
            continue

        video_file = video_files[0]
        thumbnail_filename = f"{chapter_folder.name}.jpg"
        thumbnail_path = thumbnails_path / thumbnail_filename

        if thumbnail_path.exists():
            print(f"✓ Thumbnail already exists: {thumbnail_filename}")
            success_count += 1
            continue

        print(f"Generating: {thumbnail_filename}")

        if generate_thumbnail(video_file, thumbnail_path):
            file_size = thumbnail_path.stat().st_size / 1024  # KB
            print(f"  ✓ Created ({file_size:.1f} KB)\n")
            success_count += 1
        else:
            print(f"  ✗ Failed\n")
            fail_count += 1

    print("="*60)
    print(f"Summary:")
    print(f"  ✓ Success: {success_count}")
    print(f"  ✗ Failed: {fail_count}")
    print(f"  Total: {success_count + fail_count}")
    print(f"\n✓ Thumbnails saved to: {thumbnails_path}")
    print("="*60)

if __name__ == '__main__':
    main()
