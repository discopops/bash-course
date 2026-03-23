#!/usr/bin/env python3
"""
Compress all video files to about 1/3 of their current size.
"""

import subprocess
from pathlib import Path
import shutil

def get_video_size(video_path):
    """Get the size of a video file in MB."""
    return video_path.stat().st_size / (1024 * 1024)

def compress_video(input_path, output_path):
    """
    Compress video using ffmpeg with CRF 28 (good quality, smaller size).
    Target is about 1/3 of original size.
    """
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-c:v', 'libx264',           # H.264 codec
        '-crf', '28',                # Constant Rate Factor (23=default, 28=smaller)
        '-preset', 'medium',         # Encoding speed/compression tradeoff
        '-c:a', 'aac',               # Audio codec
        '-b:a', '96k',               # Audio bitrate (reduced from default)
        '-movflags', '+faststart',   # Web optimization
        '-y',                        # Overwrite output
        str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    videos_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course/videos')

    print("Compressing all videos to ~1/3 size...\n")
    print("This will take a while (processing ~1.9GB of video)...\n")

    total_original_size = 0
    total_compressed_size = 0
    processed_count = 0
    failed_count = 0

    # Process each chapter folder
    for chapter_folder in sorted(videos_path.iterdir()):
        if not chapter_folder.is_dir() or not chapter_folder.name.startswith('Chapter_'):
            continue

        # Find video file
        video_files = list(chapter_folder.glob('*.mp4'))

        if not video_files:
            continue

        video_file = video_files[0]
        original_size = get_video_size(video_file)

        # Create temporary output file
        temp_output = video_file.parent / f"temp_{video_file.name}"

        print(f"Processing: {chapter_folder.name}")
        print(f"  Original: {original_size:.1f} MB")

        # Compress video
        if compress_video(video_file, temp_output):
            compressed_size = get_video_size(temp_output)
            compression_ratio = (compressed_size / original_size) * 100

            print(f"  Compressed: {compressed_size:.1f} MB ({compression_ratio:.1f}% of original)")

            # Replace original with compressed version
            video_file.unlink()  # Delete original
            temp_output.rename(video_file)  # Rename temp to original name

            total_original_size += original_size
            total_compressed_size += compressed_size
            processed_count += 1
            print(f"  ✓ Success\n")
        else:
            print(f"  ✗ Failed to compress\n")
            if temp_output.exists():
                temp_output.unlink()
            failed_count += 1

    print("="*60)
    print(f"Compression Summary:")
    print(f"  Videos processed: {processed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Original total size: {total_original_size/1024:.2f} GB")
    print(f"  Compressed total size: {total_compressed_size/1024:.2f} GB")
    print(f"  Space saved: {(total_original_size - total_compressed_size)/1024:.2f} GB")
    print(f"  Compression ratio: {(total_compressed_size/total_original_size)*100:.1f}%")
    print("="*60)

if __name__ == '__main__':
    main()
