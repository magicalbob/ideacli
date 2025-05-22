"""File operations for extracting and listing code samples from ideas."""

import json
import os
import sys
from ideacli.repository import resolve_idea_path

def list_files(args):
    """List filenames (with relative paths, if available) associated with a conversation."""
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    files = set()

    # Helper to add path+filename, defaulting to just filename
    def add_file(file_dict):
        if isinstance(file_dict, dict):
            for fname, fobj in file_dict.items():
                # New format: fobj is dict with 'content' and 'path'
                if isinstance(fobj, dict):
                    path = (fobj.get("path") or "").strip()
                    # Normalize the path, avoid double slashes, handle "" or "."
                    if path in ("", "."):
                        files.add(fname)
                    else:
                        if not path.endswith("/"):
                            path += "/"
                        files.add(f"{path}{fname}")
                # Legacy: fobj is just content string
                elif isinstance(fobj, str):
                    files.add(fname)
                # Unexpected: ignore/skip
        elif isinstance(file_dict, list):
            for entry in file_dict:
                if isinstance(entry, dict):
                    fname = entry.get("name")
                    path = (entry.get("path") or "").strip()
                    if fname:
                        if path in ("", "."):
                            files.add(fname)
                        else:
                            if not path.endswith("/"):
                                path += "/"
                            files.add(f"{path}{fname}")

    # Collect files from response and root-level
    add_file(idea.get("response", {}).get("files"))
    add_file(idea.get("files"))

    if files:
        print("\n".join(sorted(files)))
    else:
        print("No files found in idea response.")

def _write_file(filename, file_obj):
    """Write content to filename, creating directories as needed."""
    # If file_obj is a dict (new format), extract path/content
    if isinstance(file_obj, dict):
        content = file_obj.get("content", "")
        path = (file_obj.get("path") or "").strip()
        if path and path not in ("", "."):
            actual_path = os.path.join(path, filename)
        else:
            actual_path = filename
    # If file_obj is a string (legacy format)
    elif isinstance(file_obj, str):
        content = file_obj
        actual_path = filename
    else:
        raise ValueError(f"File object for {filename} is of unsupported type: {type(file_obj)}")
    dir_name = os.path.dirname(actual_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(actual_path, "w", encoding="utf-8") as out_file:
        out_file.write(content)
    print(f"Wrote {actual_path}")

def _extract_from_files_data(files_data):
    """Extract files from a files dict or list structure."""
    extracted = False
    if isinstance(files_data, dict):
        for filename, file_obj in files_data.items():
            _write_file(filename, file_obj)
            extracted = True
    elif isinstance(files_data, list):
        for file_entry in files_data:
            if isinstance(file_entry, dict):
                fname = file_entry.get("name")
                path = (file_entry.get("path") or "").strip()
                content = file_entry.get("content", "")
                # Compose actual_path
                if path and path not in ("", "."):
                    actual_path = os.path.join(path, fname)
                else:
                    actual_path = fname
                _write_file(actual_path, content)
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
