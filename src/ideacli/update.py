"""Update mechanism for ideacli: merges JSON updates, supports clipboard, and preserves/merges 'files'."""

import json
import os
import sys
import pyperclip
from ideacli.repository import resolve_idea_path

def deep_update(original, update):
    """
    Recursively update a dictionary.
    For dictionaries, this performs a deep update.
    For other types, it replaces the value.
    """
    for key, value in update.items():
        if key in original and isinstance(original[key], dict) and isinstance(value, dict):
            deep_update(original[key], value)
        else:
            original[key] = value

def update_idea(args):
    """
    Update an idea with new JSON content.
    Special handling for 'files' to merge them instead of replacing.
    """
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    conversation_file = os.path.join(conversation_dir, f"{args.id}.json")

    if os.path.exists(conversation_file):
        with open(conversation_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {"id": args.id}

    # Read the new data
    try:
        if hasattr(args, 'json'):
            new_data = json.loads(args.json)
        else:
            clipboard_content = pyperclip.paste()
            print(f"Got clipboard content of length: {len(clipboard_content)}")
            print(f"Clipboard first 100 characters: {clipboard_content[:100]}")
            new_data = json.loads(clipboard_content)
            print("Successfully parsed JSON from clipboard")
            print(f"Keys in new_data: {list(new_data.keys())}")
            if 'files' in new_data:
                print(f"Found 'files' key with {len(new_data['files'])} entries")
                for file_name in new_data['files']:
                    print(f"  - {file_name}")
    except (json.JSONDecodeError, TypeError, AttributeError) as e:
        print(f"Error: Could not parse JSON: {e}")
        sys.exit(1)

    new_data["id"] = args.id

    # Merge 'files' fields in 'response' dicts if present
    if 'response' in new_data and 'files' in new_data['response']:
        if 'response' not in existing_data:
            existing_data['response'] = {}
        if 'files' not in existing_data['response']:
            existing_data['response']['files'] = new_data['response']['files']
        else:
            existing_files = existing_data['response']['files']
            new_files = new_data['response']['files']

            # Dict <-> Dict
            if isinstance(existing_files, dict) and isinstance(new_files, dict):
                existing_files.update(new_files)
            # List <-> List
            elif isinstance(existing_files, list) and isinstance(new_files, list):
                existing_files_map = {
                    f.get('name'): f for f in existing_files
                    if isinstance(f, dict) and 'name' in f
                }
                for new_file in new_files:
                    if isinstance(new_file, dict) and 'name' in new_file:
                        existing_files_map[new_file['name']] = new_file
                existing_data['response']['files'] = list(existing_files_map.values())
            # Dict <-> List or List <-> Dict
            else:
                if isinstance(existing_files, dict) and isinstance(new_files, list):
                    converted_files = [
                        {"name": name, "content": content}
                        for name, content in existing_files.items()
                    ]
                    files_map = {
                        f.get('name'): f
                        for f in converted_files + new_files
                        if isinstance(f, dict) and 'name' in f
                    }
                    existing_data['response']['files'] = list(files_map.values())
                elif isinstance(existing_files, list) and isinstance(new_files, dict):
                    converted_files = [
                        {"name": name, "content": content}
                        for name, content in new_files.items()
                    ]
                    files_map = {
                        f.get('name'): f
                        for f in existing_files
                        if isinstance(f, dict) and 'name' in f
                    }
                    for new_file in converted_files:
                        if 'name' in new_file:
                            files_map[new_file['name']] = new_file
                    existing_data['response']['files'] = list(files_map.values())
        del new_data['response']['files']

    # Preserve the existing 'subject' and 'body' if they're not in the new data
    if 'subject' in existing_data and 'subject' not in new_data:
        new_data['subject'] = existing_data['subject']
    if 'body' in existing_data and 'body' not in new_data:
        new_data['body'] = existing_data['body']

    # Deep update everything except already handled 'files'
    deep_update(existing_data, new_data)

    with open(conversation_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)

    print(f"Updated idea {args.id}")
