"""Repository utilities for ideacli."""

import os
import sys
import subprocess

IDEAS_REPO = ".ideas_repo"

def resolve_repo_root(args):
    """Resolve the root path for the ideas repo."""
    if hasattr(args, "path") and args.path:
        return os.path.abspath(args.path)
    return os.getcwd()

def resolve_idea_path(args):
    """Resolve and validate idea repository path."""
    base_path = resolve_repo_root(args)
    ideas_repo_path = os.path.join(base_path, IDEAS_REPO)

    if not os.path.isdir(ideas_repo_path):
        print(
            f"Error: No ideas repository found at '{ideas_repo_path}'. "
            "Please initialize one with 'ideacli init'.",
            file=sys.stderr
        )
        sys.exit(1)

    return ideas_repo_path

def ensure_repo(args):
    """Ensure the ideas repository exists and is valid."""
    return resolve_idea_path(args)

def init_repo(args):
    """Initialize a new ideas repository."""
    path = args.path if hasattr(args, "path") and args.path else IDEAS_REPO

    if os.path.exists(path):
        if not os.path.exists(os.path.join(path, ".git")):
            print(f"Directory {path} exists but is not a git repository.")
            return False
        print(f"Repository already exists at {path}")
        return True

    try:
        os.makedirs(path, exist_ok=True)
        subprocess.run(["git", "init"], cwd=path, check=True)

        os.makedirs(os.path.join(path, "conversations"), exist_ok=True)
        with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
            f.write("# LLM Conversations Repository\n\nManaged by ideacli\n")

        subprocess.run(["git", "add", "."], cwd=path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial repository structure"],
            cwd=path,
            check=True
        )

        print(f"Initialized new ideas repository in {path}")
        return True

    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error initializing repository: {e}")
        return False

def status(args):
    """Show the status of the ideas repository."""
    path = resolve_idea_path(args)
    print("\nIdeas Repository Status:\n")
    print(f"Location: {path}")

    conv_path = os.path.join(path, "conversations")
    if os.path.isdir(conv_path):
        count = len([f for f in os.listdir(conv_path) if f.endswith(".json")])
        print(f"Number of conversations: {count}\n")
    else:
        print("Conversations folder missing.\n")

    print("Git Status:")
    try:
        output = subprocess.check_output(
            ["git", "status"], cwd=path, text=True
        )
        print(output)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error getting repository status: {e}", file=sys.stderr)
        return False

    return True
