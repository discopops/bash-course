#!/usr/bin/env python3
"""
Add video links to the bash-course-complete.ipynb notebook.
"""

import json
import re
from pathlib import Path

def extract_section_id(header_text):
    """Extract section ID like '01-01' or '00' from header."""
    # Try ### XX-XX: format
    match = re.search(r'###\s+(\d+-\d+):', header_text)
    if match:
        return match.group(1)

    # Try ## Section XX: format
    match = re.search(r'##\s+Section\s+(\d+):', header_text)
    if match:
        section_num = match.group(1)
        return f"{section_num}-00"

    return None

def find_video_file(section_id, videos_path):
    """Find the video file for a given section ID."""
    # Map section IDs to video chapter names
    video_map = {
        '00-00': 'Chapter_01_00-00 Introduction',
        '01-00': 'Chapter_02_01-00 Terminal and Finder',
        '01-01': 'Chapter_03_01-01 Basic File Manipulation',
        '01-02': 'Chapter_04_01-02 Hidden Files',
        '01-03': 'Chapter_05_01-03 Searching in Files',
        '01-04': 'Chapter_06_01-04 Paging Files',
        '02-00': 'Chapter_07_02-00 Man Pages',
        '02-01': 'Chapter_08_02-01 Programs and Commands',
        '02-02': 'Chapter_09_02-02 Basic Variables',
        '02-03': 'Chapter_10_02-03 vim Crash Course',
        '02-04': 'Chapter_11_02-04 File Permissions',
        '03-00': 'Chapter_12_03-00 Finally Scripting',
        '03-01': 'Chapter_13_03-01 User Input',
        '03-02': 'Chapter_14_03-02 Functions',
        '03-03': 'Chapter_15_03-03 Conditionals',
        '03-04': 'Chapter_16_03-04 For Loops',
        '03-05': 'Chapter_17_03-05 Input - Output',
        '03-06': 'Chapter_18_03-06 Chapter 3 Recap',
        '04-00': 'Chapter_19_04-00 Case Statements',
        '04-01': 'Chapter_20_04-01 Indexed Arrays',
        '04-02': 'Chapter_21_04-02 Associative Arrays',
        '04-03': 'Chapter_22_04-03 IFS Variable',
        '04-04': 'Chapter_23_04-04 Command Substitution',
        '04-05': 'Chapter_24_04-05 Arithmetic Expression',
        '04-06': 'Chapter_25_04-06 Process Substitution',
        '04-07': 'Chapter_26_04-07 Chapter 4 Recap',
        '05-00': 'Chapter_27_05-00 cut and tr',
        '05-01': 'Chapter_28_05-01 sed, awk, and grep',
        '05-02': 'Chapter_29_05-02 Find Command',
        '06-00': 'Chapter_30_06-00 Bash Arguments',
        '06-01': 'Chapter_31_06-01 Pipe Status',
        '06-02': 'Chapter_32_06-02 Timing Commands',
        '07-00': 'Chapter_33_07-00 Sourcing Code',
        '07-01': 'Chapter_34_07-01 Curlies vs. Parens',
        '07-02': 'Chapter_35_07-02 Return vs. Output',
        '07-03': 'Chapter_36_07-03 Chapter 7 Recap',
        '08-00': 'Chapter_37_08-00 Parameter Expansion',
        '08-01': 'Chapter_38_08-01 Array Expansion',
        '09-00': 'Chapter_39_09-00 Basic Globbing',
        '09-01': 'Chapter_40_09-01 Extended Globbing',
        '09-02': 'Chapter_41_09-02 Glob Shell Options',
        '10-00': 'Chapter_42_10-00 Brace Expansion',
        '10-01': 'Chapter_43_10-01 Braces and Globbing',
        '10-02': 'Chapter_44_10-02 Numeric Brace Expansion',
        '11-00': 'Chapter_45_11-00 Understanding printf',
        '11-01': 'Chapter_46_11-01 Date Formatting',
        '11-02': 'Chapter_47_11-02 Regular Expressions',
        '11-03': 'Chapter_48_11-03 Using mapfile',
        '12-00': 'Chapter_49_12-00 Brackets vs. Test',
        '12-01': 'Chapter_50_12-01 Special Strings',
        '13-00': 'Chapter_51_13-00 Trap Signals',
        '13-01': 'Chapter_52_13-01 Named Pipes',
        '14-00': 'Chapter_53_14-00 Color Output',
        '14-01': 'Chapter_54_14-01 Cursor Commands',
        '14-02': 'Chapter_55_14-02 Is a TTY',
        '15-00': 'Chapter_56_15-00 PS1 Variable',
        '15-01': 'Chapter_57_15-01 Customizing Bash',
        '15-02': 'Chapter_58_15-02 Readline Shortcuts',
        '16-00': 'Chapter_59_16-00 Pitfall- ls',
        '16-01': 'Chapter_60_16-01 Aliases with Arguments',
        '16-02': 'Chapter_61_16-02 Pitfall- String Length',
        '17-00': 'Chapter_62_17-00 Forkbomb',
    }

    if section_id not in video_map:
        return None

    video_folder = videos_path / video_map[section_id]
    if not video_folder.exists():
        return None

    # Find the .mp4 file in the folder
    mp4_files = list(video_folder.glob('*.mp4'))
    if mp4_files:
        return mp4_files[0]

    return None

