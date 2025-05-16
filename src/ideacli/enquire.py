"""Prepare an idea with prompt for LLM input."""

import os
import json
from ideacli.repository import resolve_idea_path

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

def load_template(template_path):
    """Load prompt template from JSON file."""
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: prompt-template.json is not valid JSON: {e}")
    return None

def build_format_instructions(template):
    """Construct format instructions from template content."""
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

def enquire(args):
    """Generate prompt and augment idea with template content."""
    repo_path = resolve_idea_path(args)
    conversation_dir = os.path.join(repo_path, "conversations")
    os.makedirs(conversation_dir, exist_ok=True)
    conversation_file = os.path.join(conversation_dir, f"{args.id}.json")

    data = {"id": args.id}
    if os.path.exists(conversation_file):
        with open(conversation_file, "r", encoding="utf-8") as f:
            data.update(json.load(f))

    if hasattr(args, 'prompt') and args.prompt:
        data["body"] = args.prompt

    user_prompt = ""
    if "subject" in data and data["subject"]:
        user_prompt += data["subject"] + "\n\n"
    if "body" in data and data["body"]:
        user_prompt += data["body"]

    template_path = os.path.join(repo_path, "../prompt-template.json")
    template_content = load_template(template_path)
    format_instr = build_format_instructions(template_content)
    lm_prompt = user_prompt + format_instr
    data["prompt"] = lm_prompt

    with open(conversation_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(lm_prompt)
            print(f"LLM prompt copied to clipboard! Length: {len(lm_prompt)} characters")
        except pyperclip.PyperclipException as e:
            print(f"Warning: Could not copy to clipboard: {e}")
    else:
        print("Warning: pyperclip not installed. Cannot copy to clipboard.")

    if hasattr(args, 'output') and args.output:
        output_data = {"conversation": data, "prompt": lm_prompt}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
