"""Command line interface for ideacli."""

import argparse
# Use relative import
from ideacli.repository import init_repo, status
from ideacli.add import add
from ideacli.list import list_ideas
from ideacli.show import show_idea
from ideacli.enquire import enquire
from ideacli.update import update_idea
from ideacli.files import list_files, extract_files
from ideacli.rename import rename_idea
from ideacli.importer import import_idea
from ideacli.rm import remove_file

def main():
    """Main entry point for the ideacli command."""
    parser = create_parser()
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
    elif args.command == "enquire":
        enquire(args)
    elif args.command == "update":
        update_idea(args)
    elif args.command == "files":
        list_files(args)
    elif args.command == "extract":
        extract_files(args)
    elif args.command == "rename":
        rename_idea(args)
    elif args.command == "version":
        # Import here to avoid circular import
        from ideacli import __version__
        print(f"ideacli version {__version__}")
    elif args.command == 'import':
        import_idea(args)
    elif args.command == 'rm':
        remove_file(args)
    else:
        parser.print_help()

def create_parser():
    """Creates and returns the argparse parser."""
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

    # List command
    list_parser = subparsers.add_parser("list", help="List all ideas")
    list_parser.add_argument("--path", help="Path to the repository")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show a specific idea by ID")
    show_parser.add_argument("--path", help="Path to the repository")
    show_parser.add_argument("--id", help="ID of the idea to show")

    # Enquire command
    enquire_parser = subparsers.add_parser("enquire",
                                           help="Prepare an idea with prompt for LLM input")
    enquire_parser.add_argument("--path", help="Path to the repository")
    enquire_parser.add_argument("--id", help="ID of the idea to enquire about", required=True)
    enquire_parser.add_argument("--prompt", help="Additional prompt for the LLM")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an idea using LLM response.")
    update_parser.add_argument("--path", help="Path to the repository")
    update_parser.add_argument("--id",
                               required=False,
                               help="The ID of the idea. (Only needed if stdin isn't used)")

    # Files command
    files_parser = subparsers.add_parser("files", help="List code files suggested in response")
    files_parser.add_argument("--path", help="Path to the repo")
    files_parser.add_argument("--id", required=True, help="ID of the idea")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract code samples into files")
    extract_parser.add_argument("--path", help="Path to the repo")
    extract_parser.add_argument("--id", required=True, help="ID of the idea")

    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Rename the subject of an idea by ID")
    rename_parser.add_argument("--path", help="Path to the repository")
    rename_parser.add_argument("--id", required=True, help="ID of the idea to rename")
    rename_parser.add_argument("--target", required=True, help="New subject/title for the idea")

    # Version command
    version_parser = subparsers.add_parser("version", help="Show the installed version of ideacli")

    # Import command
    import_parser = subparsers.add_parser('import', help='Import a file into an idea')
    import_parser.add_argument('source', help='Source file to import')
    import_parser.add_argument('--destination', 
                               help='Destination filename within the idea (defaults to source filename)')
    import_parser.add_argument('--id', required=True, help='ID of the idea to import into')
    import_parser.add_argument('--path', help='Custom path to ideas repository')
    import_parser.add_argument('--force', action='store_true', help='Force overwrite if file already exists')

    # rm command
    rm_parser = subparsers.add_parser('rm', help='Remove a file from an idea')
    rm_parser.add_argument('--id', required=True, help='ID of the idea to remove a file from')
    rm_parser.add_argument('file_name', help='Name of the file to remove')
    rm_parser.add_argument('--path', help='Custom path to ideas repository')

    return parser

if __name__ == "__main__":
    main()
