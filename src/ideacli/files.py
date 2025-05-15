# src/ideacli/files.py

from ideacli.repository import resolve_idea_path
import json
import os
import sys

def list_files(args):
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file) as f:
        idea = json.load(f)

    response = idea.get("response", {})
    files = []
    
    # Check for top-level "files" array first
    if "files" in response:
        for file_entry in response.get("files", []):
            file_name = file_entry.get("name")
            if file_name:
                files.append(file_name)
    
    # Also check for files in the traditional approach.code_samples structure
    for approach in response.get("approaches", []):
        for sample in approach.get("code_samples", []):
            file_name = sample.get("file")
            if file_name and file_name not in files:
                files.append(file_name)

    if files:
        print("\n".join(files))
    else:
        print("No files found in idea response.")

def extract_files(args):
    """Extract code samples into real files."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    idea_file = os.path.join(conversation_dir, f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"Error: No conversation found with ID '{args.id}'")
        sys.exit(1)

    with open(idea_file) as f:
        idea = json.load(f)

    response = idea.get("response", {})
    extracted = False

    # Extract from top-level "files" array
    for file_entry in response.get("files", []):
        file_name = file_entry.get("name")
        content = file_entry.get("content")
        
        if file_name and content:
            dir_name = os.path.dirname(file_name)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            with open(file_name, "w") as out_file:
                out_file.write(content)

            print(f"Wrote {file_name}")
            extracted = True

    # Also extract from the traditional approach.code_samples structure
    for approach in response.get("approaches", []):
        for sample in approach.get("code_samples", []):
            file_path = sample.get("file")
            code = sample.get("code")
            if file_path and code:
                dir_name = os.path.dirname(file_path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(file_path, "w") as out_file:
                    out_file.write(code)

                print(f"Wrote {file_path}")
                extracted = True
    
    if not extracted:
        print("No files found to extract.")
