#!/usr/bin/env python3
import json
import sys
import os

def extract_filename_and_path(key):
    # If key includes a path, split it
    if "/" in key:
        path, filename = os.path.split(key)
        return filename, path
    return key, ""

def normalize_files(files):
    new_files = {}
    # Legacy: dict mapping str to str, or str to {content, path}
    for key, value in files.items():
        filename, path = extract_filename_and_path(key)
        if isinstance(value, dict):
            # Already in new form, but ensure both keys exist
            content = value.get("content", "")
            vpath = value.get("path", path)
            if vpath is None:
                vpath = ""
            new_files[filename] = {
                "content": content,
                "path": vpath
            }
        elif isinstance(value, str):
            # Legacy: value is just content, no path
            new_files[filename] = {
                "content": value,
                "path": path  # path is "" unless found in key
            }
        else:
            print(f"WARNING: Ignoring unexpected value for file {key}: {value}", file=sys.stderr)
    return new_files

def cleanup_idea_json(data):
    # Normalize root-level files
    if "files" in data and isinstance(data["files"], dict):
        data["files"] = normalize_files(data["files"])

    # Optionally, normalize files in response (if your structure uses this)
    if "response" in data and isinstance(data["response"], dict):
        if "files" in data["response"] and isinstance(data["response"]["files"], dict):
            data["response"]["files"] = normalize_files(data["response"]["files"])

    return data

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    cleaned = cleanup_idea_json(input_data)
    json.dump(cleaned, sys.stdout, indent=2)
    print()
