"""File operations for extracting and listing code samples from ideas."""

import json
import os
import sys
from ideacli.repository import resolve_idea_path

def list_files(args):
    """List file paths associated with a conversation (uses 'path' attribute if present)."""
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    filepaths = set()

    # Helper to extract files from a 'files' dict
    def extract_filepaths(files_data):
        if isinstance(files_data, dict):
            for fname, fileobj in files_data.items():
                # Handle new format: fileobj is a dict with 'content' and 'path'
                if isinstance(fileobj, dict):
                    path = (fileobj.get("path") or "").strip()
                    if path and not path.endswith("/"):
                        path += "/"
                    full_path = f"{path}{fname}" if path else fname
                    filepaths.add(full_path)
                # Legacy: fileobj is a string (just content, no path)
                elif isinstance(fileobj, str):
                    filepaths.add(fname)
        elif isinstance(files_data, list):
            for file_entry in files_data:
                if isinstance(file_entry, dict):
                    fname = file_entry.get("name")
                    path = (file_entry.get("path") or "").strip()
                    if path and not path.endswith("/"):
                        path += "/"
                    full_path = f"{path}{fname}" if path else fname
                    filepaths.add(full_path)

    # Look in root files and response.files
    extract_filepaths(idea.get("files"))
    extract_filepaths(idea.get("response", {}).get("files"))

    if filepaths:
        print("\n".join(sorted(filepaths)))
    else:
        print("No files found in idea response.")

def _write_file(filename, content):
    """Write content to filename, creating directories as needed."""
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as out_file:
        out_file.write(content)
    print(f"Wrote {filename}")


def _extract_from_files_data(files_data):
    """Extract files from a files dict or list structure."""
    extracted = False
    if isinstance(files_data, dict):
        for filename, content in files_data.items():
            _write_file(filename, content)
            extracted = True
    elif isinstance(files_data, list):
        for file_entry in files_data:
            if isinstance(file_entry, dict):
                file_name = file_entry.get("name")
                content = file_entry.get("content")
                if file_name and content:
                    _write_file(file_name, content)
                    extracted = True
    return extracted


def _extract_from_approaches(approaches):
    """Extract files from approaches code_samples."""
    extracted = False
    for approach in approaches or []:
        if isinstance(approach, dict):
            for sample in approach.get("code_samples", []):
                file_path = sample.get("file")
                code = sample.get("code")
                if file_path and code:
                    _write_file(file_path, code)
                    extracted = True
    return extracted


def extract_files(args):
    """Extract code samples into real files from an idea conversation."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    idea_file = os.path.join(conversation_dir, f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"Error: No conversation found with ID '{args.id}'")
        sys.exit(1)

    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    response = idea.get("response", {})

    extracted = False
    # Extract from response['files'] and root-level 'files'
    extracted |= _extract_from_files_data(response.get("files", {}))
    extracted |= _extract_from_files_data(idea.get("files", {}))
    # Extract from approaches
    extracted |= _extract_from_approaches(response.get("approaches", []))

    if not extracted:
        print("No files found to extract.")
