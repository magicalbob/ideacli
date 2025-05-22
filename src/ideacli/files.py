"""File operations for extracting and listing code samples from ideas."""

import json
import os
import sys
from ideacli.repository import resolve_idea_path

SKIP_FILE_KEYS = {"state", "prompt", "last_prompt", "response", "files_needed"}

def list_files(args):
    """List filenames with paths associated with a conversation."""
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    files = set()

    # Helper to extract filename+path from a file_obj
    def extract_file_path(filename, file_obj):
        if isinstance(file_obj, dict):
            pth = (file_obj.get("path") or "").strip()
            if pth and not pth.endswith("/"):
                pth += "/"
            return f"{pth}{filename}" if pth else filename
        elif isinstance(file_obj, str):
            return filename
        return None

    # Collect file names from both 'response' and root-level 'files'
    for files_data in (idea.get("response", {}).get("files"), idea.get("files")):
        if isinstance(files_data, dict):
            for filename, file_obj in files_data.items():
                relpath = extract_file_path(filename, file_obj)
                if relpath:
                    files.add(relpath)

    if files:
        print("\n".join(sorted(files)))
    else:
        print("No files found in idea response.")

def _write_file(filename, content, path=""):
    """Write content to filename, creating directories as needed."""
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    if path and path not in ("", "."):
        actual_path = os.path.join(path, filename)
    else:
        actual_path = filename
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
            # --- Skip keys that are not actual files ---
            if filename in SKIP_FILE_KEYS:
                continue
            # Legacy: value is just file content
            if isinstance(file_obj, str):
                _write_file(filename, file_obj)
                extracted = True
            # New format: dict with at least 'content'
            elif isinstance(file_obj, dict) and "content" in file_obj:
                content = file_obj["content"]
                path = (file_obj.get("path") or "").strip()
                if isinstance(content, dict):
                    content = json.dumps(content, indent=2)
                _write_file(filename, content, path)
                extracted = True
            else:
                # Not a file; skip with message (quietly)
                continue
    elif isinstance(files_data, list):
        for file_entry in files_data:
            if isinstance(file_entry, dict):
                file_name = file_entry.get("name")
                content = file_entry.get("content")
                path = (file_entry.get("path") or "").strip()
                if file_name and content is not None:
                    if isinstance(content, dict):
                        content = json.dumps(content, indent=2)
                    _write_file(file_name, content, path)
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
