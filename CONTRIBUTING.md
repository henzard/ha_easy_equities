# Contributing to Easy Equities Home Assistant Integration

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ha_easy_equities.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

1. Install Home Assistant development environment
2. Copy the `custom_components/easy_equities` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Make your changes

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing

Before submitting a pull request:

1. Test your changes in a Home Assistant instance
2. Check for linting errors: `pylint custom_components/easy_equities`
3. Ensure all sensors update correctly
4. Test error handling scenarios

## Submitting Changes

1. Commit your changes with clear, descriptive commit messages
2. Push to your fork
3. Create a pull request with:
   - A clear title and description
   - Reference to any related issues
   - Screenshots if UI changes are involved

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation if needed
3. Add tests if applicable
4. Update CHANGELOG.md with your changes
5. Wait for review and address any feedback

## Questions?

If you have questions, please open an issue for discussion.

Thank you for contributing!
