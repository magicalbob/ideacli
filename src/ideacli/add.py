import os
import sys
import json
import uuid
import subprocess
from ideacli.repository import ensure_repo  # helper to init/check repo if needed
from ideacli.clipboard import copy_to_clipboard  # your existing clipboard utils
from ideacli.repository import IDEAS_REPO

def add(args):
    ensure_repo(args)

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
    idea_id = str(uuid.uuid4())[:8]  # Short UUID, can tweak this

    # Prepare JSON
    idea = {
        "id": idea_id,
        "subject": subject,
        "body": body
    }

    # Write file
    conversation_dir = os.path.join(IDEAS_REPO, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)

    idea_path = os.path.join(conversation_dir, f"{idea_id}.json")
    with open(idea_path, "w") as f:
        json.dump(idea, f, indent=2)

    # Git commit
    subprocess.run(["git", "add", "."], cwd=IDEAS_REPO, check=True)
    subprocess.run(["git", "commit", "-m", f"Add idea: {idea_id} - {subject}"], cwd=IDEAS_REPO, check=True)

    # Clipboard
    copy_to_clipboard(idea_id)

    print(f"Idea '{subject}' saved as {idea_id} and committed.")
