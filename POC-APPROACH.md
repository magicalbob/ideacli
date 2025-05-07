# ideacli - Proof of Concept Approach

This document outlines the focused proof-of-concept (POC) approach for the ideacli project, detailing the minimal components needed to validate the core architecture before expanding to the full roadmap.

## POC Scope

The POC will demonstrate a working end-to-end system with three integrated components:

1. Core CLI functionality
2. REST API layer
3. Basic web frontend

Advanced features like agile object types, LLM integration, and extensive search capabilities are **explicitly out of scope** for the initial POC.

## Component Breakdown

### 1. ideacli Core (CLI)

Focus on implementing only these essential commands:

- `ideacli init` - Initialize a new ideas repository
- `ideacli add` - Add a new idea with subject/body
- `ideacli list` - List all ideas
- `ideacli show` - Display a single idea by ID

Key implementation considerations:
- Separate core logic from CLI interface for reusability
- Ensure Git operations work correctly for basic storage
- Use simple ID generation algorithm 
- Keep JSON structure minimal but extensible

### 2. REST API Layer

Create a thin API layer that exposes core ideacli functionality:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ideas` | GET | List all ideas |
| `/api/ideas` | POST | Create a new idea |
| `/api/ideas/{id}` | GET | Retrieve a specific idea |

Key implementation considerations:
- Use Flask for simplicity and quick development
- Call ideacli core functions directly (not shell commands)
- Return standardized JSON responses
- Include basic error handling
- Add minimal validation

### 3. Web Frontend

Build a simple, functional web interface:

- Ideas listing page
- Idea detail view
- New idea form
- Basic navigation

Key implementation considerations:
- Use Flask templates for rendering (avoid complex JS frameworks for POC)
- Focus on functionality over design
- Communicate exclusively through the REST API
- Keep styling minimal but usable

## Project Structure

```
ideacli/
  ├── ideacli/
  │   ├── __init__.py
  │   ├── cli/           # CLI-specific code
  │   │   └── commands.py
  │   ├── core/          # Shared core functionality
  │   │   ├── __init__.py
  │   │   ├── repo.py    # Git operations
  │   │   └── ideas.py   # Idea management
  │   ├── api/           # REST API implementation
  │   │   ├── __init__.py
  │   │   ├── app.py
  │   │   └── routes.py
  │   └── web/           # Web frontend
  │       ├── __init__.py
  │       ├── views.py
  │       └── templates/
  ├── setup.py
  ├── requirements.txt
  ├── README.md
  └── POC-APPROACH.md
```

## Development Approach

1. **Refactor existing code** to separate core logic from CLI interface
2. **Implement core CLI commands** if not already completed
3. **Build REST API layer** on top of core functions
4. **Create web frontend** that communicates via the API
5. **Test end-to-end functionality** with a few example ideas

## Success Criteria

The POC will be considered successful when:

- Users can create and view ideas via both CLI and web interface
- All operations persist correctly in the Git repository
- The three layers (CLI, API, web) work together seamlessly
- The architecture demonstrates extensibility for future features

## Estimated Timeline

A single developer working part-time could complete this POC in approximately 3-4 weeks:

- Week 1: Refactor and complete core CLI functionality
- Week 2: Implement REST API layer
- Week 3: Create basic web frontend
- Week 4: Integration testing and refinements

## Next Steps After POC

Once the POC is validated, development will proceed according to the full roadmap in the README.md, with priorities determined by usage patterns and feedback. Initial post-POC priorities may include:

1. Complete remaining CRUD operations (update, delete)
2. Add LLM integration (enquire/response)
3. Implement search capabilities
4. Begin work on agile object types

The POC will provide valuable insights to guide these future development efforts.
