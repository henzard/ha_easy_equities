---
description: "Documentation standards and requirements"
alwaysApply: true
---

# Documentation Standards

## Required Documentation Files
- **`README.md`** - Main project documentation (required for HACS)
- **`CHANGELOG.md`** - Version history and changes
- **`CONTRIBUTING.md`** - Contribution guidelines
- **`SECURITY.md`** - Security policy
- **`info.md`** - HACS integration info (optional but recommended)
- **`LICENSE`** - License file

## README.md Requirements
- Clear project description
- Installation instructions (HACS and manual)
- Configuration guide
- Feature list
- Troubleshooting section
- Requirements
- Credits and acknowledgments

## Documentation Style
- Use clear, concise language
- Include code examples where helpful
- Use proper markdown formatting
- Include screenshots for UI features (if applicable)
- Keep documentation up to date with code changes

## Code Comments
- Use docstrings for all public functions and classes
- Follow Google or NumPy docstring style
- Include parameter descriptions and return types
- Document complex logic with inline comments

## Changelog Format
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Use semantic versioning
- Group changes by type (Added, Changed, Fixed, Removed)
- Include dates for releases

## Translation Files
- Keep `strings.json` and `translations/en.json` in sync
- Use clear, user-friendly error messages
- Avoid technical jargon in user-facing strings
