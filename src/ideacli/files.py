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

    # Check if "files" exists directly in the response
    if "files" in response:
        files_data = response.get("files", {})
        # Check if files is a dictionary (keys as filenames)
        if isinstance(files_data, dict):
            for filename, content in files_data.items():
                files.append(filename)
        # Check if files is a list of objects with "name" field
        elif isinstance(files_data, list):
            for file_entry in files_data:
                if isinstance(file_entry, dict):
                    file_name = file_entry.get("name")
                    if file_name:
                        files.append(file_name)

    # Also check traditional approach.code_samples format
    for approach in response.get("approaches", []):
        if isinstance(approach, dict):  # Handle approach as dictionary
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

    # Check if "files" exists directly in the response
    if "files" in response:
        files_data = response.get("files", {})
        # Check if files is a dictionary (keys as filenames)
        if isinstance(files_data, dict):
            for filename, content in files_data.items():
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(filename, "w") as out_file:
                    out_file.write(content)

                print(f"Wrote {filename}")
                extracted = True
        # Check if files is a list of objects with "name" and "content" fields
        elif isinstance(files_data, list):
            for file_entry in files_data:
                if isinstance(file_entry, dict):
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

    # Also handle the traditional approach.code_samples format
    for approach in response.get("approaches", []):
        if isinstance(approach, dict):  # Handle approach as dictionary
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
