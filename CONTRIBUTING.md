# Contributing to Discord Clone

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the Discord Clone project.

## Code of Conduct

- Be respectful and inclusive
- No harassment, discrimination, or abusive behavior
- Focus on constructive feedback
- Help each other learn and grow

## Ways to Contribute

### 1. Report Bugs
- Check existing issues first
- Provide detailed description
- Include steps to reproduce
- Share error messages/logs
- Mention your OS and versions

### 2. Suggest Features
- Describe the problem/use case
- Explain your proposed solution
- Provide examples if possible
- Check for related existing issues

### 3. Submit Code

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/Discord-clone.git
cd Discord-clone

# Run setup script
# On macOS/Linux:
chmod +x setup.sh
./setup.sh

# On Windows:
setup.bat
```

#### Making Changes

1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly

3. Commit with clear messages
```bash
git commit -m "Add feature: description of changes"
```

4. Push to your fork
```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request
   - Describe changes clearly
   - Reference related issues
   - Include screenshots if UI changes

## Development Guidelines

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions/classes
- Test new endpoints with curl or Postman
- Update requirements.txt with new packages

### Frontend (TypeScript/React)

- Use TypeScript for type safety
- Follow React best practices
- Use components for reusability
- Keep components focused and small
- Write clear variable/function names
- Use Zustand for state management

### Database

- Use SQLAlchemy ORM
- Add migrations for schema changes
- Update models.py with schema changes
- Add indexes for query performance

## Testing

Before submitting PR:

### Backend
```bash
cd backend
source venv/bin/activate
# Manual API testing
curl -X GET http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm run build  # Check for build errors
npm run lint   # Check for linting issues
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to code
- Update API docs in code comments
- Include examples for new features

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Refactoring
- `perf:` Performance
- `test:` Tests

Example:
```
feat: Add file upload support to messages

- Implement POST /channels/{id}/upload endpoint
- Add file input to message input area
- Display file previews in chat
- Store files in uploads/ directory

Closes #42
```

## Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure code follows style guide
4. Fill out PR template completely
5. Link related issues
6. Wait for code review
7. Address feedback
8. Maintain clean commit history

## Questions?

- Open a discussion issue
- Comment on related issues
- Check existing documentation
- Review code examples

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in project

Thank you for contributing! 🎉
