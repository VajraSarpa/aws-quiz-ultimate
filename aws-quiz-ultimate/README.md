# 🎓 AWS Cloud Institute Quiz - Ultimate Study Tool

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)

**A comprehensive, interactive Python quiz application for mastering the AWS Cloud Institute Developer Fundamentals course**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 📖 About

AWS Cloud Institute Quiz is a **feature-rich, gamified study tool** designed to help you master the AWS Cloud Institute Developer Fundamentals course. With 150+ questions, real coding challenges, an achievement system, and comprehensive progress tracking, it's everything you need to ace your AWS certification.

### 🎯 Why This Quiz?

- **🔨 Real Code Execution** - Write and test actual Python code
- **🏆 15+ Achievements** - Stay motivated with unlockable badges
- **📊 Smart Analytics** - Track progress with detailed statistics
- **⏰ Multiple Quiz Modes** - Practice, timed, flashcard, and review modes
- **👥 Multi-User Support** - Separate profiles for multiple learners
- **💾 Progress Tracking** - Never lose your learning progress
- **🎮 Gamified Learning** - Streaks, achievements, and rewards
- **📚 150+ Questions** - Comprehensive coverage of all 10 weeks

---

## ✨ Features

### 📚 Comprehensive Content
- **150+ Questions** across 10 weeks of AWS Cloud Institute curriculum
- **Multiple Question Types**: Multiple choice, True/False, code output, fill-in-the-blank
- **3 Difficulty Levels**: Beginner → Intermediate → Advanced
- **Complete Coverage**: Python basics through serverless applications

### 🎮 Quiz Modes
- **📖 Practice by Week** - Focus on specific topics
- **🎲 Random Quiz** - Mixed questions for general review
- **⏰ Timed Quiz** - Exam simulation with countdown timers
- **📝 Flashcard Mode** - Quick review for memorization
- **❌ Review Mode** - Master your incorrect answers

### 🔨 Coding Challenges
- **Live Code Execution** - Write real Python code that gets tested
- **Automated Testing** - Instant feedback with multiple test cases
- **Hints & Solutions** - Get help when stuck
- **Real-World Problems** - Practical programming exercises

### 🏆 Achievement System
- **15+ Unlockable Badges** - From "First Steps" to "Champion"
- **Streak Tracking** - Build momentum with consecutive correct answers
- **Milestone Rewards** - Celebrate your progress
- **Progress Visualization** - See your journey

### 📊 Advanced Analytics
- **Detailed Statistics** - Overall and per-week performance
- **Visual Progress Bars** - Color-coded accuracy tracking
- **Study Recommendations** - AI-driven suggestions for improvement
- **Weak Area Identification** - Focus on topics that need work
- **CSV Export** - Analyze progress externally

### 👥 Multi-User Support
- **Unlimited Profiles** - Perfect for families or study groups
- **Separate Progress** - Each user has independent tracking
- **Easy Switching** - Change profiles instantly
- **Individual Achievements** - Everyone earns their own badges

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required!

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aws-quiz-ultimate.git

# Navigate to the directory
cd aws-quiz-ultimate

# Run the quiz
python3 aws_quiz_ultimate.py
```

### First Time Setup

1. Run the application
2. Create your user profile when prompted
3. Start with Week 1 or try a Random Quiz!

```bash
python3 aws_quiz_ultimate.py
```

---

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 3 minutes
- **[User Guide](docs/USER_GUIDE.md)** - Complete documentation
- **[Feature Overview](docs/FEATURES.md)** - All features explained
- **[Contributing Guide](CONTRIBUTING.md)** - Help improve the project

---

## 📸 Screenshots

### Main Menu
```
╔═══════════════════════════════════════════════════════════╗
║   AWS CLOUD INSTITUTE - DEVELOPER FUNDAMENTALS QUIZ       ║
║                  Interactive Study Tool                    ║
╚═══════════════════════════════════════════════════════════╝

Welcome, Alex!
Questions Answered: 87 | Accuracy: 81.6% | Streak: 5

MAIN MENU
  1. 📚 Practice by Week (1-10)
  2. 🎲 Random Quiz
  3. 🔨 Coding Challenges
  4. 📝 Flashcard Mode
  5. ❌ Review Incorrect Answers
  6. 📊 View Progress & Stats
  7. 🏆 Achievements
  8. ⏰ Timed Quiz Mode
  9. ⏱️  Pomodoro Study Timer
  10. 💾 Export Progress to CSV
  11. ⚙️  Settings
  12. 🚪 Exit
```

### Quiz Question
```
Question 5/10
Current Score: 4/4

[Intermediate] Week 2

What does the 'break' statement do in a loop?

A) Skips the current iteration
B) Exits the loop completely
C) Restarts the loop
D) Pauses the loop

