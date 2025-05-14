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
    for approach in response.get("approaches", []):
        for sample in approach.get("code_samples", []):
            files.append(sample.get("file"))

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

    for approach in response.get("approaches", []):
        for sample in approach.get("code_samples", []):
            file_path = sample.get("file")
            code = sample.get("code")
            if file_path and code:
                dir_name = os.path.dirname(file_path)
                if dir_name:  # <-- ⭐ ⭐ ⭐ this prevents the crash
                    os.makedirs(dir_name, exist_ok=True)
    
                with open(file_path, "w") as out_file:
                    out_file.write(code)
    
                print(f"Wrote {file_path}")

