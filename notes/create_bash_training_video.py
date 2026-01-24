#!/usr/bin/env python3
"""
Create a NotebookLM training video from the bash course notebook.
"""

import sys
import json
import time

# Add notebooklm-api scripts to path
sys.path.insert(0, "/Users/BLW_M2_HOME/.claude/skills/notebooklm-api/scripts")

from api_client import NotebookLMAPIClient
from config import (
    VIDEO_FORMAT_EXPLAINER,
    VIDEO_STYLE_CLASSIC
)

def read_notebook_content(notebook_path):
    """Read and extract text content from Jupyter notebook."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    # Extract all markdown and code cells
    content_parts = []
    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source = cell.get('source', [])

        # Join source lines
        if isinstance(source, list):
            text = ''.join(source)
        else:
            text = source

        if cell_type == 'markdown':
            content_parts.append(f"## SECTION ##\n{text}\n")
        elif cell_type == 'code':
            content_parts.append(f"```bash\n{text}\n```\n")

    return '\n'.join(content_parts)

def main():
    print("🎬 Creating Bash Training Video with NotebookLM\n")

    # Initialize client
    client = NotebookLMAPIClient()

    # Step 1: Create notebook
    print("📚 Creating NotebookLM notebook...")
    notebook = client.create_notebook("Complete Bash Course - Training Material")
    notebook_id = notebook["id"]
    print(f"✅ Created notebook: {notebook_id}\n")

    # Step 2: Read and add bash course content
    print("📖 Reading bash course notebook...")
    notebook_path = "/Users/BLW_M2_HOME/GitHub/bash-course/notes/bash-course-complete.ipynb"
    content = read_notebook_content(notebook_path)

    # Split content if too large (NotebookLM has limits)
    # Split into chunks of ~100k characters
    chunk_size = 100000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    print(f"📝 Adding {len(chunks)} content chunk(s) to notebook...")
    for i, chunk in enumerate(chunks, 1):
        client.add_text_source(
            notebook_id,
            chunk,
            f"Bash Course - Part {i}/{len(chunks)}"
        )
        print(f"  ✅ Added Part {i}/{len(chunks)}")

    # Get source IDs from notebook
    print("\n📋 Fetching source IDs...")
    notebook_data = client.get_notebook(notebook_id)
    source_ids = notebook_data.get("source_ids", [])
    print(f"  ✅ Found {len(source_ids)} sources")
    print()

    # Step 3: Get notebook summary
    print("🤖 Generating AI summary...")
    summary = client.get_notebook_summary(notebook_id)
    print(f"Summary: {summary.get('summary', 'N/A')[:200]}...")
    print()

    # Step 4: Create video overview
    print("🎥 Creating training video...")
    print("   Format: Educational Explainer")
    print("   Style: Classic")
    print("   Focus: Comprehensive bash scripting course from basics to advanced")
    print()

    video = client.create_video_overview(
        notebook_id,
        format_code=VIDEO_FORMAT_EXPLAINER,
        visual_style=VIDEO_STYLE_CLASSIC,
        focus_prompt="""Create a comprehensive training video that teaches bash scripting effectively.

        Cover these key areas in order:
        1. Terminal basics and file operations
        2. Variables, functions, and conditionals
        3. Loops and control flow
        4. Text processing tools (grep, sed, awk)
        5. Advanced features (arrays, parameter expansion, globbing)
        6. Best practices and real-world examples

        Make it engaging and educational, using clear examples throughout.
        Emphasize practical applications and common use cases.
        Include tips and tricks that make learning easier.
        """,
        sources=source_ids
    )

    print("⏳ Video generation started. This may take several minutes...\n")

    # Step 5: Poll for completion
    print("📊 Checking status...")
    max_attempts = 60  # 10 minutes max
    attempt = 0

    while attempt < max_attempts:
        status = client.poll_studio_status(notebook_id)

        # Find video artifact
        video_artifact = None
        for artifact in status.get("artifacts", []):
            if artifact.get("type") == "video":
                video_artifact = artifact
                break

        if video_artifact:
            artifact_status = video_artifact.get("status", "unknown")
            print(f"   Status: {artifact_status}")

            if artifact_status == "completed":
                print("\n🎉 Video generation completed!")
                print(f"📺 Video URL: {video_artifact.get('url', 'N/A')}")
                print(f"📝 Notebook: https://notebooklm.google.com/notebook/{notebook_id}")
                break
            elif artifact_status == "failed":
                print("\n❌ Video generation failed")
                print(f"Error: {video_artifact.get('error', 'Unknown error')}")
                break

        attempt += 1
        time.sleep(10)  # Check every 10 seconds

    if attempt >= max_attempts:
        print("\n⏱️  Timeout waiting for video generation")
        print(f"Check status manually: https://notebooklm.google.com/notebook/{notebook_id}")

    print("\n" + "="*60)
    print("Summary:")
    print(f"Notebook ID: {notebook_id}")
    print(f"Notebook URL: https://notebooklm.google.com/notebook/{notebook_id}")
    print(f"Sources added: {len(source_ids)}")
    print("="*60)

if __name__ == "__main__":
    main()
