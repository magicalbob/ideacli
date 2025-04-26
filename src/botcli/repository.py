"""Repository management functionality for botcli."""

import os
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
            f.write("# LLM Conversations Repository\n\nManaged by idea-cli\n")
        
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

def status(args):
    """Check status of the ideas repository"""
    path = args.path if args.path else IDEAS_REPO
    
    if not os.path.exists(os.path.join(path, ".git")):
        print(f"No ideas repository found at {path}")
        return False
    
    try:
        # Get git status
        status_output = subprocess.check_output(
            ["git", "status"], cwd=path, universal_newlines=True
        )
        
        # Get summary stats
        num_conversations = len(os.listdir(os.path.join(path, "conversations")))
        
        status_msg = f"Ideas Repository Status:\n\n"
        status_msg += f"Location: {os.path.abspath(path)}\n"
        status_msg += f"Number of conversations: {num_conversations}\n\n"
        status_msg += "Git Status:\n"
        status_msg += status_output
        
        print(status_msg)
        
        return True
    except Exception as e:
        print(f"Error getting repository status: {e}")
        return False
