"""File operations for importing external files into ideas."""

import json
import os
import sys
from pathlib import Path
from ideacli.repository import resolve_idea_path


def import_idea(args):
    """Import a file into an idea's JSON representation."""
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Source file {args.source} does not exist")
        sys.exit(1)

    # Read the source file content
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            file_content = source_file.read()
    except Exception as e:
        print(f"Error reading source file: {e}")
        sys.exit(1)

    # Read the idea file
    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    # Determine destination filename - simple approach
    # Always use just the filename by default, unless destination is specified
    dest_filename = args.destination if args.destination else source_path.name

    # Initialize files dictionary if it doesn't exist
    if "files" not in idea:
        idea["files"] = {}
    
    # Check if file already exists in any location
    file_exists = False
    
    # Check in the root-level "files" dictionary
    if dest_filename in idea["files"]:
        file_exists = True
    
    # Also check in the response["files"] dictionary if it exists
    if "response" in idea and "files" in idea["response"]:
        if isinstance(idea["response"]["files"], dict) and dest_filename in idea["response"]["files"]:
            file_exists = True
    
    # Handle existing file
    if file_exists and not args.force:
        print(f"File {dest_filename} already exists in idea {args.id}. Use --force to overwrite.")
        sys.exit(1)
    
    # Store the file content in the idea JSON
    idea["files"][dest_filename] = file_content
    
    # Write back the updated idea JSON
    try:
        with open(idea_file, 'w', encoding='utf-8') as f:
            json.dump(idea, f, indent=2)
        print(f"Imported {args.source} as {dest_filename} into idea {args.id}")
    except Exception as e:
        print(f"Error updating idea file: {e}")
        sys.exit(1)

    return True
