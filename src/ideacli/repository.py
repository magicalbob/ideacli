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
        print(f"Error: No ideas repository found at '{ideas_repo_path}'. Please initialize one with 'ideacli init'.", file=sys.stderr)
        sys.exit(1)

    return ideas_repo_path

def ensure_repo(args):
    """Ensure the ideas repository exists and is valid."""
    return resolve_idea_path(args)

def init_repo(args):
    """Initialize a new ideas repository."""
    base_path = resolve_repo_root(args)
    repo_path = os.path.join(base_path, IDEAS_REPO)

    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    elif not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' exists but is not a directory.", file=sys.stderr)
        return False

    git_dir = os.path.join(repo_path, ".git")
    if not os.path.exists(git_dir):
        try:
            subprocess.check_call(["git", "init"], cwd=repo_path)
            subprocess.check_call(["git", "add", "."], cwd=repo_path)
            subprocess.check_call(["git", "commit", "-m", "Initial commit"], cwd=repo_path)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git initialization failed: {e}", file=sys.stderr)
            return False
    else:
        print(f"Directory {repo_path} exists but is not a git repository.", file=sys.stderr)
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
        output = subprocess.check_output(["git", "status"], cwd=path, text=True)
        print(output)
    except Exception as e:
        print(f"Error getting repository status: {e}", file=sys.stderr)
        return False

    return True
