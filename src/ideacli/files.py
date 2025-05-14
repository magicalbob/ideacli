# src/ideacli/files.py

from ideacli.repository import resolve_idea_path
import json
import os
import sys

def list_files(args):
    repo_path = resolve_idea_path(args)
    idea_file = os.path.join(repo_path, "conversations", f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"No conversation with ID {args.id}")
        sys.exit(1)

    with open(idea_file) as f:
        idea = json.load(f)

    response = idea.get("response", {})
    files = []
    for approach in response.get("approaches", []):
        for sample in approach.get("code_samples", []):
            files.append(sample.get("file"))

    if files:
        print("\n".join(files))
    else:
        print("No files found in idea response.")
