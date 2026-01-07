# Contributing to AWS Quiz Ultimate

First off, thank you for considering contributing to AWS Quiz Ultimate! 🎉

It's people like you that make this tool better for everyone studying for the AWS Cloud Institute.

## 🌟 Ways to Contribute

### 1. Report Bugs 🐛

Found a bug? Please open an issue with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Your Python version and OS
- Any error messages or screenshots

### 2. Suggest Features ✨

Have an idea? We'd love to hear it! Open an issue with:
- Clear description of the feature
- Why it would be useful
- How it might work
- Any examples or mockups

### 3. Add Questions 📝

The more questions, the better! To add questions:

```python
# In create_question_database() function:
Question(
    week=1,                    # Week number (1-10)
    difficulty='Beginner',     # Beginner, Intermediate, or Advanced
    q_type='MCQ',             # MCQ, TrueFalse, FillBlank, CodeOutput
    question='Your question here?',
    options=['A', 'B', 'C', 'D'],  # For MCQ
    correct='B',              # Correct answer
    explanation='Why this is correct...',
    hint='Optional hint'
)
```

**Guidelines for Questions:**
- ✅ Must be relevant to AWS Cloud Institute curriculum
- ✅ Should have clear, unambiguous answers
- ✅ Must include detailed explanations
- ✅ Hints should guide without giving away the answer
- ✅ Test your question before submitting!

### 4. Create Coding Challenges 🔨

Add hands-on coding exercises:

```python
# In create_coding_challenges() function:
CodingChallenge(
    week=3,
    title="Your Challenge Name",
    description="Clear problem description",
    example_input="[1, 2, 3]",
    example_output="[3, 2, 1]",
    hint="Helpful hint without solution",
    test_cases=[
        (([1, 2, 3],), [3, 2, 1]),
        (([],), []),
        # Add more test cases
    ],
    solution="def your_solution():\n    ..."
)
```

**Guidelines for Coding Challenges:**
- ✅ Should be solvable in 5-15 minutes
- ✅ Must have at least 3 test cases
- ✅ Include edge cases (empty input, single item, etc.)
- ✅ Provide working solution
- ✅ Difficulty appropriate for the week

### 5. Improve Documentation 📖

Help others learn faster:
- Fix typos or unclear instructions
- Add examples or screenshots
- Improve explanations
- Translate to other languages

### 6. Fix Code Issues 🔧

Found a bug or want to improve the code?
- Write clean, commented code
- Follow existing code style
- Test your changes
- Update documentation if needed

## 🚀 Getting Started

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/aws-quiz-ultimate.git
   cd aws-quiz-ultimate
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

4. **Make your changes**
   - Edit the code
   - Test thoroughly
   - Add/update documentation

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: clear description of your changes"
   ```

6. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Provide clear description of changes
   - Wait for review!

## 📋 Pull Request Guidelines

### Before Submitting

- ✅ Test your changes thoroughly
- ✅ Update documentation if needed
- ✅ Follow the existing code style
- ✅ Make sure the quiz still runs without errors
- ✅ Check for typos and formatting

### PR Description Should Include

- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How did you test it?
- **Screenshots**: If UI changes, include screenshots

### Example PR Description

```markdown
## Add 15 New Week 4 Questions

### What
Adds 15 new questions for Week 4 (Dictionaries & Functions)

### Why
Week 4 only had 10 questions, needed more variety

### Changes
- Added 10 MCQ questions on dictionary methods
- Added 3 questions on lambda functions
- Added 2 advanced questions on *args/**kwargs

### Testing
- Tested all questions in Practice by Week mode
- Verified explanations are clear
- Checked difficulty levels are appropriate

### Questions Added
[List of questions or reference to commits]
```

## 🎨 Code Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Use type hints where appropriate

```python
# Good
def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return (correct / total) * 100

# Not as good
def calc(c, t):
    return (c/t)*100 if t!=0 else 0
```

### Documentation Style

- Use clear, concise language
- Include examples where helpful
- Keep formatting consistent
- Use proper Markdown syntax

## 🐛 Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10, macOS 13, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- Quiz Version: [e.g., 1.0]

**Additional Context**
Any other information about the problem.
```

## ✨ Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like.

**Problem It Solves**
What problem does this feature address?

**Proposed Solution**
How you envision this working.

**Alternatives Considered**
Other solutions you've thought about.

**Additional Context**
Any other information, mockups, or examples.
```

## 🔍 Code Review Process

1. **Submission**: You create a pull request
2. **Review**: Maintainers review your code
3. **Feedback**: You may receive change requests
4. **Revision**: Make requested changes
5. **Approval**: PR is approved
6. **Merge**: Changes are merged into main branch

### What Reviewers Look For

- ✅ Code works correctly
- ✅ Follows project style
- ✅ Includes proper tests
- ✅ Documentation updated
- ✅ No breaking changes
- ✅ Solves stated problem

## 📜 Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add: 10 new Week 8 database questions"
git commit -m "Fix: Streak counter not resetting properly"
git commit -m "Update: README with new features"
git commit -m "Refactor: Simplify question display logic"

# Not as clear
git commit -m "updates"
git commit -m "fixed bug"
git commit -m "changes"
```

### Commit Message Format

```
Type: Brief description

Longer description if needed explaining:
- What changed
- Why it changed
- Any breaking changes
```

**Types:**
- `Add:` New features, questions, challenges
- `Fix:` Bug fixes
- `Update:` Updates to existing features
- `Refactor:` Code improvements without changing behavior
- `Docs:` Documentation changes
- `Test:` Adding or updating tests

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- 🔴 More coding challenges (we need 10+ more!)
- 🔴 Additional questions for Weeks 8-10
- 🔴 Bug fixes and error handling improvements

### Medium Priority
- 🟡 UI/UX improvements
- 🟡 Performance optimizations
- 🟡 Additional quiz modes

### Low Priority
- 🟢 Documentation improvements
- 🟢 Code refactoring
- 🟢 New features

## ❓ Questions?

- 💬 Open an issue with the "question" label
- 📧 Contact the maintainers
- 📖 Check existing documentation

## 🙏 Thank You!

Every contribution, no matter how small, makes a difference. Thank you for helping make AWS Quiz Ultimate better for everyone!

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Happy Contributing! 🎉

**Remember**: Be kind, be respectful, and have fun learning together!
