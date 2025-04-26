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

## Next Steps
- Complete the 'add' verb with ID generation
- Experiment with different ID creation algorithms
- Implement distance checking between IDs
- Add support for detecting and parsing JSON input
- Build out the remaining CRUD operations afterward
- Consider search capabilities leveraging Git's features

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
