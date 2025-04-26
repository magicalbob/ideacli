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

# More commands coming soon...
```

## Next Steps
- Complete the 'add' verb with ID generation
- Experiment with different ID creation algorithms
- Implement distance checking between IDs
- Add support for detecting and parsing JSON input
- Build out the remaining CRUD operations afterward
- Consider search capabilities leveraging Git's features

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
