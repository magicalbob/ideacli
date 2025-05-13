"""Update an existing idea by ID with LLM response."""

import os
import json
import sys
import subprocess
from ideacli.repository import resolve_idea_path
from ideacli.clipboard import paste_from_clipboard  # <- add this import

def update_idea(args):
    """Update an existing idea with LLM response JSON from stdin or clipboard."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    idea_file = os.path.join(conversation_dir, f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"Error: No conversation found with ID '{args.id}'", file=sys.stderr)
        sys.exit(1)

    # Read input
    try:
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print("No input piped, reading response from clipboard...")
            input_text = paste_from_clipboard()

        response_json = json.loads(input_text)

    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    # Load existing idea
    try:
        with open(idea_file, "r") as f:
            idea = json.load(f)
    except Exception as e:
        print(f"Error reading idea file: {e}", file=sys.stderr)
        sys.exit(1)

    # Update response field
    idea["response"] = response_json

    # Save updated idea
    try:
        with open(idea_file, "w") as f:
            json.dump(idea, f, indent=2)

        # Stage changes
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

        # Only commit if there are staged changes
        result = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=repo_path)
        if result.returncode != 0:
            subprocess.run(
                ["git", "commit", "-m", f"Update idea: {args.id} with response"],
                cwd=repo_path,
                check=True
            )
            print(f"Successfully updated idea '{args.id}'.")
        else:
            print(f"No changes to update for idea '{args.id}'.")

    except Exception as e:
        print(f"Error updating idea: {e}", file=sys.stderr)
        sys.exit(1)
