# ideacli - LLM Conversations Manager
[![PyPI version](https://badge.fury.io/py/ideacli.svg)](https://badge.fury.io/py/ideacli)
<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/maw71luh2fj9v3f4u4um" alt="trackgit-views" />
</a>

> **Note:** For details on our focused proof-of-concept (POC) approach and implementation plan, please see [POC-APPROACH.md](POC-APPROACH.md).

## Core Concept
- A CLI tool to manage insights and conversations from multiple LLMs
- Using Git as the backend for version control and storage
- Clipboard integration for cross-LLM compatibility without requiring direct APIs
- Potential for seamless GitLab integration for enterprise environments

## Interface Design
- Simple subject/body format for basic input
- First line treated as subject line (used for ID generation)
- Remaining lines as the body content
- Support for both interactive prompts and piped input
- Progressive enhancement with optional JSON input for advanced metadata

## ID System
- Generate human-readable IDs from the subject line
- Ensure uniqueness and sufficient difference between IDs
- Use string distance algorithms (via textdistance library) to verify ID distinctiveness
- Return ID to user and copy to clipboard for easy reference

## Implementation Approach
- Focus on getting the Create operation (add verb) solid first
- Split into focused modules for maintainability
- Hide implementation details (.ideas_repo)
- Make complex features optional but available
- Support command line args to modify behavior (tags, overwrite options)

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/magicalbob/ideacli.git
cd ideacli

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Now you can run the tool from anywhere
ideacli --help
```

or alternatively just install one of the releases:
```bash
pip install git+https://github.com/magicalbob/ideacli@v0.1.1
```

### Requirements
- Python 3.6 or higher
- Git

## Usage
```bash
# Initialize a new ideas repository
ideacli init

# Check the status of your ideas repository
ideacli status

# Add a new idea
ideacli add
Subject: A big idea
Body (end with CTRL+D on empty line):
Do something marvelous.
Do it today!
[main 5e23bb5] Add idea: 7a7b3a7d - A big idea
 1 file changed, 5 insertions(+)
 create mode 100644 conversations/7a7b3a7d.json
Copied to clipboard!
Idea 'A big idea' saved as 7a7b3a7d and committed.

# List your old ideas
ideacli list
[7a7b3a7d] A big idea
[05ee8e27] Another idea
[a7ba4d6f] Fourth time around
[f12e4337] My new idea
[7a1e34c5] Third idea

# Show an idea
ideacli show --id 7a1e34c5
Subject: Third idea

Body:
Let use see the count.

# More commands coming soon...
```

## Using `prompt-template.json` for Flexible File Generation

### What is `prompt-template.json`?

`prompt-template.json` is a configuration file that defines the structure and instructions for how LLMs (Large Language Models) should respond to your `ideacli enquire` requests. It acts as a *contract* between you and the LLM, ensuring that responses are in a machine-readable JSON format and contain exactly the files and data you need.

### Where does it live?

Place your `prompt-template.json` in the **root** of your project directory (typically alongside your `.ideas_repo` and source folders). `ideacli enquire` will automatically pick it up and use it to generate LLM prompts.

* * * * *

### Flexible File Generation with LLMs

With the right `prompt-template.json`, you can specify *any* set of output files---Python code, Markdown docs, configs, tests, etc.---in a single LLM round-trip.

#### How it Works

-   The prompt template defines the **structure and constraints** of LLM responses.

-   `ideacli enquire` uses this template to generate a JSON prompt, which is put on your clipboard, ready for pasting into your LLM of choice (e.g., ChatGPT, Claude, Gemini).

-   The LLM's response, in turn, can be parsed by `ideacli update` and its files extracted to your project.

* * * * *

#### Example: Recommended Generalized Template

Below is a flexible `prompt-template.json` you can use for almost any file-generation task:

```json
{
  "format_instructions": {
    "description": "Please respond ONLY with a valid JSON object, containing an object property named 'files' whose keys are filenames (with appropriate extensions), and whose values are the full file contents as strings. Include a property 'approaches' describing your methodology and a 'conclusion' summarizing the output.",
    "expected_structure": {
      "approaches": {
        "description": "Approach methodology for creating the requested files"
      },
      "files": {
        "example.py": "# Python file content here",
        "example.json": "{\"title\": \"Story\", \"content\": \"...\"}",
        "README.md": "# Documentation here"
      },
      "conclusion": "Summary of the provided files"
    },
    "important_notes": [
      "Your entire response must be a valid JSON object",
      "The 'files' property must include a file for each requested topic",
      "Each file must have content appropriate for its extension",
      "Do not include any text outside the JSON structure"
    ]
  }
}
```

* * * * *

#### Example Workflow

1.  **Edit or create your `prompt-template.json`** as above, tailored for your desired output files.

2.  **Run:**

```bash
ideacli enquire --prompt "Create a Python MVP for the Unspiked app. Please output: app.py (Flask app), requirements.txt, README.md." --id myproj1
```

3.  **Paste the generated prompt into your LLM** (such as ChatGPT or Claude).

4.  **Copy the LLM's JSON response** to your clipboard.

5.  **Run:**

```bash
ideacli update --id myproj1
ideacli files --id myproj1
ideacli extract --id myproj1
```

6.  You'll now have real files: `app.py`, `requirements.txt`, `README.md`, etc., with content generated directly by the LLM.

---

#### Tips

-   Be explicit in your prompt about filenames and formats; the LLM will follow your lead.

-   You can generate multi-file Python projects, config folders, tests, or documentation in one go.

-   Update your template or prompt for more advanced cases (e.g., subdirectories, extra constraints).

-   You may keep multiple `prompt-template.json` variants for different workflows.

---

#### Why this Works

-   The generalized template gives the LLM maximum flexibility and you maximum control over the resulting project structure and content.

-   The process is robust, extensible, and works with any modern AI assistant.

-   `prompt-template.json` is the key to unlocking this power---customize it to suit your project or team conventions.

---

**What happens if prompt-template.json is missing?**\
If prompt-template.json is absent from your project, ideacli enquire will generate a basic prompt containing only your own request text (with no format instructions or schema).
This is fine for informal use, but to reliably automate file extraction and multi-file workflows, you should provide an explicit template.
A present and well-formed prompt-template.json ensures LLM outputs are always in a predictable, machine-readable format for the update and extract steps.

## Next Steps
- ~Complete the 'add' verb with ID generation~
- ~Add a show command (R from CRUD)~
- ~Add an enquire command. Display the current idea as a JSON object with an extra prompt to tell the LLM what is required. Place the JSON in the paste buffer ready for copying to the chosen LLM(s). (one version of U from CRUD)~
- ~Add an update command. Take info from the paste buffer and use it to update an idea. This is the stage after an enquire (where the LLM has responded to the enquiry. Implies that as well as the prompt added by the enquire, the enquire should also include context in its JSON output to ensure [as much as one can] that the LLM's reply will include the idea Id). (the second part of the U from CRUD).~
- Add an import command to make a file appear in the ideacli files for an idea.
- Add a delete command to delete a particular idea. This could be a hard or soft delete? Either completely removing the idea from .ideas_repo or just marking that it is no longer being pursued?
- Implement optional agile object types:
  - Add configuration to enable/disable "agile mode" for a repository
  - Support agile object types (epic, story, task, subtask) with appropriate metadata
  - Implement relationship tracking between agile objects (parent/child connections)
  - Add agile-specific fields like priority, size/points, status, acceptance criteria
  - Create views for visualizing agile hierarchies and relationships
  - Support filtering and reporting on agile objects (by type, status, priority)
  - Ensure backward compatibility with standard idea objects
- Develop REST API and web frontend:
  - Refactor ideacli to separate core logic from CLI interface
  - Create a REST API layer (Flask/FastAPI) that uses ideacli's core functions
  - Design API endpoints that map to ideacli commands (add, show, list, etc.)
  - Build a web frontend that communicates exclusively through the REST API
  - Implement Kanban-style board views for visualizing workflow
  - Add drag-and-drop functionality for status updates
  - Design dashboard with metrics and reporting capabilities
  - Support user authentication and permission levels
  - Ensure real-time updates when multiple users are active
  - Add API documentation and client SDKs for third-party integrations
- Experiment with different ID creation algorithms
- Implement distance checking between IDs
- Add support for detecting and parsing JSON input
- Consider search capabilities leveraging Git's features
- Pretty Table - Columnize ID and Subject nicely, align them
- Sorted by subject     - Allow --sort subject (instead of ID)
- Show created date     - Read file mtime (os.stat) and show it
- Full body preview     - Add --long to show the body text under each item
- Tagging support - add tags come / display tags next to ideas
- Pagination - --page 1 to show 10 ideas at a time
- Export - ideacli list --json dumps the list to a JSON array
- Implement secure sharing infrastructure with end-to-end encryption:
  - Enable repository sharing via GitHub with built-in encryption
  - Support "bring your own key" (BYOK) model for user-controlled encryption
  - Implement key exchange mechanisms for authorized collaborators
  - Ensure all idea content remains encrypted at rest and in transit
  - Add granular access controls using GitHub's fine-grained permission system
  - Create commands for managing shared encrypted repositories
  - Provide options for local-only keys vs. team-shared encryption keys

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
