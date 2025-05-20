"""List all ideas in the repository."""

import os
import json
from ideacli.repository import resolve_idea_path

def list_ideas(args):
    """List ideas in the repository."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")

    if not os.path.exists(conversation_dir):
        print("No conversations found.")
        return

    ideas = []
    for filename in os.listdir(conversation_dir):
        if filename.endswith(".json"):
            with open(os.path.join(conversation_dir, filename), "r", encoding="utf-8") as f:
                idea = json.load(f)
                ideas.append((idea.get("id"), idea.get("subject")))

    if not ideas:
        print("No ideas found.")
        return

    # Optional: sort by subject alphabetically
    ideas.sort(key=lambda x: (x[1] or '').lower())

    for idea_id, subject in ideas:
        print(f"[{idea_id}] {subject}")
