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

    # First, check for files in response
    if "files" in response:
        files_data = response["files"]
        if isinstance(files_data, dict):
            for filename in files_data.keys():
                files.append(filename)

    # ALSO check for files at the root level (this is the key addition)
    if "files" in idea:
        files_data = idea["files"]
        if isinstance(files_data, dict):
            for filename in files_data.keys():
                files.append(filename)

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

    # Process files from the "files" field in response
    if "files" in response:
        files_data = response.get("files", {})
        if isinstance(files_data, dict):
            for filename, content in files_data.items():
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(filename, "w") as out_file:
                    out_file.write(content)

                print(f"Wrote {filename}")
                extracted = True
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

    # NEW: Also process files from the root level "files" field
    if "files" in idea:
        files_data = idea.get("files", {})
        if isinstance(files_data, dict):
            for filename, content in files_data.items():
                dir_name = os.path.dirname(filename)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(filename, "w") as out_file:
                    out_file.write(content)

                print(f"Wrote {filename}")
                extracted = True
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

    # Handle the traditional approach.code_samples format
    for approach in response.get("approaches", []):
        if isinstance(approach, dict):
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
