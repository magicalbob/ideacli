"""Command line interface for botcli."""

import argparse
import sys
# Use relative import
from .repository import init_repo, status

def main():
    """Main entry point for the botcli command."""
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
