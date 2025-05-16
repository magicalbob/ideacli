"""Prepare an idea with prompt for LLM input."""

import os
import json
import sys
from ideacli.repository import resolve_idea_path
from ideacli.clipboard import copy_to_clipboard

def enquire(args):
    # Load existing data if available
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    conversation_file = os.path.join(conversation_dir, f"{args.id}.json")

    # Read the template file
    template_path = os.path.join(repo_path, "../prompt-template.json")
    print(f"Looking for template at: {template_path}")
    template_content = None
    if os.path.exists(template_path):
        print(f"Template file found!")
        try:
            with open(template_path, "r") as f:
                template_content = json.load(f)
                print(f"Template loaded successfully")
        except json.JSONDecodeError as e:
            print(f"Warning: prompt-template.json is not valid JSON: {e}")
    else:
        print(f"Template file not found at: {template_path}")

    # Prepare the enquiry data
    if os.path.exists(conversation_file):
        with open(conversation_file, "r") as f:
            data = json.load(f)
    else:
        data = {"id": args.id}

    # Update data with user prompt
    if hasattr(args, 'prompt'):
        data["body"] = args.prompt

    # Extract just the user's prompt (not the full JSON structure)
    user_prompt = ""
    if "subject" in data and data["subject"]:
        user_prompt += data["subject"] + "\n\n"
    if "body" in data and data["body"]:
        user_prompt += data["body"]

    # Add our format instructions
    format_instr = ""
    if template_content:
        print("Adding format instructions from template")
        format_instr += "\n\n## RESPONSE FORMAT REQUIREMENTS:\n"

        # Get the description
        desc = template_content.get("format_instructions", {}).get("description", "")
        if desc:
            format_instr += desc + "\n\n"
            print("Added description from template")

        # Add the expected structure details
        expected = template_content.get("format_instructions", {}).get("expected_structure")
        if expected:
            format_instr += "Your response must be a valid JSON object with this structure:\n\n"
            format_instr += "```json\n" + json.dumps(expected, indent=2) + "\n```\n\n"
            print("Added expected structure from template")

        # Add the important notes
        notes = template_content.get("format_instructions", {}).get("important_notes", [])
        if notes:
            format_instr += "IMPORTANT:\n"
            for note in notes:
                format_instr += f"- {note}\n"
            print("Added important notes from template")
    else:
        print("No template content available to add format instructions")

    # Create the FULL prompt that will be sent to the LLM
    lm_prompt = user_prompt + format_instr

    # Store this in the data
    data["prompt"] = lm_prompt

    # Save data to file
    with open(conversation_file, "w") as f:
        json.dump(data, f, indent=2)

    # Copy the prompt to clipboard
    try:
        import pyperclip
        pyperclip.copy(lm_prompt)
        print(f"LLM prompt copied to clipboard! Length: {len(lm_prompt)} characters")
    except ImportError:
        print("Warning: pyperclip not installed. Cannot copy to clipboard.")
    except Exception as e:
        print(f"Warning: Could not copy to clipboard: {e}")

    # Write full json to output file if requested
    if hasattr(args, 'output') and args.output:
        output_data = {"conversation": data, "prompt": lm_prompt}
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
