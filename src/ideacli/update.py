"""
Update mechanism for ideacli: handles stateful updates,
ensures original prompt is included, and manages file analysis workflow.
"""

import json
import os
import sys

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

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
    Update an idea with new JSON content, supporting analysis phase and solution phase.
    """
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    conversation_file = os.path.join(conversation_dir, f"{args.id}.json")

    # Load existing data
    if os.path.exists(conversation_file):
        with open(conversation_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        print(f"Error: No conversation with ID {args.id}")
        sys.exit(1)

    state = existing_data.get("state", "added")

    # Read new input (clipboard or --json)
    try:
        if hasattr(args, 'json') and args.json:
            new_data = json.loads(args.json)
        else:
            import pyperclip
            clipboard_content = pyperclip.paste()
            new_data = json.loads(clipboard_content)
    except Exception as e:
        print(f"Error: Could not parse JSON: {e}")
        sys.exit(1)

    # --- PHASE 1: "analysis requested" - user pasted files_needed from LLM ---
    if state == "analysis requested" and "files_needed" in new_data:
        files_needed = new_data["files_needed"]

        # 1. Fetch the original prompt (subject + body)
        subject = existing_data.get("subject", "")
        body = existing_data.get("body", "")
        original_prompt = subject
        if body:
            original_prompt += "\n\n" + body

        # 2. Prepare the files requested
        files_available = existing_data.get("files", {})
        repo_root = repo_path  # Adjust if your files are elsewhere

        file_texts = []
        for fname in files_needed:
            # Try from repo root, then from files in JSON if present
            fpath = os.path.join(repo_root, fname)
            file_content = None
            if os.path.isfile(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    file_content = f.read()
            elif files_available and fname in files_available:
                file_content = files_available[fname]
            else:
                file_content = "[File not found]"
            file_texts.append(f"--- {fname} ---\n{file_content}")

        files_section = "\n".join(file_texts)

        # 3. Assemble new prompt
        solution_prompt = (
            f"{original_prompt}\n\n"
            f"Here are the files you requested:\n"
            f"{files_section}\n\n"
            "Please answer the original question above, using these files. "
            "Respond ONLY with a valid JSON object containing your analysis, "
            "and (optionally) any updated files as a JSON property 'files'."
        )

        # 4. Copy prompt to clipboard
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(solution_prompt)
                print(f"Prompt for LLM copied to clipboard! ({len(solution_prompt)} chars)")
            except Exception as e:
                print(f"Could not copy to clipboard: {e}")
        else:
            print("--- Prompt for LLM ---\n")
            print(solution_prompt)

        # 5. Update state, save files_needed and prompt for auditing
        existing_data["state"] = "updated"
        existing_data["files_needed"] = files_needed
        existing_data["last_prompt"] = solution_prompt
        with open(conversation_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2)
        print("Ready for next LLM roundtrip.")
        return

    # --- PHASE 2: "updated" - user pastes LLM's actual answer/changes ---
    elif state == "updated":
        # Expect new_data to contain LLM's answer and optionally updated files
        # (This logic may need customizing depending on your LLM output structure)

        # Merge new content, prioritizing 'files' if present
        if "files" in new_data:
            # Store under response for consistency
            if "response" not in existing_data:
                existing_data["response"] = {}
            existing_data["response"]["files"] = new_data["files"]

        # Optionally save LLM's analysis/answer
        for k in ("analysis", "conclusion", "answer"):
            if k in new_data:
                if "response" not in existing_data:
                    existing_data["response"] = {}
                existing_data["response"][k] = new_data[k]

        existing_data["state"] = "added"  # or maybe "completed"
        with open(conversation_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2)
        print("Conversation updated with LLM's solution.")
        return

    # Error conditions: update called in wrong state
    elif state == "added":
        print("Error: Cannot update an idea in 'added' state. Run 'enquire' first.")
        sys.exit(1)
    else:
        print(f"Error: Unhandled conversation state '{state}'.")
        sys.exit(1)
