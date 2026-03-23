#!/usr/bin/env python3
"""
Add video links to the top of all readme.md files in the notes directory.
"""

import os
import re
from pathlib import Path

def normalize_name(name):
    """Normalize folder name for matching."""
    # Remove numbers, dashes, convert to lowercase
    normalized = re.sub(r'^\d+-\d+-', '', name)
    normalized = normalized.replace('-', ' ').lower()
    return normalized.strip()

def find_matching_video_folder(note_folder, video_base_path):
    """Find the matching video folder for a note folder."""
    # Exact mappings for specific folders
    exact_mappings = {
        '03-05-io': 'Chapter_17_03-05 Input - Output',
        '09-02-glob-options': 'Chapter_41_09-02 Glob Shell Options',
        '16-00-pitfall-ls-list': 'Chapter_59_16-00 Pitfall- ls',
        '16-02-ansi-length': 'Chapter_61_16-02 Pitfall- String Length',
    }

    # Check exact mapping first
    if note_folder in exact_mappings:
        exact_folder = video_base_path / exact_mappings[note_folder]
        if exact_folder.exists():
            return exact_folder

    note_normalized = normalize_name(note_folder)

    # Special case mappings for differences between note and video names
    mappings = {
        'intro': 'introduction',
        'pager': 'paging files',
        'more variables': 'basic variables',
        'actually scripting': 'finally scripting',
        'taking input': 'user input',
        'io': 'input   output',  # Note: triple space in video name
        'what we have': 'chapter',
        'cut tr': 'cut and tr',
        'sed awk grep': 'sed, awk, and grep',
        'find cmd': 'find command',
        'pipestatus': 'pipe status',
        'timing': 'timing commands',
        'sourcing': 'sourcing code',
        'curlies vs parens': 'curlies vs. parens',
        'return vs output': 'return vs. output',
        'array expansion chars': 'array expansion',
        'brace string expansion': 'brace expansion',
        'braces numeric': 'numeric brace expansion',
        'printf': 'understanding printf',
        'regex': 'regular expressions',
        'mapfile readarray': 'using mapfile',
        'test vs bracket': 'brackets vs. test',
        'isatty': 'is a tty',
        'interactive ps1': 'ps1 variable',
        'customize bashrc': 'customizing bash',
        'readline and such': 'readline shortcuts',
        'pitfall ls list': 'pitfall  ls',  # Note: double space
        'ansi length': 'pitfall  string length',  # Note: double space
        'glob options': 'glob shell options',
    }

    # Apply mapping if exists
    search_name = mappings.get(note_normalized, note_normalized)

    # Search through video folders
    for video_folder in sorted(video_base_path.iterdir()):
        if not video_folder.is_dir() or not video_folder.name.startswith('Chapter_'):
            continue

        video_name = video_folder.name
        # Extract the part after Chapter_XX_
        video_title = re.sub(r'^Chapter_\d+_\d+-\d+ ', '', video_name).lower()

        if search_name in video_title or video_title in search_name:
            return video_folder

    return None

def get_video_file_path(video_folder):
    """Get the relative path to the video file."""
    # Find the .mp4 file in the folder
    mp4_files = list(video_folder.glob('*.mp4'))
    if mp4_files:
        return mp4_files[0]
    return None

def add_video_link_to_readme(readme_path, video_path):
    """Add video link to the top of readme.md file."""
    # Read existing content
    with open(readme_path, 'r') as f:
        content = f.read()

    # Check if video link already exists
    if '## 📹 Video' in content or 'videos/' in content:
        print(f"  ⚠️  Video link already exists, skipping")
        return False

    # Create relative path from notes folder to video
    # notes/XX-XX-name/readme.md -> ../../videos/Chapter_XX/video.mp4
    relative_video_path = os.path.relpath(video_path, readme_path.parent)

    # Create video link section
    video_section = f"## 📹 Video\n\n[Watch this chapter]({relative_video_path})\n\n---\n\n"

    # Add to top of file
    new_content = video_section + content

    # Write back
    with open(readme_path, 'w') as f:
        f.write(new_content)

    return True

def main():
    base_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course')
    notes_path = base_path / 'notes'
    videos_path = base_path / 'videos'

    if not videos_path.exists():
        print(f"Error: Videos directory not found: {videos_path}")
        return

    print("Adding video links to readme files...\n")

    updated_count = 0
    skipped_count = 0
    not_found_count = 0

    # Process each note folder
    note_folders = sorted([f for f in notes_path.iterdir() if f.is_dir() and re.match(r'^\d+-\d+-', f.name)])

    for note_folder in note_folders:
        readme_path = note_folder / 'readme.md'

        if not readme_path.exists():
            print(f"❌ {note_folder.name}: No readme.md found")
            not_found_count += 1
            continue

        print(f"Processing: {note_folder.name}")

        # Find matching video folder
        video_folder = find_matching_video_folder(note_folder.name, videos_path)

        if not video_folder:
            print(f"  ❌ No matching video folder found")
            not_found_count += 1
            continue

        # Get video file path
        video_file = get_video_file_path(video_folder)

        if not video_file:
            print(f"  ❌ No video file found in {video_folder.name}")
            not_found_count += 1
            continue

        print(f"  ✓ Matched with: {video_folder.name}")
        print(f"    Video: {video_file.name}")

        # Add video link to readme
        if add_video_link_to_readme(readme_path, video_file):
            print(f"  ✓ Added video link")
            updated_count += 1
        else:
            skipped_count += 1

    print("\n" + "="*60)
    print(f"Summary:")
    print(f"  ✓ Updated: {updated_count}")
    print(f"  ⚠️  Skipped (already exists): {skipped_count}")
    print(f"  ❌ Not found/No match: {not_found_count}")
    print(f"  Total processed: {len(note_folders)}")
    print("="*60)

if __name__ == '__main__':
    main()
