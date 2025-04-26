#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import argparse

def copy_to_clipboard(text):
    """Copy text to clipboard based on platform"""
    if platform.system() == "Darwin":  # macOS
        process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
        process.communicate(text.encode())
    elif platform.system() == "Windows":
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        process.communicate(text.encode())
    elif platform.system() == "Linux":
        try:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode())
        except FileNotFoundError:
            try:
                process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
                process.communicate(text.encode())
            except FileNotFoundError:
                print("Error: No clipboard command found. Install xclip or wl-copy.")
                return False
    print("Copied to clipboard!")
    return True

def paste_from_clipboard():
    """Get text from clipboard based on platform"""
    if platform.system() == "Darwin":  # macOS
        return subprocess.check_output('pbpaste', universal_newlines=True)
    elif platform.system() == "Windows":
        try:
            return subprocess.check_output(['powershell.exe', '-command', 'Get-Clipboard'], universal_newlines=True)
        except:
            print("Error getting clipboard contents on Windows")
            return ""
    elif platform.system() == "Linux":
        try:
            return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], universal_newlines=True)
        except FileNotFoundError:
            try:
                return subprocess.check_output(['wl-paste'], universal_newlines=True)
            except FileNotFoundError:
                print("Error: No clipboard command found. Install xclip or wl-copy.")
                return ""

def init_repo(args):
    """Initialize a new ideas repository"""
    path = args.path if args.path else "./ideas_repo"
    
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
        copy_to_clipboard(success_msg)
        
        return True
    except Exception as e:
        print(f"Error initializing repository: {e}")
        return False

def status(args):
    """Check status of the ideas repository"""
    path = args.path if args.path else "./ideas_repo"
    
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
        
        # Copy status to clipboard
        copy_to_clipboard(status_msg)
        
        return True
    except Exception as e:
        print(f"Error getting repository status: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="CLI tool for managing LLM conversation ideas")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new ideas repository")
    init_parser.add_argument("--path", help="Path for the new repository")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of ideas repository")
    status_parser.add_argument("--path", help="Path to the repository")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_repo(args)
    elif args.command == "status":
        status(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
