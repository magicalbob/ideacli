"""Rename the subject of an idea by ID."""

import os
import json
import sys
from ideacli.repository import resolve_idea_path

def rename_idea(args):
    """Rename the subject of a conversation by ID."""
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

        old_subject = idea.get("subject", "(No subject)")
        idea["subject"] = args.target

        with open(idea_file, "w", encoding="utf-8") as f:
            json.dump(idea, f, indent=2)

        print(
            f"Renamed idea '{args.id}' from:\n  {old_subject}\nto:\n  {args.target}"
        )

    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"Error renaming idea: {e}", file=sys.stderr)
        sys.exit(1)