Your answer (A/B/C/D) [H for hint, S to skip]: B

✓ CORRECT!

💡 Explanation: The 'break' statement immediately exits 
the innermost loop.

🔥 Streak: 5!
```

### Progress Stats
```
══════════════════════════════════════════════
          USER STATISTICS
══════════════════════════════════════════════

Overall Performance:
  Total Questions: 87
  Correct Answers: 71
  Accuracy: 81.6%

Progress by Week:
  Week  1: ████████████████░░░░ 82.5% (33/40)
  Week  2: ██████████████████░░ 88.9% (24/27)
  Week  3: ████████░░░░░░░░░░░░ 42.9% (6/14)
```

---

## 🎓 Course Coverage

| Week | Topics | Questions |
|------|--------|-----------|
| 1 | Python Basics | 15+ |
| 2 | Control Flow | 15+ |
| 3 | Lists & APIs | 15+ |
| 4 | Dictionaries & Functions | 15+ |
| 5 | Files & Error Handling | 15+ |
| 6 | Object-Oriented Programming | 15+ |
| 7 | Git & Version Control | 15+ |
| 8 | Databases (SQL & DynamoDB) | 15+ |
| 9 | Cloud Storage (S3 & Textract) | 15+ |
| 10 | Serverless (Lambda & API Gateway) | 15+ |

---

## 🎯 Usage Examples

### Practice a Specific Week
```bash
# Start the quiz and select option 1
python3 aws_quiz_ultimate.py

# Choose week (1-10)
# Answer questions and get instant feedback!
```

### Try a Coding Challenge
```python
# Select option 3 from main menu
# Write actual Python code
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Code gets tested automatically!
# ✓ All tests passed!
```

### Review Your Mistakes
```bash
# Select option 5 - Review Incorrect Answers
# Quiz only shows questions you got wrong
# Master them to remove from review list
```

---

## 🏆 Achievement System

Unlock achievements as you progress:

| Achievement | Description | Requirement |
|------------|-------------|-------------|
| 🎯 First Steps | Answer first question correctly | 1 correct |
| 🔥 Hot Streak | 5 correct in a row | 5 streak |
| 📚 Scholar | 50 correct answers | 50 correct |
| 🎓 Master | 100 correct answers | 100 correct |
| 🏆 Champion | 200 correct answers | 200 correct |
| 🔨 Code Warrior | Complete 10 coding challenges | 10 challenges |
| 💯 Perfectionist | 5 perfect quizzes | 100% x5 |

[See all 15+ achievements](docs/FEATURES.md#achievement-system)

---

## 💾 Data & Privacy

- **Local Storage**: All data stored locally in JSON format
- **No Internet Required**: Works completely offline
- **Privacy First**: No tracking, no accounts, no data collection
- **Easy Backup**: Simple file-based storage
- **Export Options**: CSV export for external analysis

---

## 🛠️ Technical Details

### Built With
- **Python 3.7+** - Core language
- **Standard Library Only** - No external dependencies
- **Cross-Platform** - Windows, macOS, Linux

### Architecture
- **Object-Oriented Design** - Clean, modular code
- **JSON Storage** - Human-readable data format
- **Automated Testing** - For coding challenges
- **Error Handling** - Robust and user-friendly

### Project Structure
```
aws-quiz-ultimate/
├── aws_quiz_ultimate.py    # Main application
├── docs/                    # Documentation
│   ├── USER_GUIDE.md
│   ├── QUICK_START.md
│   └── FEATURES.md
├── examples/                # Example outputs
│   └── sample_quiz_data.json
├── README.md               # This file
├── LICENSE                 # MIT License
└── CONTRIBUTING.md         # Contribution guidelines
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 **Report Bugs** - Found an issue? Let us know!
- ✨ **Suggest Features** - Have an idea? Share it!
- 📝 **Add Questions** - More questions = better learning
- 🔨 **Create Challenges** - Add coding exercises
- 📖 **Improve Docs** - Help others learn faster
- 🌍 **Translations** - Make it accessible to everyone

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

## 📞 Support

- 📖 [Read the Docs](docs/)
- 💬 [Open an Issue](https://github.com/yourusername/aws-quiz-ultimate/issues)
- 🤝 [Contribute](CONTRIBUTING.md)

---

## 🎉 Acknowledgments

- AWS Cloud Institute for the excellent course curriculum
- The Python community for amazing tools and libraries
- All contributors who help improve this project

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/aws-quiz-ultimate?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/aws-quiz-ultimate?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/aws-quiz-ultimate?style=social)

---

<div align="center">

**Made with ❤️ for AWS Cloud Institute students**

[⬆ Back to Top](#-aws-cloud-institute-quiz---ultimate-study-tool)

</div>
