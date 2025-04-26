"""Command line interface for ideacli."""

import argparse
import sys
# Use relative import
from ideacli.repository import init_repo, status
from ideacli.add import add
from ideacli.list import list_ideas
from ideacli.show import show_idea

def main():
    """Main entry point for the ideacli command."""
    parser = argparse.ArgumentParser(description="CLI tool for managing LLM conversation ideas")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new ideas repository")
    init_parser.add_argument("--path", help="Path for the new repository")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check status of ideas repository")
    status_parser.add_argument("--path", help="Path to the repository")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new idea to the repository")
    add_parser.add_argument("--path", help="Path to the repository")

    #List command
    list_parser = subparsers.add_parser("list", help="List all ideas")
    list_parser.add_argument("--path", help="Path to the repository")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show a specific idea by ID")
    show_parser.add_argument("--path", help="Path to the repository")
    show_parser.add_argument("--id", help="ID of the idea to show")

    args = parser.parse_args()
    
    if args.command == "init":
        init_repo(args)
    elif args.command == "status":
        status(args)
    elif args.command == "add":
        add(args)
    elif args.command == "list":
        list_ideas(args)
    elif args.command == "show":
        show_idea(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
