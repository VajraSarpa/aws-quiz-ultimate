# Installation & Setup Guide

Complete guide for installing and setting up AWS Quiz Ultimate on your system.

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [First-Time Setup](#first-time-setup)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## 💻 System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **OS**: Windows 7+, macOS 10.12+, or Linux (any recent distro)
- **Disk Space**: 5 MB
- **RAM**: 100 MB (minimal)
- **Terminal**: Any terminal/command prompt with color support

### Recommended
- **Python**: 3.9 or higher
- **Terminal**: Modern terminal with full color support
  - Windows: Windows Terminal, PowerShell 7+
  - macOS: iTerm2, default Terminal
  - Linux: GNOME Terminal, Konsole, etc.

---

## 📥 Installation Methods

### Method 1: Git Clone (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/aws-quiz-ultimate.git

# 2. Navigate to directory
cd aws-quiz-ultimate

# 3. Run the quiz
python3 aws_quiz_ultimate.py
```

**Advantages:**
- Easy to update
- Get latest features quickly
- Contribute back easily

---

### Method 2: Download ZIP

1. Go to: https://github.com/yourusername/aws-quiz-ultimate
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file
5. Open terminal in the extracted folder
6. Run: `python3 aws_quiz_ultimate.py`

**Advantages:**
- No Git required
- Simple download
- Works offline immediately

---

### Method 3: Download Release

1. Go to: https://github.com/yourusername/aws-quiz-ultimate/releases
2. Download the latest `aws-quiz-ultimate-vX.X.X.zip`
3. Extract the archive
4. Run: `python3 aws_quiz_ultimate.py`

**Advantages:**
- Stable versions only
- Changelog included
- Tagged versions

---

## ⚙️ First-Time Setup

### Step 1: Verify Python Installation

```bash
# Check Python version
python3 --version

# Should show: Python 3.7.x or higher
```

**If Python is not installed:**
- **Windows**: Download from https://python.org
- **macOS**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) or equivalent

---

### Step 2: Run the Quiz

```bash
# From the aws-quiz-ultimate directory
python3 aws_quiz_ultimate.py
```

**On Windows**, you might need:
```bash
python aws_quiz_ultimate.py
```

---

### Step 3: Create Your Profile

On first run, you'll see:
```
╔═══════════════════════════════════════════════════════════╗
║   AWS CLOUD INSTITUTE - DEVELOPER FUNDAMENTALS QUIZ       ║
╚═══════════════════════════════════════════════════════════╝

Enter your name: _
```

1. Type your name
2. Press Enter
3. Your profile is created!

---

### Step 4: Start Learning

Choose from the main menu:
- Start with **Option 1: Practice by Week** → Week 1
- Or try **Option 2: Random Quiz** to explore

---

## 🔄 Updating

### If Installed via Git

```bash
# Navigate to quiz directory
cd aws-quiz-ultimate

# Pull latest changes
git pull origin main

# Run the updated version
python3 aws_quiz_ultimate.py
```

**Your progress is preserved!** The `quiz_data.json` file is not affected by updates.

---

### If Installed via ZIP/Download

1. Backup your `quiz_data.json` file (contains your progress)
2. Download the new version
3. Extract to a new folder
4. Copy your `quiz_data.json` to the new folder
5. Run the new version

---

## 🐛 Troubleshooting

### Issue: "python3: command not found"

**Solution:**
```bash
# Try just "python" instead
python aws_quiz_ultimate.py

# Or check if Python is in PATH
where python     # Windows
which python3    # macOS/Linux
```

---

### Issue: Colors Not Displaying (Windows)

**Solution 1:** Use Windows Terminal (recommended)
- Download from Microsoft Store
- Modern color support

**Solution 2:** Update PowerShell
```bash
# Install PowerShell 7
winget install Microsoft.PowerShell
```

**Solution 3:** Run in Windows Terminal
- Right-click folder
- "Open in Windows Terminal"

---

### Issue: "ModuleNotFoundError" or Import Errors

**This shouldn't happen** as the quiz uses only standard library.

**If it does:**
1. Verify Python version: `python3 --version`
2. Ensure Python 3.7+
3. Try reinstalling Python
4. Check file integrity (re-download if needed)

---

### Issue: Permission Denied

**macOS/Linux:**
```bash
# Make file executable
chmod +x aws_quiz_ultimate.py

# Run directly
./aws_quiz_ultimate.py
```

**Windows:**
- Right-click file → Properties
- Uncheck "Read-only" if checked

---

### Issue: Can't Save Progress

**Causes:**
- No write permission in directory
- Disk full
- Antivirus blocking

**Solutions:**
```bash
# Check directory permissions
ls -la    # macOS/Linux
dir       # Windows

# Run from home directory instead
cd ~
python3 /path/to/aws_quiz_ultimate.py
```

---

### Issue: Quiz Freezes or Crashes

**Solutions:**
1. Check Python version (need 3.7+)
2. Try different terminal
3. Check for background processes
4. Restart terminal
5. Re-download file (may be corrupted)

---

### Issue: Questions Not Loading

**Solutions:**
1. Verify file is complete (should be ~90KB)
2. Re-download if file is incomplete
3. Check for syntax errors if you modified the file
4. Use fresh copy from repository

---

## 🗑️ Uninstallation

### To Completely Remove

```bash
# Navigate to parent directory
cd ..

# Remove quiz directory
rm -rf aws-quiz-ultimate    # macOS/Linux
rmdir /s aws-quiz-ultimate  # Windows
```

### To Preserve Your Progress

```bash
# Copy your data first
cp aws-quiz-ultimate/quiz_data.json ~/backup/

# Then remove
rm -rf aws-quiz-ultimate
```

Your progress file `quiz_data.json` contains all your data.

---

## 📁 File Locations

### Main Files
- `aws_quiz_ultimate.py` - Main application
- `quiz_data.json` - Your progress (auto-created)
- `quiz_progress_*.csv` - Exported stats (if you export)

### Documentation
- `README.md` - Main documentation
- `docs/USER_GUIDE.md` - Complete user guide
- `docs/QUICK_START.md` - Quick start guide
- `docs/FEATURES.md` - Feature documentation

### Configuration
- `.gitignore` - Git ignore rules (if using Git)
- `LICENSE` - MIT License
- `CONTRIBUTING.md` - Contribution guidelines

---

## 🔐 Data & Privacy

### Where is Your Data Stored?

All data is stored locally in:
```
aws-quiz-ultimate/quiz_data.json
```

### What Data is Stored?

- Your name
- Questions answered
- Correct/incorrect answers
- Study dates
- Achievements earned
- Per-week statistics

### Privacy

- ✅ 100% local storage
- ✅ No internet connection required
- ✅ No external servers
- ✅ No tracking or analytics
- ✅ You control your data

---

## 🎯 Quick Command Reference

```bash
# Install
git clone https://github.com/yourusername/aws-quiz-ultimate.git
cd aws-quiz-ultimate

# Run
python3 aws_quiz_ultimate.py

# Update (if using Git)
git pull origin main

# Backup data
cp quiz_data.json quiz_data.backup.json

# Check Python version
python3 --version
```

---

## 💡 Tips for Best Experience

### Terminal Recommendations

**Windows:**
- ✅ Windows Terminal (best)
- ✅ PowerShell 7+
- ⚠️ Command Prompt (basic colors)

**macOS:**
- ✅ iTerm2 (best)
- ✅ Default Terminal (good)
- ✅ Hyper (good)

**Linux:**
- ✅ GNOME Terminal (best)
- ✅ Konsole (best)
- ✅ Terminator (good)
- ✅ Any modern terminal

---

### Font Recommendations

For best emoji and icon display:
- **Windows**: Cascadia Code, Consolas
- **macOS**: SF Mono, Monaco
- **Linux**: DejaVu Sans Mono, Ubuntu Mono

---

## 📞 Need Help?

### Resources
- 📖 [User Guide](docs/USER_GUIDE.md)
- 🚀 [Quick Start](docs/QUICK_START.md)
- ❓ [Open an Issue](https://github.com/yourusername/aws-quiz-ultimate/issues)

### Common Solutions
1. **Update Python** to latest 3.x version
2. **Use modern terminal** with color support
3. **Check permissions** in directory
4. **Re-download file** if corrupted
5. **Read error messages** carefully

---

## ✅ Verification Checklist

After installation, verify:
- [ ] Python 3.7+ installed
- [ ] Quiz file runs without errors
- [ ] Colors display correctly
- [ ] Can create user profile
- [ ] Progress saves correctly
- [ ] Can answer questions
- [ ] Can access all menu options

If all checked, you're ready to learn! 🎉

---

## 🎓 Next Steps

1. ✅ Complete installation
2. ✅ Create your profile
3. ✅ Start with Week 1
4. ✅ Try a coding challenge
5. ✅ Check your achievements
6. ✅ Review your progress

**Happy studying!** 🚀

---

*Last updated: 2024-11-24*
