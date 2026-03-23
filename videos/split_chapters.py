#!/usr/bin/env python3
"""
Split YouTube video into chapters based on timestamps.
"""

import json
import subprocess
import os
import sys
from pathlib import Path

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename.strip()

def get_chapters(video_url):
    """Extract chapter information from YouTube video."""
    cmd = ['yt-dlp', '--dump-json', video_url]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return data.get('chapters', []), data.get('title', 'Unknown')

def split_video(input_file, chapters, output_dir):
    """Split video into chapters using ffmpeg."""
    print(f"\nSplitting video into {len(chapters)} chapters...")

    for i, chapter in enumerate(chapters, 1):
        chapter_title = sanitize_filename(chapter['title'])
        start_time = chapter['start_time']
        end_time = chapter['end_time']
        duration = end_time - start_time

        # Create chapter folder
        chapter_folder = output_dir / f"Chapter_{i:02d}_{chapter_title}"
        chapter_folder.mkdir(exist_ok=True)

        # Output filename
        output_file = chapter_folder / f"{chapter_title}.mp4"

        print(f"\n[{i}/{len(chapters)}] Processing: {chapter_title}")
        print(f"  Duration: {duration:.1f}s ({start_time:.1f}s - {end_time:.1f}s)")

        # FFmpeg command to extract chapter
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-ss', str(start_time),
            '-t', str(duration),
            '-c', 'copy',  # Copy without re-encoding (faster)
            '-avoid_negative_ts', '1',
            '-y',  # Overwrite output file
            str(output_file)
        ]

        # Run ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print(f"  ✓ Saved: {output_file.name} ({file_size:.1f} MB)")
        else:
            print(f"  ✗ Error processing chapter: {chapter_title}")
            print(f"    {result.stderr[:200]}")

def main():
    video_url = "https://youtube.com/watch?v=Sx9zG7wa4FA"
    base_dir = Path.home() / "Desktop" / "Bash_Scripting_Course"
    input_file = base_dir / "full_video.mp4"

    # Check if video file exists
    if not input_file.exists():
        print(f"Error: Video file not found: {input_file}")
        sys.exit(1)

    print("Extracting chapter information...")
    chapters, video_title = get_chapters(video_url)

    if not chapters:
        print("No chapters found in video!")
        sys.exit(1)

    print(f"\nVideo: {video_title}")
    print(f"Total chapters: {len(chapters)}")
    print(f"Input file: {input_file}")
    print(f"Output directory: {base_dir}")

    # Split video
    split_video(input_file, chapters, base_dir)

    print("\n" + "="*60)
    print("✓ All chapters processed successfully!")
    print(f"✓ Output location: {base_dir}")
    print("="*60)

if __name__ == '__main__':
    main()
