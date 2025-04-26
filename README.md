# ideacli - LLM Conversations Manager

## Core Concept
- A CLI tool to manage insights and conversations from multiple LLMs
- Using Git as the backend for version control and storage
- Clipboard integration for cross-LLM compatibility without requiring direct APIs

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

## Next Steps
- ~Complete the 'add' verb with ID generation~
- ~Add a show command (R from CRUD)~
- Add an enquire command. Display the current idea as a JSON object with an extra prompt to tell the LLM what is required. Place the JSON in the paste buffer ready for copying to the chosen LLM(s). (one version of U from CRUD)
- Add an update command. Take info from the paste buffer and use it to update an idea. This is the stage after an enquire (where the LLM has responded to the enquiry. Implies that as well as the prompt added by the enquire, the enquire should also include context in its JSON output to ensure [as much as one can] that the LLM's reply will include the idea Id). (the second part of the U from CRUD).
- Add a delete command to delete a particular idea. This could be a hard or sof delete? Either completely removing the idea from .ideas_repo or just marking that it is no longer being pursued?
- Experiment with different ID creation algorithms
- Implement distance checking between IDs
- Add support for detecting and parsing JSON input
- Consider search capabilities leveraging Git's features
- Pretty Table - Columnize ID and Subject nicely, align them
- Sorted by subject	- Allow --sort subject (instead of ID)
- Show created date	- Read file mtime (os.stat) and show it
- Full body preview	- Add --long to show the body text under each item
- Tagging support - add tags come / display tags next to ideas
- Pagination - --page 1 to show 10 ideas at a time
- Export - ideacli list --json dumps the list to a JSON array

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
