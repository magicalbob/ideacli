import json
import os
import sys
from ideacli.repository import resolve_idea_path

def remove_file(args):
    """Remove a file from the JSON record of an idea."""
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file, encoding="utf-8") as f:
        idea = json.load(f)

    files_data = idea.get("files", {})

    if args.file_name in files_data:
        del files_data[args.file_name]
        with open(idea_file, "w", encoding="utf-8") as f:
            json.dump(idea, f, indent=4)
        print(f"Removed {args.file_name} from idea {args.id}")
    else:
        print(f"File {args.file_name} not found in idea {args.id}")