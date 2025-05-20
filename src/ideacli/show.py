"""Show a specific idea by ID."""

import os
import json
import sys
from ideacli.repository import resolve_idea_path

def show_idea(args):
    """Show the details of a conversation by ID."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    idea_file = os.path.join(conversation_dir, f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(
            f"Error: No conversation found with ID '{args.id}'",
            file=sys.stderr
        )
        sys.exit(1)

    try:
        with open(idea_file, "r", encoding="utf-8") as f:
            idea = json.load(f)

        print(f"Subject: {idea.get('subject', '(No subject)')}\n")
        print(f"Body:\n{idea.get('body', '(No body)')}\n")

        response = idea.get('response')
        if response:
            print("Response:")
            print(json.dumps(response, indent=2))
        else:
            print("(No response recorded)")

    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"Error reading conversation file: {e}", file=sys.stderr)
        sys.exit(1)