def create_video_cell(video_path):
    """Create a markdown cell with video link."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "\n",
            f"**📹 [Watch this section video]({video_path})**\n",
            "\n",
            "---"
        ]
    }

def process_notebook(notebook_path, videos_path):
    """Add video links to notebook sections."""
    print(f"Processing notebook: {notebook_path}")
    print(f"Videos directory: {videos_path}\n")

    # Load notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    new_cells = []
    added_count = 0
    skipped_count = 0

    i = 0
    while i < len(cells):
        cell = cells[i]
        new_cells.append(cell)

        # Check if this is a section header
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])
            first_line = source.strip().split('\n')[0] if source.strip() else ''

            # Check if it's a section header
            if re.match(r'###?\s+\d+-\d+:', first_line) or re.match(r'##\s+Section\s+\d+:', first_line):
                section_id = extract_section_id(first_line)

                if section_id:
                    print(f"Found section: {first_line}")

                    # Check if next cell is already a video link
                    if i + 1 < len(cells):
                        next_cell = cells[i + 1]
                        if next_cell['cell_type'] == 'markdown':
                            next_source = ''.join(next_cell['source'])
                            if '📹' in next_source or 'Watch this section video' in next_source:
                                print(f"  ⚠️  Video link already exists, skipping\n")
                                skipped_count += 1
                                i += 1
                                continue

                    # Find video file
                    video_file = find_video_file(section_id, videos_path)

                    if video_file:
                        # Create relative path
                        relative_path = f"../videos/{video_file.parent.name}/{video_file.name}"
                        print(f"  ✓ Adding video link: {relative_path}\n")

                        # Insert video cell
                        video_cell = create_video_cell(relative_path)
                        new_cells.append(video_cell)
                        added_count += 1
                    else:
                        print(f"  ❌ No video found for section {section_id}\n")

        i += 1

    # Update notebook with new cells
    notebook['cells'] = new_cells

    # Save notebook
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)

    print("="*60)
    print(f"Summary:")
    print(f"  ✓ Video links added: {added_count}")
    print(f"  ⚠️  Skipped (already exists): {skipped_count}")
    print(f"  Total cells in notebook: {len(new_cells)}")
    print("="*60)

def main():
    base_path = Path('/Users/BLW_M2_HOME/GitHub/bash-course')
    notebook_path = base_path / 'notes' / 'bash-course-complete.ipynb'
    videos_path = base_path / 'videos'

    if not notebook_path.exists():
        print(f"Error: Notebook not found: {notebook_path}")
        return

    if not videos_path.exists():
        print(f"Error: Videos directory not found: {videos_path}")
        return

    process_notebook(notebook_path, videos_path)

if __name__ == '__main__':
    main()
