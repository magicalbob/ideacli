import sys
import json
import os
from ideacli.repository import resolve_idea_path
from ideacli.clipboard import paste_from_clipboard

def update(args):
    """Update an existing idea using input from clipboard or stdin."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")

    # Read from stdin if data is piped in, otherwise use clipboard
    if not sys.stdin.isatty():
        clipboard_json = sys.stdin.read().strip()
    else:
        clipboard_json = paste_from_clipboard()

    if not clipboard_json:
        print("Error: No valid JSON found in input.", file=sys.stderr)
        sys.exit(1)

    try:
        llm_response = json.loads(clipboard_json)

        idea_id = llm_response.get("conversation", {}).get("id") or args.id
        if not idea_id:
            print("Error: No idea ID found. Provide it via argument or within JSON input.", file=sys.stderr)
            sys.exit(1)

        idea_file = os.path.join(conversation_dir, f"{idea_id}.json")
        if not os.path.isfile(idea_file):
            print(f"Error: No conversation found with ID '{idea_id}'", file=sys.stderr)
            sys.exit(1)

        with open(idea_file, "r") as f:
            existing_data = json.load(f)

        # Merge new response into existing idea
        existing_data["response"] = llm_response.get("response", {})

        with open(idea_file, "w") as f:
            json.dump(existing_data, f, indent=2)

        print(f"Successfully updated idea '{idea_id}'.")

    except Exception as e:
        print(f"Error updating idea: {e}", file=sys.stderr)
        sys.exit(1)
