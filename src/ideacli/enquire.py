"""Prepare an idea with prompt for LLM input (patched for no-files shortcut)."""

import os
import json
from ideacli.repository import resolve_idea_path

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

def load_template(template_path):
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: prompt-template.json is not valid JSON: {e}")
    return None

def build_format_instructions(template):
    if not template:
        return ""
    lines = ["\n\n## RESPONSE FORMAT REQUIREMENTS:\n"]
    desc = template.get("format_instructions", {}).get("description", "")
    if desc:
        lines.append(desc + "\n\n")
    expected = template.get("format_instructions", {}).get("expected_structure")
    if expected:
        lines.append("Your response must be a valid JSON object with this structure:\n\n")
        lines.append("```json\n" + json.dumps(expected, indent=2) + "\n```\n\n")
    notes = template.get("format_instructions", {}).get("important_notes", [])
    if notes:
        lines.append("IMPORTANT:\n")
        lines.extend(f"- {note}\n" for note in notes)
    return "".join(lines)

def files_in_idea(data):
    """Returns a list of files mentioned in the idea (in response/files or root-level files)."""
    files = set()
    for files_data in (data.get("response", {}).get("files"), data.get("files")):
        if isinstance(files_data, dict):
            files.update(files_data.keys())
        elif isinstance(files_data, list):
            # If list of dicts with name keys (rare, but some LLMs do this)
            for entry in files_data:
                if isinstance(entry, dict) and "name" in entry:
                    files.add(entry["name"])
    return list(files)

def enquire(args):
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    conversation_file = os.path.join(conversation_dir, f"{args.id}.json")

    # Load or initialize data
    data = {"id": args.id}
    if os.path.exists(conversation_file):
        with open(conversation_file, "r", encoding="utf-8") as f:
            data.update(json.load(f))

    # Update body if prompt provided
    if hasattr(args, 'prompt') and args.prompt:
        data["body"] = args.prompt

    # Compose user prompt from subject and body
    user_prompt = ""
    if "subject" in data and data["subject"]:
        user_prompt += data["subject"] + "\n\n"
    if "body" in data and data["body"]:
        user_prompt += data["body"]

    # Detect what files already exist for this idea
    file_list = files_in_idea(data)

    if not file_list:
        # No files yet: skip analysis step, go straight to solution
        print("No files found for this idea. Skipping 'files needed' step.")
        data["state"] = "updated"
        user_prompt += (
            "\n\nThere are currently **no files** in this project."
            "\nPlease create the initial files needed for this idea, as described above."
        )
        # Optionally add format_instructions if using prompt-template.json
        template_path = os.path.join(repo_path, "../prompt-template.json")
        template_content = load_template(template_path)
        format_instr = build_format_instructions(template_content)
        lm_prompt = user_prompt + format_instr
        data["prompt"] = lm_prompt
    else:
        # Files exist: ask which files are needed for the analysis step
        data["state"] = "analysis requested"
        user_prompt += (
            "\n\nWhich of these files would you need to see to answer the following prompt?\n"
            f"{file_list}\n"
            "Respond with a JSON list of filenames."
        )
        template_path = os.path.join(repo_path, "../prompt-template.json")
        template_content = load_template(template_path)
        format_instr = build_format_instructions(template_content)
        lm_prompt = user_prompt + format_instr
        data["prompt"] = lm_prompt

    # Write updated conversation file
    with open(conversation_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Copy to clipboard
    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(data["prompt"])
            print(f"LLM prompt copied to clipboard! Length: {len(data['prompt'])} characters")
        except pyperclip.PyperclipException as e:
            print(f"Warning: Could not copy to clipboard: {e}")
    else:
        print("Warning: pyperclip not installed. Cannot copy to clipboard.")

    if hasattr(args, 'output') and args.output:
        output_data = {"conversation": data, "prompt": data["prompt"]}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
