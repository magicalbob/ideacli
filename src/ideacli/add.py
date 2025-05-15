"""Add a new idea to the ideas repository."""

import os
import sys
import json
import uuid
import subprocess
from ideacli.repository import resolve_idea_path
from ideacli.clipboard import copy_to_clipboard

ERROR_REPO_NOT_FOUND = "Error: ideas repository not found at '{}'. Forget to run 'ideacli init'?"

def add(args):
    """Add by prompting user/reading piped input, saves, commits & copies ID to clipboard."""
    repo_path = resolve_idea_path(args)

    # Check that conversations directory exists
    conversation_dir = os.path.join(repo_path, "conversations")
    if not os.path.exists(conversation_dir):
        print(ERROR_REPO_NOT_FOUND.format(repo_path), file=sys.stderr)
        sys.exit(1)

    if sys.stdin.isatty():
        # Interactive
        subject = input("Subject: ").strip()
        print("Body (end with CTRL+D on empty line):")
        body = sys.stdin.read().strip()
    else:
        # Piped input
        lines = sys.stdin.read().splitlines()
        if not lines:
            print("Error: No input provided.", file=sys.stderr)
            sys.exit(1)
        subject = lines[0].strip()
        body = "\n".join(lines[1:]).strip()

    if not subject or not body:
        print("Error: Both subject and body are required.", file=sys.stderr)
        sys.exit(1)

    # Create unique random ID
    idea_id = str(uuid.uuid4())[:8]  # Short UUID

    # Prepare JSON
    idea = {
        "id": idea_id,
        "subject": subject,
        "body": body
    }

    # Write file
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    idea_path = os.path.join(conversation_dir, f"{idea_id}.json")
    with open(idea_path, "w", encoding="utf-8") as f:
        json.dump(idea, f, indent=2)

    # Git commit
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Add idea: {idea_id} - {subject}"],
        cwd=repo_path,
        check=True
    )

    # Clipboard
    copy_to_clipboard(idea_id)
    print(f"Idea '{subject}' saved as {idea_id} and committed.")
