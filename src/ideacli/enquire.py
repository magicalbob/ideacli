"""Prepare an idea with prompt for LLM input."""

import os
import json
import sys
from ideacli.repository import resolve_idea_path
from ideacli.clipboard import copy_to_clipboard

def enquire(args):
    """Display the idea as JSON with an extra prompt and copy to clipboard."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")

    idea_file = os.path.join(conversation_dir, f"{args.id}.json")

    if not os.path.isfile(idea_file):
        print(f"Error: No conversation found with ID '{args.id}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(idea_file, "r") as f:
            idea = json.load(f)
        
        # Create a new object with the idea and the prompt
        llm_input = {
            "conversation": idea,
            "prompt": args.prompt or "Please provide feedback on this idea."
        }
        
        # Convert to JSON string with pretty formatting
        json_str = json.dumps(llm_input, indent=2)
        
        # Display to console
        print("Prepared LLM Input:")
        print(json_str)
        
        # Copy to clipboard
        success = copy_to_clipboard(json_str)
        if success:
            print("\nJSON copied to clipboard and ready for pasting to your LLM!")
        
    except Exception as e:
        print(f"Error preparing LLM input: {e}", file=sys.stderr)
        sys.exit(1)
