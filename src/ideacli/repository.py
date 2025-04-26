"""Repository management functionality for ideacli."""

import os
import sys
import subprocess
# Use relative import
from .clipboard import copy_to_clipboard

# Default repository location (hidden directory)
IDEAS_REPO = os.path.join('.', '.ideas_repo')

def init_repo(args):
    """Initialize a new ideas repository"""
    path = args.path if args.path else IDEAS_REPO
    
    if os.path.exists(path):
        if not os.path.exists(os.path.join(path, ".git")):
            print(f"Directory {path} exists but is not a git repository.")
            return False
        else:
            print(f"Repository already exists at {path}")
            return True
    
    try:
        os.makedirs(path, exist_ok=True)
        subprocess.run(["git", "init"], cwd=path, check=True)
        # Create initial README
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write("# LLM Conversations Repository\n\nManaged by ideacli\n")
        
        # Create initial structure
        os.makedirs(os.path.join(path, "conversations"), exist_ok=True)
        
        # Commit initial structure
        subprocess.run(["git", "add", "."], cwd=path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial repository structure"], cwd=path, check=True)
        
        print(f"Initialized new ideas repository in {path}")
        
        # Copy success message to clipboard
        success_msg = f"Ideas repository initialized in {path}"
        
        return True
    except Exception as e:
        print(f"Error initializing repository: {e}")
        return False

def ensure_repo(args):
    """Ensure the ideas repository is initialized."""
    if not init_repo(args):
        print("Error: Could not initialize ideas repository.", file=sys.stderr)
        sys.exit(1)

def resolve_idea_path(args):
    """Resolve and validate idea repository path."""
    if hasattr(args, "path") and args.path:
        base_path = os.path.abspath(args.path)
        ideas_repo_path = os.path.join(base_path, ".ideas_repo")
    else:
        ideas_repo_path = os.path.abspath(IDEAS_REPO)

    if not os.path.isdir(ideas_repo_path):
        print(f"Error: No ideas repository found at '{ideas_repo_path}'. Please initialize one with 'ideacli init'.", file=sys.stderr)
        sys.exit(1)

    return ideas_repo_path

def status(args):
    """Check status of the ideas repository"""
    path = resolve_idea_path(args)

    if not os.path.exists(os.path.join(path, ".git")):
        print("Error: Ideas repository not found.", file=sys.stderr)
        return False

    try:
        print("\nIdeas Repository Status:\n")
        print(f"Location: {path}")

        conversation_dir = os.path.join(path, "conversations")
        if os.path.exists(conversation_dir):
            conversations = [
                f for f in os.listdir(conversation_dir)
                if f.endswith(".json") and os.path.isfile(os.path.join(conversation_dir, f))
            ]
            print(f"Number of conversations: {len(conversations)}")
        else:
            print("No conversations directory found.")

        print("\nGit Status:")
        git_status = subprocess.check_output(["git", "status"], cwd=path, universal_newlines=True)
        print(git_status)

        return True
    except Exception as e:
        print(f"Error getting repository status: {e}", file=sys.stderr)
        return False
