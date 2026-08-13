# General Guidelines

## When to Use
*When working with notes, documents, or other data, but not code*

## Medium
- Notes in Markdown or plain text
- CSV or other common structured data formats
- SQLite when appropriate

## Accessibility
- All notes and data should be readable by both humans and machines
- Avoid formats that limit accessibility

## Organization
- Keep files organized in folders so humans can navigate easily
- Use a project-level `CLAUDE.md` file to explain the project's purpose, current status, and key information.
- Use a `TODO.md` file to track tasks and progress
- Use an `INDEX.md` as a quick reference to find specific files
- Keep these files up to date, and read them at startup in case they've changed.

## What to Avoid
- Complex databases or systems unless absolutely necessary
- Proprietary formats or tools
- Unnecessary complexity: Keep things simple and clear!

--------------------------------------------------------------------------------


# Coding Guidelines

## When to Use
*When working with code (generating, reviewing, etc)*

## Communication Style
- Be concise without sacrificing clarity
- For complex explanations, start with a brief summary then go step-by-step
- Briefly state your rationale when making decisions
- Ask for clarification when requirements are ambiguous
- Flag potential issues or trade-offs proactively

## Coding Approach
- Write clean, readable code with clear variable names
- Prioritize simplicity over cleverness
- Add comments for complex logic, not obvious code
- Write quality code even when it differs from existing patterns, but avoid drastic departures that would complicate maintenance.
- Use whitespace for readability (blank lines between blocks, aligned entries, visual grouping)

## Error Handling
- Prioritize reliability over comprehensive edge case coverage
- Ensure errors trigger human notification
- Write clear, actionable error messages without verbosity
- Include contextual data to aid debugging when possible
- Avoid try/catch and try/except blocks unless necessary; let the system handle errors naturally.

## When to Pause and Ask
- Requirements are unclear or conflicting
- Multiple valid approaches exist with different trade-offs
- Changes would significantly impact existing functionality

## Version Control
- Write clear, concise commit messages. Stay under 120 characters. 
- Keep commits focused on a cohesive unit of work
