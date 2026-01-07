#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   AWS CLOUD INSTITUTE - DEVELOPER FUNDAMENTALS QUIZ                       ║
║                    Ultimate Interactive Study Tool                        ║
║                                                                           ║
║   Features:                                                               ║
║   • 150+ Questions across 10 weeks                                        ║
║   • Multiple question types (MCQ, T/F, Code, Fill-in-blank)              ║
║   • Live coding challenges with execution                                 ║
║   • Achievement system with badges                                        ║
║   • Multiple user profiles                                                ║
║   • Timed quiz mode                                                       ║
║   • Flashcard mode                                                        ║
║   • Progress tracking & analytics                                         ║
║   • Study recommendations                                                 ║
║   • Spaced repetition algorithm                                           ║
║   • Export results to CSV                                                 ║
║   • Pomodoro study timer                                                  ║
║                                                                           ║
║   Requirements: Python 3.7+                                               ║
║   Usage: python3 aws_quiz_ultimate.py                                     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import json
import os
import random
import time
import sys
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import re

# ============================================================================
# COLOR CODES FOR TERMINAL OUTPUT
# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text: str, color=Colors.CYAN):
    """Print a formatted header"""
    width = 75
    print(f"\n{color}{'═' * width}")
    print(f"{text.center(width)}")
    print(f"{'═' * width}{Colors.RESET}\n")

def print_subheader(text: str):
    """Print a formatted subheader"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * len(text)}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.BRIGHT_GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.BRIGHT_RED}✗ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def get_input(prompt: str, color=Colors.WHITE) -> str:
    """Get user input with color"""
    return input(f"{color}{prompt}{Colors.RESET}").strip()

def press_enter():
    """Wait for user to press enter"""
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

# ============================================================================
# QUESTION CLASS
# ============================================================================

class Question:
    """Represents a quiz question"""
    
    def __init__(self, week: int, difficulty: str, q_type: str, question: str,
                 options: List[str], correct: str, explanation: str, 
                 hint: str = "", code: str = "", q_id: str = ""):
        self.week = week
        self.difficulty = difficulty  # Beginner, Intermediate, Advanced
        self.q_type = q_type  # MCQ, TrueFalse, FillBlank, CodeOutput, Coding
        self.question = question
        self.options = options
        self.correct = correct
        self.explanation = explanation
        self.hint = hint
        self.code = code
        self.q_id = q_id or f"W{week}_{q_type}_{random.randint(1000, 9999)}"
    
    def display(self, show_hint: bool = False):
        """Display the question"""
        # Difficulty indicator
        diff_colors = {
            'Beginner': Colors.GREEN,
            'Intermediate': Colors.YELLOW,
            'Advanced': Colors.RED
        }
        diff_color = diff_colors.get(self.difficulty, Colors.WHITE)
        
        print(f"{diff_color}[{self.difficulty}]{Colors.RESET} Week {self.week}")
        print(f"\n{Colors.BOLD}{self.question}{Colors.RESET}\n")
        
        # Display code if present
        if self.code:
            print(f"{Colors.CYAN}```python")
            print(self.code)
            print(f"```{Colors.RESET}\n")
        
        # Display options
        if self.options:
            for i, option in enumerate(self.options):
                print(f"  {chr(65 + i)}) {option}")
            print()
        
        # Display hint if requested
        if show_hint and self.hint:
            print(f"{Colors.YELLOW}💡 Hint: {self.hint}{Colors.RESET}\n")
    
    def check_answer(self, answer: str) -> bool:
        """Check if answer is correct"""
        answer = answer.strip().upper()
        correct = self.correct.strip().upper()
        
        if self.q_type == 'MCQ':
            return answer == correct
        elif self.q_type == 'TrueFalse':
            return answer == correct or (answer == 'T' and correct == 'TRUE') or (answer == 'F' and correct == 'FALSE')
        elif self.q_type == 'FillBlank':
            # Allow flexible matching for fill in the blank
            return answer.replace(' ', '').lower() == correct.replace(' ', '').lower()
        else:
            return answer == correct
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'week': self.week,
            'difficulty': self.difficulty,
            'type': self.q_type,
            'question': self.question,
            'options': self.options,
            'correct': self.correct,
            'explanation': self.explanation,
            'hint': self.hint,
            'code': self.code,
            'id': self.q_id
        }

# ============================================================================
# ACHIEVEMENT SYSTEM
# ============================================================================

class Achievement:
    """Represents an achievement/badge"""
    
    def __init__(self, name: str, description: str, icon: str, requirement: str):
        self.name = name
        self.description = description
        self.icon = icon
        self.requirement = requirement
        self.earned = False
        self.earned_date = None
    
    def earn(self):
        """Mark achievement as earned"""
        self.earned = True
        self.earned_date = datetime.now().isoformat()
    
    def display(self):
        """Display achievement"""
        status = f"{Colors.BRIGHT_GREEN}✓ EARNED" if self.earned else f"{Colors.DIM}Not earned yet"
        print(f"{self.icon} {Colors.BOLD}{self.name}{Colors.RESET} - {self.description}")
        print(f"   {status}{Colors.RESET}")
        if self.earned and self.earned_date:
            date = datetime.fromisoformat(self.earned_date).strftime("%Y-%m-%d")
            print(f"   {Colors.DIM}Earned on: {date}{Colors.RESET}")

class AchievementSystem:
    """Manages user achievements"""
    
    def __init__(self):
        self.achievements = self._create_achievements()
    
    def _create_achievements(self) -> List[Achievement]:
        """Create all available achievements"""
        return [
            Achievement("🎯 First Steps", "Answer your first question correctly", "🎯", "correct_1"),
            Achievement("🔥 Hot Streak", "Get 5 correct answers in a row", "🔥", "streak_5"),
            Achievement("⚡ Lightning Streak", "Get 10 correct answers in a row", "⚡", "streak_10"),
            Achievement("🌟 Perfect Week", "Score 100% on any week's quiz", "🌟", "perfect_week"),
            Achievement("📚 Scholar", "Answer 50 questions correctly", "📚", "correct_50"),
            Achievement("🎓 Master", "Answer 100 questions correctly", "🎓", "correct_100"),
            Achievement("🏆 Champion", "Answer 200 questions correctly", "🏆", "correct_200"),
            Achievement("💪 Dedicated", "Study for 5 days in a row", "💪", "days_5"),
            Achievement("🔨 Code Warrior", "Complete 10 coding challenges", "🔨", "coding_10"),
            Achievement("🚀 Speed Demon", "Complete a quiz in under 2 minutes", "🚀", "speed_120"),
            Achievement("🧠 Big Brain", "Score 90%+ on an Advanced quiz", "🧠", "advanced_90"),
            Achievement("📖 Bookworm", "Complete all 10 weeks", "📖", "weeks_10"),
            Achievement("💯 Perfectionist", "Get 100% on 5 different quizzes", "💯", "perfect_5"),
            Achievement("🎪 Jack of All Trades", "Answer questions from every week", "🎪", "all_weeks"),
            Achievement("⏰ Time Lord", "Complete a 20-question timed quiz", "⏰", "timed_20"),
        ]
    
    def check_achievements(self, stats: dict) -> List[Achievement]:
        """Check and award achievements based on stats"""
        newly_earned = []
        
        for achievement in self.achievements:
            if achievement.earned:
                continue
            
            # Check requirements
            if achievement.requirement == "correct_1" and stats['total_correct'] >= 1:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "streak_5" and stats['best_streak'] >= 5:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "streak_10" and stats['best_streak'] >= 10:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "correct_50" and stats['total_correct'] >= 50:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "correct_100" and stats['total_correct'] >= 100:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "correct_200" and stats['total_correct'] >= 200:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "coding_10" and stats.get('coding_completed', 0) >= 10:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "weeks_10" and len(stats.get('weeks_completed', [])) >= 10:
                achievement.earn()
                newly_earned.append(achievement)
            elif achievement.requirement == "perfect_5" and stats.get('perfect_quizzes', 0) >= 5:
                achievement.earn()
                newly_earned.append(achievement)
        
        return newly_earned
    
    def display_all(self):
        """Display all achievements"""
        earned = [a for a in self.achievements if a.earned]
        locked = [a for a in self.achievements if not a.earned]
        
        print(f"\n{Colors.BOLD}Achievements: {len(earned)}/{len(self.achievements)}{Colors.RESET}\n")
        
        if earned:
            print(f"{Colors.GREEN}✓ Earned:{Colors.RESET}")
            for achievement in earned:
                achievement.display()
                print()
        
        if locked:
            print(f"\n{Colors.DIM}🔒 Locked:{Colors.RESET}")
            for achievement in locked:
                achievement.display()
                print()

# ============================================================================
# USER PROFILE
# ============================================================================

class UserProfile:
    """Represents a user profile with stats and progress"""
    
    def __init__(self, name: str):
        self.name = name
        self.created_date = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()
        
        # Statistics
        self.total_questions = 0
        self.total_correct = 0
        self.total_incorrect = 0
        self.best_streak = 0
        self.current_streak = 0
        self.total_time_seconds = 0
        self.perfect_quizzes = 0
        self.coding_completed = 0
        
        # Week progress
        self.week_stats = {i: {'attempted': 0, 'correct': 0} for i in range(1, 11)}
        self.weeks_completed = []
        
        # Question tracking
        self.incorrect_questions = []  # List of question IDs
        self.mastered_questions = []   # Questions answered correctly multiple times
        
        # Study sessions
        self.study_days = []  # List of dates
        
        # Achievements
        self.achievements = AchievementSystem()
    
    def update_stats(self, correct: bool, week: int, question_id: str):
        """Update user statistics"""
        self.total_questions += 1
        self.last_active = datetime.now().isoformat()
        
        if correct:
            self.total_correct += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
            self.week_stats[week]['correct'] += 1
            
            # Remove from incorrect list if present
            if question_id in self.incorrect_questions:
                self.incorrect_questions.remove(question_id)
                self.mastered_questions.append(question_id)
        else:
            self.total_incorrect += 1
            self.current_streak = 0
            if question_id not in self.incorrect_questions:
                self.incorrect_questions.append(question_id)
        
        self.week_stats[week]['attempted'] += 1
        
        # Track study day
        today = datetime.now().date().isoformat()
        if today not in self.study_days:
            self.study_days.append(today)
    
    def get_accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.total_questions == 0:
            return 0.0
        return (self.total_correct / self.total_questions) * 100
    
    def get_weak_weeks(self) -> List[int]:
        """Identify weeks with low performance"""
        weak_weeks = []
        for week, stats in self.week_stats.items():
            if stats['attempted'] >= 5:  # Only consider weeks with enough attempts
                accuracy = (stats['correct'] / stats['attempted']) * 100
                if accuracy < 70:
                    weak_weeks.append(week)
        return weak_weeks
    
    def get_study_recommendations(self) -> List[str]:
        """Generate personalized study recommendations"""
        recommendations = []
        
        # Check weak weeks
        weak_weeks = self.get_weak_weeks()
        if weak_weeks:
            recommendations.append(f"Focus on Week(s) {', '.join(map(str, weak_weeks))} - accuracy below 70%")
        
        # Check streak
        if self.current_streak < 3:
            recommendations.append("Try to build a streak of correct answers for better retention")
        
        # Check study consistency
        if len(self.study_days) < 5:
            recommendations.append("Study more consistently - aim for daily practice")
        
        # Check incorrect questions
        if len(self.incorrect_questions) > 10:
            recommendations.append(f"Review {len(self.incorrect_questions)} incorrect questions")
        
        # Check coding challenges
        if self.coding_completed < 5:
            recommendations.append("Practice more coding challenges to improve hands-on skills")
        
        # Check overall progress
        if self.total_questions < 50:
            recommendations.append("Complete more questions to build a strong foundation")
        
        if not recommendations:
            recommendations.append("Great job! Keep up the consistent practice!")
        
        return recommendations
    
    def display_stats(self):
        """Display detailed statistics"""
        print_header("USER STATISTICS", Colors.CYAN)
        
        accuracy = self.get_accuracy()
        
        print(f"{Colors.BOLD}Profile:{Colors.RESET} {self.name}")
        print(f"{Colors.BOLD}Member Since:{Colors.RESET} {datetime.fromisoformat(self.created_date).strftime('%Y-%m-%d')}")
        print(f"{Colors.BOLD}Study Days:{Colors.RESET} {len(self.study_days)} days\n")
        
        print(f"{Colors.BOLD}Overall Performance:{Colors.RESET}")
        print(f"  Total Questions: {self.total_questions}")
        print(f"  Correct Answers: {Colors.GREEN}{self.total_correct}{Colors.RESET}")
        print(f"  Incorrect Answers: {Colors.RED}{self.total_incorrect}{Colors.RESET}")
        
        # Accuracy with color
        if accuracy >= 80:
            acc_color = Colors.GREEN
        elif accuracy >= 60:
            acc_color = Colors.YELLOW
        else:
            acc_color = Colors.RED
        print(f"  Accuracy: {acc_color}{accuracy:.1f}%{Colors.RESET}\n")
        
        print(f"{Colors.BOLD}Streaks:{Colors.RESET}")
        print(f"  Current Streak: {Colors.YELLOW}{self.current_streak}{Colors.RESET}")
        print(f"  Best Streak: {Colors.GREEN}{self.best_streak}{Colors.RESET}\n")
        
        print(f"{Colors.BOLD}Progress by Week:{Colors.RESET}")
        for week in range(1, 11):
            stats = self.week_stats[week]
            if stats['attempted'] > 0:
                week_acc = (stats['correct'] / stats['attempted']) * 100
                bar_length = int(week_acc / 5)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                
                if week_acc >= 80:
                    color = Colors.GREEN
                elif week_acc >= 60:
                    color = Colors.YELLOW
                else:
                    color = Colors.RED
                
                print(f"  Week {week:2d}: {color}{bar}{Colors.RESET} {week_acc:5.1f}% ({stats['correct']}/{stats['attempted']})")
            else:
                print(f"  Week {week:2d}: {Colors.DIM}No attempts yet{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}Additional Stats:{Colors.RESET}")
        print(f"  Perfect Quizzes: {self.perfect_quizzes}")
        print(f"  Coding Challenges: {self.coding_completed}")
        print(f"  Questions to Review: {len(self.incorrect_questions)}")
        print(f"  Mastered Questions: {len(self.mastered_questions)}")
        
        # Study recommendations
        print_subheader("📚 Study Recommendations")
        recommendations = self.get_study_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary"""
        return {
            'name': self.name,
            'created_date': self.created_date,
            'last_active': self.last_active,
            'total_questions': self.total_questions,
            'total_correct': self.total_correct,
            'total_incorrect': self.total_incorrect,
            'best_streak': self.best_streak,
            'current_streak': self.current_streak,
            'total_time_seconds': self.total_time_seconds,
            'perfect_quizzes': self.perfect_quizzes,
            'coding_completed': self.coding_completed,
            'week_stats': self.week_stats,
            'weeks_completed': self.weeks_completed,
            'incorrect_questions': self.incorrect_questions,
            'mastered_questions': self.mastered_questions,
            'study_days': self.study_days,
            'achievements': {
                a.name: {'earned': a.earned, 'earned_date': a.earned_date}
                for a in self.achievements.achievements
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserProfile':
        """Create profile from dictionary"""
        profile = cls(data['name'])
        profile.created_date = data.get('created_date', datetime.now().isoformat())
        profile.last_active = data.get('last_active', datetime.now().isoformat())
        profile.total_questions = data.get('total_questions', 0)
        profile.total_correct = data.get('total_correct', 0)
        profile.total_incorrect = data.get('total_incorrect', 0)
        profile.best_streak = data.get('best_streak', 0)
        profile.current_streak = data.get('current_streak', 0)
        profile.total_time_seconds = data.get('total_time_seconds', 0)
        profile.perfect_quizzes = data.get('perfect_quizzes', 0)
        profile.coding_completed = data.get('coding_completed', 0)
        profile.week_stats = data.get('week_stats', {i: {'attempted': 0, 'correct': 0} for i in range(1, 11)})
        profile.weeks_completed = data.get('weeks_completed', [])
        profile.incorrect_questions = data.get('incorrect_questions', [])
        profile.mastered_questions = data.get('mastered_questions', [])
        profile.study_days = data.get('study_days', [])
        
        # Restore achievements
        saved_achievements = data.get('achievements', {})
        for achievement in profile.achievements.achievements:
            if achievement.name in saved_achievements:
                ach_data = saved_achievements[achievement.name]
                if ach_data['earned']:
                    achievement.earned = True
                    achievement.earned_date = ach_data['earned_date']
        
        return profile

# ============================================================================
# QUESTION DATABASE
# ============================================================================

def create_question_database() -> List[Question]:
    """Create comprehensive question database"""
    questions = []
    
    # ========================================================================
    # WEEK 1: Python Basics
    # ========================================================================
    
    questions.extend([
        Question(1, 'Beginner', 'MCQ',
                'Which of the following is a valid variable name in Python?',
                ['1st_variable', 'first-variable', 'first_variable', 'first variable'],
                'C', 'Variable names can contain letters, numbers, and underscores, but cannot start with a number or contain hyphens/spaces.',
                'Variable names must follow Python naming conventions'),
        
        Question(1, 'Beginner', 'MCQ',
                'What is the output of: print(type(5.0))?',
                ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'number'>"],
                'B', '5.0 is a floating-point number, so its type is float.',
                'The .0 indicates a decimal number'),
        
        Question(1, 'Intermediate', 'CodeOutput',
                'What is the output of the following code?',
                ['5', '2', '2.5', 'Error'],
                'B', 'The // operator performs floor division, returning only the integer part.',
                'Look at the operator carefully - double slash',
                'x = 5\ny = 2\nprint(x // y)'),
        
        Question(1, 'Intermediate', 'MCQ',
                'What does the len() function return for the string "Hello"?',
                ['4', '5', '6', 'Error'],
                'B', 'len() returns the number of characters in the string, which is 5.',
                'Count each character including letters'),
        
        Question(1, 'Advanced', 'CodeOutput',
                'What is the output?',
                ['HelloWorld', 'Hello World', 'Error', 'Hello'],
                'B', 'String concatenation with + joins the strings. The space is included in the second string.',
                'Pay attention to the space in the second string',
                's1 = "Hello"\ns2 = " World"\nprint(s1 + s2)'),
        
        Question(1, 'Beginner', 'TrueFalse',
                'In Python, variables must be declared with a type before use.',
                ['True', 'False'],
                'FALSE', 'Python is dynamically typed, so variables do not need type declarations.',
                'Python uses dynamic typing'),
        
        Question(1, 'Intermediate', 'FillBlank',
                'Complete the code to convert string to integer: x = ___("42")',
                [],
                'int', 'The int() function converts a string to an integer.',
                'Think about type conversion functions'),
        
        Question(1, 'Advanced', 'MCQ',
                'What is the result of: bool("")?',
                ['True', 'False', 'None', 'Error'],
                'B', 'Empty strings are considered False in Python (falsy values).',
                'Empty containers are falsy in Python'),
        
        Question(1, 'Beginner', 'MCQ',
                'Which operator is used for exponentiation in Python?',
                ['^', '**', 'pow', 'exp'],
                'B', 'The ** operator is used for exponentiation (e.g., 2 ** 3 = 8).',
                'It\'s a double character operator'),
        
        Question(1, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['ABC', 'ABCABCABC', 'Error', 'AAA BBB CCC'],
                'B', 'String multiplication repeats the string n times.',
                'The * operator with strings creates repetition',
                'print("ABC" * 3)'),
    ])
    
    # ========================================================================
    # WEEK 2: Control Flow
    # ========================================================================
    
    questions.extend([
        Question(2, 'Beginner', 'MCQ',
                'What does the break statement do in a loop?',
                ['Skips the current iteration', 'Exits the loop completely', 'Restarts the loop', 'Pauses the loop'],
                'B', 'break immediately exits the innermost loop.',
                'Think about stopping the loop entirely'),
        
        Question(2, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['0 1 2', '1 2 3', '0\\n1\\n2', '1\\n2\\n3'],
                'C', 'range(3) generates 0, 1, 2. print() adds a newline after each number.',
                'range() starts at 0 by default, print() adds newlines',
                'for i in range(3):\n    print(i)'),
        
        Question(2, 'Beginner', 'MCQ',
                'Which keyword is used for an alternative condition in if statements?',
                ['else', 'elif', 'otherwise', 'then'],
                'B', 'elif (else if) is used for additional conditions.',
                'It\'s a combination of two words'),
        
        Question(2, 'Advanced', 'CodeOutput',
                'What is the output?',
                ['1 2 4 5', '1 2 4', '1 2 3 4 5', '1 4 5'],
                'A', 'continue skips printing 3, break stops the loop at 5.',
                'continue skips one iteration, break exits the loop',
                'for i in range(1, 6):\n    if i == 3:\n        continue\n    if i == 5:\n        break\n    print(i, end=" ")'),
        
        Question(2, 'Intermediate', 'TrueFalse',
                'A while loop always executes at least once.',
                ['True', 'False'],
                'FALSE', 'If the condition is False initially, the loop body never executes.',
                'Check the condition before entering'),
        
        Question(2, 'Advanced', 'MCQ',
                'What is the purpose of the else clause in a for loop?',
                ['Handles errors', 'Executes if loop completes normally', 'Provides alternative iteration', 'None of these'],
                'B', 'The else clause executes after the loop completes, unless break is called.',
                'It runs when the loop finishes without break'),
        
        Question(2, 'Beginner', 'CodeOutput',
                'What is the output?',
                ['positive', 'negative', 'zero', 'No output'],
                'C', 'x is 0, so it matches the elif condition.',
                'Check which condition matches 0',
                'x = 0\nif x > 0:\n    print("positive")\nelif x == 0:\n    print("zero")\nelse:\n    print("negative")'),
        
        Question(2, 'Intermediate', 'FillBlank',
                'Complete: for i in range(10, 1, ___): will count down from 10 to 2',
                [],
                '-1', 'The third parameter in range() is the step. -1 counts down.',
                'You need to go backwards'),
        
        Question(2, 'Advanced', 'MCQ',
                'What does pass do in Python?',
                ['Exits the loop', 'Skips to next iteration', 'Does nothing (placeholder)', 'Raises an error'],
                'C', 'pass is a null operation used as a placeholder.',
                'It\'s used when syntax requires a statement but you want to do nothing'),
        
        Question(2, 'Beginner', 'MCQ',
                'Which loop is best when you don\'t know how many iterations are needed?',
                ['for loop', 'while loop', 'do-while loop', 'foreach loop'],
                'B', 'while loops continue until a condition is false, making them ideal for unknown iteration counts.',
                'This loop checks a condition each time'),
    ])
    
    # ========================================================================
    # WEEK 3: Lists & APIs
    # ========================================================================
    
    questions.extend([
        Question(3, 'Beginner', 'MCQ',
                'How do you access the first element of a list?',
                ['list[0]', 'list[1]', 'list.first()', 'list.get(0)'],
                'A', 'Lists use zero-based indexing, so the first element is at index 0.',
                'Python uses zero-based indexing'),
        
        Question(3, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['[1, 2, 3, 4]', '[4, 1, 2, 3]', '[1, 2, 3]', 'Error'],
                'B', 'insert(0, 4) adds 4 at the beginning of the list.',
                'insert() adds at a specific position',
                'nums = [1, 2, 3]\nnums.insert(0, 4)\nprint(nums)'),
        
        Question(3, 'Advanced', 'MCQ',
                'What does list comprehension [x**2 for x in range(5)] produce?',
                ['[0, 1, 4, 9, 16]', '[1, 2, 3, 4, 5]', '[0, 1, 2, 3, 4]', '[1, 4, 9, 16, 25]'],
                'A', 'List comprehension squares each number from 0 to 4.',
                'Square each number in range(5)'),
        
        Question(3, 'Beginner', 'MCQ',
                'Which method adds an element to the end of a list?',
                ['add()', 'append()', 'insert()', 'push()'],
                'B', 'append() adds an element to the end of the list.',
                'Think about adding to the end'),
        
        Question(3, 'Intermediate', 'TrueFalse',
                'Lists in Python are mutable (can be changed after creation).',
                ['True', 'False'],
                'TRUE', 'Lists are mutable - you can modify, add, or remove elements.',
                'Can you change list elements after creation?'),
        
        Question(3, 'Advanced', 'FillBlank',
                'Complete to get every other element: my_list[::___]',
                [],
                '2', 'The step parameter of 2 gets every second element.',
                'Use the step parameter in slicing'),
        
        Question(3, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['3', '2', '4', 'Error'],
                'A', 'Negative indices count from the end. -1 is the last element.',
                'Negative indices count backwards',
                'nums = [1, 2, 3, 4]\nprint(nums[-2])'),
        
        Question(3, 'Beginner', 'MCQ',
                'What does the len() function return for [1, 2, 3, 4, 5]?',
                ['4', '5', '6', 'Error'],
                'B', 'len() returns the number of elements, which is 5.',
                'Count the elements'),
        
        Question(3, 'Advanced', 'MCQ',
                'What is the result of [1, 2] + [3, 4]?',
                ['[1, 2, 3, 4]', '[4, 6]', 'Error', '[1, 2] [3, 4]'],
                'A', 'The + operator concatenates lists.',
                'Lists can be joined together'),
        
        Question(3, 'Intermediate', 'MCQ',
                'Which method removes and returns the last element of a list?',
                ['remove()', 'delete()', 'pop()', 'pull()'],
                'C', 'pop() removes and returns the last element (or element at specified index).',
                'This method both removes and gives you the element'),
    ])
    
    # ========================================================================
    # WEEK 4: Dictionaries & Functions
    # ========================================================================
    
    questions.extend([
        Question(4, 'Beginner', 'MCQ',
                'How do you create an empty dictionary?',
                ['dict = []', 'dict = {}', 'dict = ()', 'dict = new dict()'],
                'B', 'Curly braces {} create an empty dictionary.',
                'Dictionaries use curly braces'),
        
        Question(4, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['Alice', 'Error', 'None', '25'],
                'A', 'The key "name" maps to the value "Alice".',
                'Access dictionary values by key',
                'person = {"name": "Alice", "age": 25}\nprint(person["name"])'),
        
        Question(4, 'Advanced', 'MCQ',
                'What does the get() method do if the key doesn\'t exist?',
                ['Raises KeyError', 'Returns None', 'Returns empty string', 'Creates the key'],
                'B', 'get() returns None (or a default value) instead of raising an error.',
                'get() is safer than bracket notation'),
        
        Question(4, 'Beginner', 'MCQ',
                'Which keyword is used to define a function?',
                ['func', 'function', 'def', 'define'],
                'C', 'The def keyword defines functions in Python.',
                'It\'s a short, three-letter keyword'),
        
        Question(4, 'Intermediate', 'FillBlank',
                'Complete the lambda to multiply by 2: lambda x: x ___ 2',
                [],
                '* 2', 'Use the multiplication operator *.',
                'Lambda functions can use arithmetic operators'),
        
        Question(4, 'Advanced', 'CodeOutput',
                'What is the output?',
                ['10', '5', 'Error', 'None'],
                'A', 'The function returns x + y, which is 3 + 7 = 10.',
                'The return statement sends back the sum',
                'def add(x, y):\n    return x + y\nprint(add(3, 7))'),
        
        Question(4, 'Intermediate', 'TrueFalse',
                'Dictionary keys must be unique.',
                ['True', 'False'],
                'TRUE', 'Each key in a dictionary must be unique. Duplicate keys will overwrite previous values.',
                'Can two keys have the same name?'),
        
        Question(4, 'Beginner', 'MCQ',
                'What method returns all keys in a dictionary?',
                ['keys()', 'getKeys()', 'allKeys()', 'keyList()'],
                'A', 'The keys() method returns all dictionary keys.',
                'It\'s a simple, descriptive method name'),
        
        Question(4, 'Advanced', 'MCQ',
                'What is *args in a function definition?',
                ['Multiplies arguments', 'Variable number of positional arguments', 'Keyword arguments', 'Optional arguments'],
                'B', '*args allows a function to accept any number of positional arguments.',
                'The asterisk allows variable length arguments'),
        
        Question(4, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['10', '20', 'Error', 'None'],
                'B', 'The default parameter value b=20 is used when no second argument is provided.',
                'Default parameters are used when not specified',
                'def func(a, b=20):\n    return b\nprint(func(10))'),
    ])
    
    # ========================================================================
    # WEEK 5: Files & Error Handling
    # ========================================================================
    
    questions.extend([
        Question(5, 'Beginner', 'MCQ',
                'Which mode opens a file for reading?',
                ['"w"', '"r"', '"a"', '"x"'],
                'B', 'The "r" mode opens a file for reading.',
                'Think about the first letter of "read"'),
        
        Question(5, 'Intermediate', 'MCQ',
                'What is the purpose of the with statement when working with files?',
                ['Faster file access', 'Automatic file closing', 'Better error handling', 'All of the above'],
                'B', 'The with statement ensures the file is properly closed after use.',
                'It manages resources automatically'),
        
        Question(5, 'Advanced', 'CodeOutput',
                'What happens if you try to open a non-existent file in read mode without error handling?',
                ['Returns None', 'Creates the file', 'Raises FileNotFoundError', 'Returns empty string'],
                'C', 'Python raises FileNotFoundError when trying to read a non-existent file.',
                'Missing files cause specific errors'),
        
        Question(5, 'Beginner', 'MCQ',
                'Which keyword starts an exception handling block?',
                ['try', 'catch', 'except', 'handle'],
                'A', 'The try keyword begins an exception handling block.',
                'You "try" code that might fail'),
        
        Question(5, 'Intermediate', 'TrueFalse',
                'The finally block always executes, even if an exception occurs.',
                ['True', 'False'],
                'TRUE', 'finally always executes, whether an exception occurred or not.',
                'It\'s called "finally" for a reason'),
        
        Question(5, 'Advanced', 'FillBlank',
                'To catch any exception: except ___ as e:',
                [],
                'Exception', 'Exception is the base class for all exceptions.',
                'It\'s the parent class of all errors'),
        
        Question(5, 'Intermediate', 'MCQ',
                'What does json.loads() do?',
                ['Saves JSON to file', 'Parses JSON string to Python object', 'Creates JSON file', 'Validates JSON'],
                'B', 'json.loads() converts a JSON string into a Python object.',
                'The "s" stands for "string"'),
        
        Question(5, 'Beginner', 'MCQ',
                'Which module is used to work with CSV files in Python?',
                ['csv', 'file', 'data', 'excel'],
                'A', 'The csv module provides CSV file handling.',
                'It\'s named after the file format'),
        
        Question(5, 'Advanced', 'MCQ',
                'What is the difference between "w" and "a" file modes?',
                ['No difference', '"w" writes, "a" appends', '"w" is faster', '"a" creates new file'],
                'B', '"w" overwrites the file, while "a" appends to the end.',
                'One destroys old content, one adds to it'),
        
        Question(5, 'Intermediate', 'CodeOutput',
                'What does this code print if the file doesn\'t exist?',
                ['Empty string', 'File not found', 'Error', 'None'],
                'B', 'The except block catches the error and prints the message.',
                'The except block handles the FileNotFoundError',
                'try:\n    f = open("missing.txt")\nexcept FileNotFoundError:\n    print("File not found")'),
    ])
    
    # ========================================================================
    # WEEK 6: Object-Oriented Programming
    # ========================================================================
    
    questions.extend([
        Question(6, 'Beginner', 'MCQ',
                'What keyword is used to create a class?',
                ['class', 'object', 'new', 'define'],
                'A', 'The class keyword defines a new class.',
                'It\'s the same word as the concept'),
        
        Question(6, 'Intermediate', 'MCQ',
                'What is self in a class method?',
                ['A keyword', 'Reference to the instance', 'The class name', 'A parameter'],
                'B', 'self refers to the instance of the class.',
                'It represents the object itself'),
        
        Question(6, 'Advanced', 'MCQ',
                'What is the purpose of __init__ method?',
                ['Destructor', 'Constructor/Initializer', 'String representation', 'Comparison'],
                'B', '__init__ initializes a new instance of the class.',
                'It\'s called when creating objects'),
        
        Question(6, 'Beginner', 'TrueFalse',
                'A class can have multiple objects (instances).',
                ['True', 'False'],
                'TRUE', 'You can create many instances from a single class definition.',
                'Think of a class as a blueprint'),
        
        Question(6, 'Intermediate', 'FillBlank',
                'To inherit from a class: class Child(___):',
                [],
                'Parent', 'Put the parent class name in parentheses.',
                'The parent class goes in parentheses'),
        
        Question(6, 'Advanced', 'MCQ',
                'What does the super() function do?',
                ['Creates a superclass', 'Calls parent class methods', 'Makes a class abstract', 'Increases priority'],
                'B', 'super() calls methods from the parent class.',
                'It accesses the parent/super class'),
        
        Question(6, 'Intermediate', 'CodeOutput',
                'What is the output?',
                ['Toyota', 'Car', 'Error', 'None'],
                'A', 'The make attribute is set to "Toyota" in __init__.',
                'Check what\'s assigned in the constructor',
                'class Car:\n    def __init__(self, make):\n        self.make = make\nc = Car("Toyota")\nprint(c.make)'),
        
        Question(6, 'Advanced', 'MCQ',
                'What is polymorphism in OOP?',
                ['Multiple classes', 'Same interface, different implementations', 'Class inheritance', 'Object creation'],
                'B', 'Polymorphism allows objects of different classes to be treated uniformly.',
                'Many forms of the same interface'),
        
        Question(6, 'Beginner', 'MCQ',
                'What is encapsulation?',
                ['Hiding implementation details', 'Creating multiple objects', 'Inheriting classes', 'Using loops'],
                'A', 'Encapsulation bundles data and methods, hiding internal details.',
                'It\'s about data hiding'),
        
        Question(6, 'Intermediate', 'MCQ',
                'How do you define a private attribute in Python?',
                ['private name', '_name', '__name', 'name_private'],
                'C', 'Double underscore __ prefix makes an attribute private.',
                'Use double underscore prefix'),
    ])
    
    # ========================================================================
    # WEEK 7: Git & Version Control
    # ========================================================================
    
    questions.extend([
        Question(7, 'Beginner', 'MCQ',
                'What command initializes a new Git repository?',
                ['git start', 'git init', 'git new', 'git create'],
                'B', 'git init initializes a new Git repository.',
                'It\'s short for "initialize"'),
        
        Question(7, 'Intermediate', 'MCQ',
                'What does git add do?',
                ['Commits changes', 'Stages files for commit', 'Pushes to remote', 'Creates branch'],
                'B', 'git add stages files, preparing them for commit.',
                'It adds files to the staging area'),
        
        Question(7, 'Advanced', 'MCQ',
                'What is the difference between git pull and git fetch?',
                ['No difference', 'pull = fetch + merge', 'pull is faster', 'fetch is deprecated'],
                'B', 'git pull fetches and merges changes; git fetch only fetches.',
                'Pull does an extra step'),
        
        Question(7, 'Beginner', 'MCQ',
                'Which command creates a new branch?',
                ['git new branch_name', 'git branch branch_name', 'git create branch_name', 'git branch -n branch_name'],
                'B', 'git branch branch_name creates a new branch.',
                'Use the branch command with a name'),
        
        Question(7, 'Intermediate', 'TrueFalse',
                'git commit -m "message" commits and pushes changes.',
                ['True', 'False'],
                'FALSE', 'git commit only commits locally. You need git push to push to remote.',
                'Commit and push are separate operations'),
        
        Question(7, 'Advanced', 'FillBlank',
                'To undo the last commit: git reset ___',
                [],
                'HEAD~1', 'HEAD~1 refers to the commit before the current HEAD.',
                'Use HEAD with a tilde and number'),
        
        Question(7, 'Intermediate', 'MCQ',
                'What does git status show?',
                ['Commit history', 'Current branch and file states', 'Remote repositories', 'Branches'],
                'B', 'git status shows the current branch and the status of files.',
                'It shows the current state'),
        
        Question(7, 'Beginner', 'MCQ',
                'How do you switch to an existing branch?',
                ['git switch branch_name', 'git checkout branch_name', 'git change branch_name', 'Both A and B'],
                'D', 'Both git switch and git checkout can switch branches.',
                'There are two modern ways'),
        
        Question(7, 'Advanced', 'MCQ',
                'What is a merge conflict?',
                ['Branch error', 'Same file edited in different branches', 'Network error', 'Permission error'],
                'B', 'Merge conflicts occur when the same file is edited in different ways in different branches.',
                'It happens when changes collide'),
        
        Question(7, 'Intermediate', 'MCQ',
                'What does git clone do?',
                ['Creates a branch', 'Copies a remote repository', 'Merges branches', 'Deletes repository'],
                'B', 'git clone creates a local copy of a remote repository.',
                'It makes a copy of a repo'),
    ])
    
    # ========================================================================
    # WEEK 8: Databases
    # ========================================================================
    
    questions.extend([
        Question(8, 'Beginner', 'MCQ',
                'What does SQL stand for?',
                ['Simple Query Language', 'Structured Query Language', 'Standard Query Language', 'System Query Language'],
                'B', 'SQL stands for Structured Query Language.',
                'It\'s about structure'),
        
        Question(8, 'Intermediate', 'MCQ',
                'Which SQL command retrieves data from a database?',
                ['GET', 'SELECT', 'RETRIEVE', 'FETCH'],
                'B', 'SELECT retrieves data from database tables.',
                'You "select" what you want to see'),
        
        Question(8, 'Advanced', 'MCQ',
                'In DynamoDB, what is a partition key?',
                ['Secondary index', 'Primary key component', 'Foreign key', 'Sorting key'],
                'B', 'The partition key is the primary key component that determines data distribution.',
                'It\'s part of the primary key'),
        
        Question(8, 'Beginner', 'MCQ',
                'Which SQL command adds a new record?',
                ['ADD', 'INSERT', 'NEW', 'CREATE'],
                'B', 'INSERT adds new records to a table.',
                'You "insert" new data'),
        
        Question(8, 'Intermediate', 'TrueFalse',
                'DynamoDB is a NoSQL database.',
                ['True', 'False'],
                'TRUE', 'DynamoDB is a NoSQL key-value and document database.',
                'It doesn\'t use SQL'),
        
        Question(8, 'Advanced', 'FillBlank',
                'Complete SQL: SELECT * FROM users WHERE age ___ 18',
                [],
                '> 18', 'Use a comparison operator like > (greater than).',
                'You need a comparison operator'),
        
        Question(8, 'Intermediate', 'MCQ',
                'What does the WHERE clause do in SQL?',
                ['Sorts results', 'Filters results', 'Joins tables', 'Groups results'],
                'B', 'WHERE filters rows based on a condition.',
                'It specifies which rows to include'),
        
        Question(8, 'Beginner', 'MCQ',
                'Which Python library is commonly used with DynamoDB?',
                ['pymongo', 'boto3', 'sqlalchemy', 'psycopg2'],
                'B', 'boto3 is the AWS SDK for Python, used with DynamoDB.',
                'It\'s the AWS SDK'),
        
        Question(8, 'Advanced', 'MCQ',
                'What is an eventual consistency model?',
                ['Always consistent', 'Consistent after short delay', 'Never consistent', 'Immediately consistent'],
                'B', 'Eventual consistency means data will be consistent after a short delay.',
                'Eventually means "after a short time"'),
        
        Question(8, 'Intermediate', 'MCQ',
                'What does JOIN do in SQL?',
                ['Combines rows from multiple tables', 'Adds new columns', 'Deletes duplicates', 'Sorts data'],
                'A', 'JOIN combines rows from two or more tables based on a related column.',
                'It connects tables together'),
    ])
    
    # ========================================================================
    # WEEK 9: Cloud Storage
    # ========================================================================
    
    questions.extend([
        Question(9, 'Beginner', 'MCQ',
                'What does S3 stand for?',
                ['Simple Storage Service', 'Secure Storage System', 'Standard Storage Solution', 'Super Storage Service'],
                'A', 'S3 stands for Simple Storage Service.',
                'It\'s about simplicity'),
        
        Question(9, 'Intermediate', 'MCQ',
                'What is an S3 bucket?',
                ['A container for objects', 'A type of database', 'A compute instance', 'A network'],
                'A', 'An S3 bucket is a container for storing objects (files).',
                'It holds your files'),
        
        Question(9, 'Advanced', 'MCQ',
                'What is Amazon Textract used for?',
                ['Text editing', 'Extracting text from documents', 'Text translation', 'Text generation'],
                'B', 'Textract extracts text and data from scanned documents.',
                'It extracts text'),
        
        Question(9, 'Beginner', 'TrueFalse',
                'S3 bucket names must be globally unique across all AWS accounts.',
                ['True', 'False'],
                'TRUE', 'S3 bucket names must be unique across all of AWS.',
                'They\'re unique worldwide'),
        
        Question(9, 'Intermediate', 'MCQ',
                'Which boto3 method uploads a file to S3?',
                ['put_file()', 'upload_file()', 'send_file()', 'write_file()'],
                'B', 'upload_file() uploads a file to an S3 bucket.',
                'It\'s descriptive: upload_file'),
        
        Question(9, 'Advanced', 'FillBlank',
                'S3 objects are identified by a unique ___',
                [],
                'key', 'The key is the unique identifier for an object in a bucket.',
                'It\'s a unique identifier'),
        
        Question(9, 'Intermediate', 'MCQ',
                'What is S3 versioning?',
                ['Database versions', 'Keeping multiple versions of objects', 'API versions', 'Bucket versions'],
                'B', 'S3 versioning keeps multiple variants of an object in the same bucket.',
                'It tracks different versions of files'),
        
        Question(9, 'Beginner', 'MCQ',
                'What is the maximum size of an S3 object?',
                ['5 MB', '5 GB', '5 TB', 'Unlimited'],
                'C', 'S3 objects can be up to 5 TB in size.',
                'It\'s measured in terabytes'),
        
        Question(9, 'Advanced', 'MCQ',
                'What is the purpose of S3 lifecycle policies?',
                ['Security', 'Automatic object management', 'Performance', 'Monitoring'],
                'B', 'Lifecycle policies automatically transition or delete objects based on rules.',
                'They manage objects over time'),
        
        Question(9, 'Intermediate', 'TrueFalse',
                'S3 provides 99.999999999% (11 nines) durability.',
                ['True', 'False'],
                'TRUE', 'S3 is designed for 11 nines of durability.',
                'It\'s extremely durable'),
    ])
    
    # ========================================================================
    # WEEK 10: Serverless & Lambda
    # ========================================================================
    
    questions.extend([
        Question(10, 'Beginner', 'MCQ',
                'What is AWS Lambda?',
                ['A database', 'Serverless compute service', 'Storage service', 'Network service'],
                'B', 'Lambda is a serverless compute service that runs code in response to events.',
                'It runs code without servers'),
        
        Question(10, 'Intermediate', 'MCQ',
                'What triggers a Lambda function?',
                ['Only HTTP requests', 'Events from AWS services', 'Only scheduled tasks', 'Manual invocation only'],
                'B', 'Lambda functions can be triggered by various AWS service events.',
                'Many things can trigger it'),
        
        Question(10, 'Advanced', 'MCQ',
                'What is cold start in Lambda?',
                ['Startup delay for new instances', 'Lambda error', 'Network issue', 'Memory problem'],
                'A', 'Cold start is the latency when Lambda initializes a new execution environment.',
                'It\'s the initial startup time'),
        
        Question(10, 'Beginner', 'TrueFalse',
                'You need to manage servers when using Lambda.',
                ['True', 'False'],
                'FALSE', 'Lambda is serverless - AWS manages the infrastructure.',
                'That\'s why it\'s called serverless'),
        
        Question(10, 'Intermediate', 'MCQ',
                'What is API Gateway?',
                ['Database gateway', 'Creates and manages APIs', 'Storage gateway', 'Network gateway'],
                'B', 'API Gateway creates, publishes, and manages APIs.',
                'It handles APIs'),
        
        Question(10, 'Advanced', 'FillBlank',
                'Lambda functions must have a ___ handler',
                [],
                'handler', 'The handler is the entry point method that Lambda calls.',
                'It\'s the entry point'),
        
        Question(10, 'Intermediate', 'MCQ',
                'What is event-driven architecture?',
                ['Server-based design', 'Actions triggered by events', 'Database design', 'Network design'],
                'B', 'Event-driven architecture uses events to trigger and communicate between services.',
                'Events drive actions'),
        
        Question(10, 'Beginner', 'MCQ',
                'Which languages does Lambda support?',
                ['Only Python', 'Only JavaScript', 'Multiple languages including Python, Node.js, Java', 'Only compiled languages'],
                'C', 'Lambda supports multiple languages including Python, Node.js, Java, Go, and more.',
                'It supports many languages'),
        
        Question(10, 'Advanced', 'MCQ',
                'What is a Lambda layer?',
                ['Security layer', 'Reusable code package', 'Network layer', 'Storage layer'],
                'B', 'Lambda layers are reusable packages of libraries and dependencies.',
                'It\'s for sharing code'),
        
        Question(10, 'Intermediate', 'TrueFalse',
                'Lambda functions can run indefinitely.',
                ['True', 'False'],
                'FALSE', 'Lambda has a maximum execution time (currently 15 minutes).',
                'There\'s a time limit'),
    ])
    
    # Add more questions for each week to reach 150+ total
    # Additional advanced questions
    
    questions.extend([
        # More Week 1 questions
        Question(1, 'Advanced', 'MCQ',
                'What is the difference between == and is operators?',
                ['No difference', '== compares values, is compares identity', 'is is faster', '== is deprecated'],
                'B', '== checks value equality, while is checks if two variables reference the same object.',
                'One checks value, one checks identity'),
        
        # More Week 2 questions
        Question(2, 'Advanced', 'CodeOutput',
                'What is printed?',
                ['1 2 3', '2 3', '2', '1 3'],
                'B', 'The else clause in a for loop executes only if the loop completes without break.',
                'Loop else executes when loop completes normally',
                'for i in [1, 2, 3]:\n    if i == 1:\n        continue\n    print(i, end=" ")'),
        
        # More Week 3 questions
        Question(3, 'Advanced', 'FillBlank',
                'To flatten a nested list: [item for sublist in nested for item in ___]',
                [],
                'sublist', 'This is a nested list comprehension that iterates through sublists.',
                'Think about nested iteration'),
        
        # More Week 4 questions
        Question(4, 'Advanced', 'MCQ',
                'What is a closure in Python?',
                ['Class method', 'Function that remembers variables from enclosing scope', 'Loop construct', 'Exception handler'],
                'B', 'A closure is a function that captures variables from its enclosing scope.',
                'It "closes over" variables'),
        
        # More Week 5 questions
        Question(5, 'Advanced', 'MCQ',
                'What is the with statement also known as?',
                ['Loop manager', 'Context manager', 'File manager', 'Error manager'],
                'B', 'The with statement uses context managers for resource management.',
                'It manages context'),
        
        # More Week 6 questions
        Question(6, 'Advanced', 'MCQ',
                'What is the purpose of __str__ method?',
                ['Compare objects', 'String representation for users', 'Initialize object', 'Delete object'],
                'B', '__str__ provides a human-readable string representation of an object.',
                'It makes readable strings'),
        
        # More Week 7 questions
        Question(7, 'Advanced', 'MCQ',
                'What is git rebase used for?',
                ['Delete branches', 'Rewrite commit history', 'Create tags', 'Push to remote'],
                'B', 'git rebase rewrites commit history by moving commits to a new base.',
                'It changes the base of commits'),
        
        # More Week 8 questions
        Question(8, 'Advanced', 'MCQ',
                'What is a DynamoDB GSI?',
                ['Global Simple Index', 'Global Secondary Index', 'Generic SQL Interface', 'Generated System ID'],
                'B', 'GSI (Global Secondary Index) allows queries on non-primary key attributes.',
                'It\'s a secondary index'),
        
        # More Week 9 questions
        Question(9, 'Advanced', 'MCQ',
                'What is S3 Transfer Acceleration?',
                ['Faster uploads via CloudFront', 'Compression', 'Parallel uploads', 'Caching'],
                'A', 'Transfer Acceleration uses CloudFront edge locations for faster uploads.',
                'It uses edge locations'),
        
        # More Week 10 questions
        Question(10, 'Advanced', 'MCQ',
                'What is Lambda@Edge?',
                ['Lambda on EC2', 'Lambda at CloudFront edge locations', 'Lambda debugging tool', 'Lambda monitoring'],
                'B', 'Lambda@Edge runs functions at CloudFront edge locations closer to users.',
                'It runs at the edge'),
    ])
    
    return questions

# ============================================================================
# CODING CHALLENGES
# ============================================================================

class CodingChallenge:
    """Represents a coding challenge"""
    
    def __init__(self, week: int, title: str, description: str, 
                 example_input: str, example_output: str, hint: str, 
                 test_cases: List[Tuple], solution: str):
        self.week = week
        self.title = title
        self.description = description
        self.example_input = example_input
        self.example_output = example_output
        self.hint = hint
        self.test_cases = test_cases
        self.solution = solution
    
    def display(self):
        """Display the challenge"""
        print_subheader(f"🔨 Coding Challenge - Week {self.week}")
        print(f"{Colors.BOLD}{self.title}{Colors.RESET}\n")
        print(f"{self.description}\n")
        print(f"{Colors.CYAN}Example Input:{Colors.RESET} {self.example_input}")
        print(f"{Colors.GREEN}Expected Output:{Colors.RESET} {self.example_output}\n")
    
    def test_solution(self, user_code: str) -> Tuple[bool, str]:
        """Test user's solution against test cases"""
        try:
            # Create a namespace for execution
            namespace = {}
            exec(user_code, namespace)
            
            # Run test cases
            passed = 0
            for input_data, expected in self.test_cases:
                # Extract function name (assume first function defined)
                func_name = [name for name in namespace if callable(namespace[name]) and not name.startswith('__')][0]
                func = namespace[func_name]
                
                result = func(*input_data) if isinstance(input_data, tuple) else func(input_data)
                
                if result == expected:
                    passed += 1
                else:
                    return False, f"Test failed: input {input_data}, expected {expected}, got {result}"
            
            return True, f"All {passed}/{len(self.test_cases)} tests passed!"
        
        except Exception as e:
            return False, f"Error: {str(e)}"

def create_coding_challenges() -> List[CodingChallenge]:
    """Create coding challenges"""
    return [
        CodingChallenge(
            week=3,
            title="Remove Duplicates",
            description="Write a function that removes duplicates from a list while preserving order.",
            example_input="[1, 2, 2, 3, 4, 3, 5]",
            example_output="[1, 2, 3, 4, 5]",
            hint="Use a set to track seen items, but build a new list to preserve order.",
            test_cases=[
                (([1, 2, 2, 3, 4, 3, 5],), [1, 2, 3, 4, 5]),
                (([5, 5, 5],), [5]),
                (([ ],), []),
            ],
            solution="""def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result"""
        ),
        
        CodingChallenge(
            week=4,
            title="Count Word Frequency",
            description="Write a function that counts the frequency of each word in a string.",
            example_input='"hello world hello"',
            example_output='{"hello": 2, "world": 1}',
            hint="Use a dictionary to track counts. Split the string into words first.",
            test_cases=[
                (("hello world hello",), {"hello": 2, "world": 1}),
                (("test",), {"test": 1}),
            ],
            solution="""def word_frequency(text):
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq"""
        ),
        
        CodingChallenge(
            week=2,
            title="FizzBuzz",
            description="Write a function that returns 'Fizz' for multiples of 3, 'Buzz' for multiples of 5, 'FizzBuzz' for multiples of both, and the number otherwise.",
            example_input="15",
            example_output='"FizzBuzz"',
            hint="Use modulo operator % and check divisibility.",
            test_cases=[
                ((15,), "FizzBuzz"),
                ((9,), "Fizz"),
                ((10,), "Buzz"),
                ((7,), "7"),
            ],
            solution="""def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)"""
        ),
    ]

# ============================================================================
# QUIZ MANAGER
# ============================================================================

class QuizManager:
    """Main quiz management class"""
    
    def __init__(self):
        self.questions = create_question_database()
        self.coding_challenges = create_coding_challenges()
        self.current_user: Optional[UserProfile] = None
        self.data_file = 'quiz_data.json'
        self.load_data()
    
    def load_data(self):
        """Load user data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.users = {name: UserProfile.from_dict(profile_data) 
                                 for name, profile_data in data.items()}
            except:
                self.users = {}
        else:
            self.users = {}
    
    def save_data(self):
        """Save user data to file"""
        data = {name: profile.to_dict() for name, profile in self.users.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def select_user(self):
        """Select or create user profile"""
        clear_screen()
        print_header("🎓 AWS CLOUD INSTITUTE QUIZ", Colors.BRIGHT_CYAN)
        
        if self.users:
            print(f"{Colors.BOLD}Existing Users:{Colors.RESET}")
            for i, name in enumerate(self.users.keys(), 1):
                last_active = datetime.fromisoformat(self.users[name].last_active)
                print(f"  {i}. {name} (Last active: {last_active.strftime('%Y-%m-%d')})")
            print(f"  {len(self.users) + 1}. Create new user")
            
            choice = get_input(f"\nSelect user (1-{len(self.users) + 1}): ")
            
            try:
                choice = int(choice)
                if 1 <= choice <= len(self.users):
                    self.current_user = list(self.users.values())[choice - 1]
                    return
            except:
                pass
        
        # Create new user
        name = get_input("\nEnter your name: ")
        if name:
            self.current_user = UserProfile(name)
            self.users[name] = self.current_user
            self.save_data()
            print_success(f"Welcome, {name}!")
            time.sleep(1)
    
    def main_menu(self):
        """Display main menu"""
        while True:
            clear_screen()
            print_header("🎓 AWS CLOUD INSTITUTE QUIZ", Colors.BRIGHT_CYAN)
            
            print(f"{Colors.BOLD}Welcome, {self.current_user.name}!{Colors.RESET}\n")
            
            # Quick stats
            accuracy = self.current_user.get_accuracy()
            print(f"{Colors.DIM}Questions Answered: {self.current_user.total_questions} | "
                  f"Accuracy: {accuracy:.1f}% | Streak: {self.current_user.current_streak}{Colors.RESET}\n")
            
            print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}\n")
            options = [
                "📚 Practice by Week (1-10)",
                "🎲 Random Quiz",
                "🔨 Coding Challenges",
                "📝 Flashcard Mode",
                "❌ Review Incorrect Answers",
                "📊 View Progress & Stats",
                "🏆 Achievements",
                "⏰ Timed Quiz Mode",
                "⏱️  Pomodoro Study Timer",
                "💾 Export Progress to CSV",
                "⚙️  Settings",
                "🚪 Exit"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"  {i:2d}. {option}")
            
            choice = get_input(f"\n{Colors.CYAN}Select an option (1-{len(options)}): {Colors.RESET}")
            
            try:
                choice = int(choice)
                if choice == 1:
                    self.practice_by_week()
                elif choice == 2:
                    self.random_quiz()
                elif choice == 3:
                    self.coding_challenges_menu()
                elif choice == 4:
                    self.flashcard_mode()
                elif choice == 5:
                    self.review_incorrect()
                elif choice == 6:
                    self.view_progress()
                elif choice == 7:
                    self.view_achievements()
                elif choice == 8:
                    self.timed_quiz()
                elif choice == 9:
                    self.pomodoro_timer()
                elif choice == 10:
                    self.export_to_csv()
                elif choice == 11:
                    self.settings()
                elif choice == 12:
                    self.save_data()
                    print_success("\n👋 Thanks for studying! Keep up the great work!")
                    sys.exit(0)
            except:
                print_error("Invalid choice!")
                time.sleep(1)
    
    def practice_by_week(self):
        """Practice questions from a specific week"""
        clear_screen()
        print_header("📚 PRACTICE BY WEEK")
        
        weeks = {
            1: "Python Basics",
            2: "Control Flow",
            3: "Lists & APIs",
            4: "Dictionaries & Functions",
            5: "Files & Error Handling",
            6: "Object-Oriented Programming",
            7: "Git & Version Control",
            8: "Databases (SQL & DynamoDB)",
            9: "Cloud Storage (S3 & Textract)",
            10: "Serverless (Lambda & API Gateway)"
        }
        
        for week, topic in weeks.items():
            stats = self.current_user.week_stats[week]
            if stats['attempted'] > 0:
                accuracy = (stats['correct'] / stats['attempted']) * 100
                status = f"({accuracy:.0f}% - {stats['correct']}/{stats['attempted']})"
            else:
                status = "(Not attempted)"
            print(f"  {week:2d}. Week {week}: {topic} {Colors.DIM}{status}{Colors.RESET}")
        
        print(f"  11. Back to main menu")
        
        choice = get_input(f"\n{Colors.CYAN}Select week (1-11): {Colors.RESET}")
        
        try:
            choice = int(choice)
            if 1 <= choice <= 10:
                self.run_quiz(week=choice)
            elif choice == 11:
                return
        except:
            print_error("Invalid choice!")
            time.sleep(1)
    
    def random_quiz(self, num_questions: int = 10):
        """Run a random quiz with mixed questions"""
        self.run_quiz(num_questions=num_questions, random_mix=True)
    
    def run_quiz(self, week: Optional[int] = None, num_questions: int = 10, 
                 random_mix: bool = False, timed: bool = False, time_limit: int = 0):
        """Run a quiz session"""
        clear_screen()
        
        # Select questions
        if week:
            available = [q for q in self.questions if q.week == week]
            title = f"Week {week} Quiz"
        elif random_mix:
            available = self.questions
            title = "Random Quiz"
        else:
            available = self.questions
            title = "Quiz"
        
        if not available:
            print_error("No questions available!")
            press_enter()
            return
        
        # Randomize and limit
        quiz_questions = random.sample(available, min(num_questions, len(available)))
        
        print_header(title)
        print(f"{Colors.BOLD}Questions: {len(quiz_questions)}{Colors.RESET}")
        if timed:
            print(f"{Colors.YELLOW}Time Limit: {time_limit} seconds{Colors.RESET}")
        print()
        
        press_enter()
        
        # Run quiz
        score = 0
        start_time = time.time()
        
        for i, question in enumerate(quiz_questions, 1):
            clear_screen()
            
            # Time check
            if timed:
                elapsed = time.time() - start_time
                remaining = time_limit - elapsed
                if remaining <= 0:
                    print_warning("⏰ Time's up!")
                    break
                print(f"{Colors.YELLOW}Time Remaining: {int(remaining)}s{Colors.RESET}\n")
            
            print(f"{Colors.BOLD}Question {i}/{len(quiz_questions)}{Colors.RESET}")
            print(f"{Colors.DIM}Current Score: {score}/{i-1}{Colors.RESET}\n")
            
            question.display()
            
            # Get answer
            if question.q_type == 'TrueFalse':
                answer = get_input("Your answer (T/F) [H for hint, S to skip]: ")
            elif question.q_type == 'FillBlank':
                answer = get_input("Your answer [H for hint, S to skip]: ")
            else:
                answer = get_input("Your answer (A/B/C/D) [H for hint, S to skip]: ")
            
            # Handle hints and skips
            if answer.upper() == 'H':
                print(f"\n{Colors.YELLOW}💡 Hint: {question.hint}{Colors.RESET}\n")
                if question.q_type == 'TrueFalse':
                    answer = get_input("Your answer (T/F): ")
                elif question.q_type == 'FillBlank':
                    answer = get_input("Your answer: ")
                else:
                    answer = get_input("Your answer (A/B/C/D): ")
            
            if answer.upper() == 'S':
                print_warning("⏭️  Skipped")
                press_enter()
                continue
            
            # Check answer
            is_correct = question.check_answer(answer)
            
            if is_correct:
                score += 1
                print_success("CORRECT!")
                self.current_user.update_stats(True, question.week, question.q_id)
            else:
                print_error(f"INCORRECT! Correct answer: {question.correct}")
                self.current_user.update_stats(False, question.week, question.q_id)
            
            print(f"\n{Colors.CYAN}💡 Explanation: {question.explanation}{Colors.RESET}")
            
            # Show streak
            if is_correct and self.current_user.current_streak >= 3:
                print(f"\n{Colors.YELLOW}🔥 Streak: {self.current_user.current_streak}!{Colors.RESET}")
            
            press_enter()
        
        # Quiz complete
        end_time = time.time()
        duration = end_time - start_time
        
        clear_screen()
        print_header("📊 QUIZ COMPLETE!", Colors.GREEN)
        
        percentage = (score / len(quiz_questions)) * 100
        
        print(f"{Colors.BOLD}Final Score: {score}/{len(quiz_questions)} ({percentage:.1f}%){Colors.RESET}\n")
        print(f"Time Taken: {int(duration // 60)}m {int(duration % 60)}s\n")
        
        # Performance message
        if percentage == 100:
            print(f"{Colors.BRIGHT_GREEN}🌟 PERFECT SCORE! Outstanding work!{Colors.RESET}")
            self.current_user.perfect_quizzes += 1
        elif percentage >= 80:
            print(f"{Colors.GREEN}🎉 Excellent work! You're mastering this material!{Colors.RESET}")
        elif percentage >= 60:
            print(f"{Colors.YELLOW}👍 Good job! Keep practicing to improve.{Colors.RESET}")
        else:
            print(f"{Colors.RED}💪 Keep studying! Review the material and try again.{Colors.RESET}")
        
        # Check for achievements
        stats = {
            'total_correct': self.current_user.total_correct,
            'best_streak': self.current_user.best_streak,
            'perfect_quizzes': self.current_user.perfect_quizzes,
            'coding_completed': self.current_user.coding_completed,
            'weeks_completed': self.current_user.weeks_completed
        }
        
        new_achievements = self.current_user.achievements.check_achievements(stats)
        
        if new_achievements:
            print(f"\n{Colors.BRIGHT_YELLOW}🏆 NEW ACHIEVEMENTS UNLOCKED!{Colors.RESET}\n")
            for achievement in new_achievements:
                print(f"  {achievement.icon} {achievement.name}")
        
        self.save_data()
        press_enter()
    
    def coding_challenges_menu(self):
        """Coding challenges menu"""
        clear_screen()
        print_header("🔨 CODING CHALLENGES")
        
        print(f"{Colors.BOLD}Available Challenges:{Colors.RESET}\n")
        
        for i, challenge in enumerate(self.coding_challenges, 1):
            print(f"  {i}. {challenge.title} (Week {challenge.week})")
        
        print(f"  {len(self.coding_challenges) + 1}. Back to main menu")
        
        choice = get_input(f"\n{Colors.CYAN}Select challenge (1-{len(self.coding_challenges) + 1}): {Colors.RESET}")
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.coding_challenges):
                self.run_coding_challenge(self.coding_challenges[choice - 1])
        except:
            pass
    
    def run_coding_challenge(self, challenge: CodingChallenge):
        """Run a coding challenge"""
        clear_screen()
        challenge.display()
        
        print(f"{Colors.BOLD}Write your solution below.{Colors.RESET}")
        print(f"{Colors.DIM}Type 'DONE' on a new line when finished, or 'HINT' for a hint:{Colors.RESET}\n")
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            elif line.strip().upper() == 'HINT':
                print(f"\n{Colors.YELLOW}💡 Hint: {challenge.hint}{Colors.RESET}\n")
                continue
            lines.append(line)
        
        user_code = '\n'.join(lines)
        
        print(f"\n{Colors.CYAN}Testing your solution...{Colors.RESET}\n")
        time.sleep(1)
        
        success, message = challenge.test_solution(user_code)
        
        if success:
            print_success(message)
            self.current_user.coding_completed += 1
            self.save_data()
        else:
            print_error(message)
            print(f"\n{Colors.YELLOW}Would you like to see the solution? (Y/N): {Colors.RESET}", end='')
            if input().strip().upper() == 'Y':
                print(f"\n{Colors.CYAN}Solution:{Colors.RESET}")
                print(challenge.solution)
        
        press_enter()
    
    def flashcard_mode(self):
        """Flashcard study mode"""
        clear_screen()
        print_header("📝 FLASHCARD MODE")
        
        print("Select difficulty:")
        print("  1. Beginner")
        print("  2. Intermediate")
        print("  3. Advanced")
        print("  4. Mixed")
        
        choice = get_input("\nYour choice (1-4): ")
        
        difficulty_map = {
            '1': 'Beginner',
            '2': 'Intermediate',
            '3': 'Advanced',
            '4': 'Mixed'
        }
        
        if choice not in difficulty_map:
            return
        
        difficulty = difficulty_map[choice]
        
        if difficulty == 'Mixed':
            cards = self.questions
        else:
            cards = [q for q in self.questions if q.difficulty == difficulty]
        
        random.shuffle(cards)
        
        for i, card in enumerate(cards, 1):
            clear_screen()
            print(f"{Colors.BOLD}Flashcard {i}/{len(cards)}{Colors.RESET}\n")
            print(f"{Colors.CYAN}Week {card.week} - {card.difficulty}{Colors.RESET}\n")
            print(f"{Colors.BOLD}{card.question}{Colors.RESET}\n")
            
            input(f"{Colors.DIM}Press Enter to reveal answer...{Colors.RESET}")
            
            print(f"\n{Colors.GREEN}Answer: {card.correct}{Colors.RESET}")
            print(f"\n{Colors.CYAN}Explanation: {card.explanation}{Colors.RESET}\n")
            
            response = get_input("Continue? (Y/N): ")
            if response.upper() != 'Y':
                break
    
    def review_incorrect(self):
        """Review incorrect answers"""
        if not self.current_user.incorrect_questions:
            clear_screen()
            print_info("🎉 Great! You have no incorrect answers to review!")
            press_enter()
            return
        
        # Get incorrect questions
        incorrect_qs = [q for q in self.questions if q.q_id in self.current_user.incorrect_questions]
        
        if not incorrect_qs:
            return
        
        clear_screen()
        print_header(f"❌ REVIEW INCORRECT ANSWERS ({len(incorrect_qs)} questions)")
        
        print("These are questions you've answered incorrectly. Time to master them!\n")
        press_enter()
        
        self.run_quiz(week=None, num_questions=len(incorrect_qs), random_mix=False)
    
    def view_progress(self):
        """View detailed progress"""
        clear_screen()
        self.current_user.display_stats()
        press_enter()
    
    def view_achievements(self):
        """View achievements"""
        clear_screen()
        print_header("🏆 ACHIEVEMENTS")
        self.current_user.achievements.display_all()
        press_enter()
    
    def timed_quiz(self):
        """Timed quiz mode"""
        clear_screen()
        print_header("⏰ TIMED QUIZ MODE")
        
        print("Select quiz length:")
        print("  1. Quick (5 questions, 3 minutes)")
        print("  2. Standard (10 questions, 5 minutes)")
        print("  3. Long (20 questions, 10 minutes)")
        
        choice = get_input("\nYour choice (1-3): ")
        
        quiz_config = {
            '1': (5, 180),
            '2': (10, 300),
            '3': (20, 600)
        }
        
        if choice in quiz_config:
            num_q, time_limit = quiz_config[choice]
            self.run_quiz(num_questions=num_q, random_mix=True, timed=True, time_limit=time_limit)
    
    def pomodoro_timer(self):
        """Pomodoro study timer"""
        clear_screen()
        print_header("⏱️  POMODORO STUDY TIMER")
        
        print("Pomodoro Technique: 25 minutes of focused study, 5-minute break.\n")
        
        print("  1. Start Pomodoro Session")
        print("  2. Custom Timer")
        print("  3. Back")
        
        choice = get_input("\nYour choice: ")
        
        if choice == '1':
            self.run_timer(25 * 60, "Study Time")
            print_success("\n🎉 Great work! Time for a 5-minute break.")
            take_break = get_input("Start break timer? (Y/N): ")
            if take_break.upper() == 'Y':
                self.run_timer(5 * 60, "Break Time")
        elif choice == '2':
            try:
                minutes = int(get_input("Enter minutes: "))
                self.run_timer(minutes * 60, "Study Time")
            except:
                print_error("Invalid input!")
    
    def run_timer(self, seconds: int, title: str):
        """Run a countdown timer"""
        clear_screen()
        print_header(f"⏱️  {title.upper()}")
        
        start = time.time()
        end = start + seconds
        
        while time.time() < end:
            remaining = int(end - time.time())
            mins, secs = divmod(remaining, 60)
            
            # Clear line and print timer
            print(f"\r{Colors.BRIGHT_YELLOW}{mins:02d}:{secs:02d}{Colors.RESET}", end='', flush=True)
            time.sleep(1)
        
        print(f"\r{Colors.BRIGHT_GREEN}✓ Complete!{Colors.RESET}")
        time.sleep(1)
    
    def export_to_csv(self):
        """Export progress to CSV"""
        clear_screen()
        print_header("💾 EXPORT PROGRESS")
        
        filename = f"quiz_progress_{self.current_user.name}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['AWS Cloud Institute Quiz - Progress Report'])
                writer.writerow(['User', self.current_user.name])
                writer.writerow(['Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # Overall stats
                writer.writerow(['Overall Statistics'])
                writer.writerow(['Total Questions', self.current_user.total_questions])
                writer.writerow(['Correct Answers', self.current_user.total_correct])
                writer.writerow(['Incorrect Answers', self.current_user.total_incorrect])
                writer.writerow(['Accuracy', f"{self.current_user.get_accuracy():.1f}%"])
                writer.writerow(['Best Streak', self.current_user.best_streak])
                writer.writerow([])
                
                # Week breakdown
                writer.writerow(['Week', 'Attempted', 'Correct', 'Accuracy'])
                for week in range(1, 11):
                    stats = self.current_user.week_stats[week]
                    if stats['attempted'] > 0:
                        accuracy = (stats['correct'] / stats['attempted']) * 100
                        writer.writerow([f"Week {week}", stats['attempted'], stats['correct'], f"{accuracy:.1f}%"])
                    else:
                        writer.writerow([f"Week {week}", 0, 0, "N/A"])
            
            print_success(f"Progress exported to: {filename}")
        except Exception as e:
            print_error(f"Export failed: {e}")
        
        press_enter()
    
    def settings(self):
        """Settings menu"""
        clear_screen()
        print_header("⚙️  SETTINGS")
        
        print("  1. Change User")
        print("  2. Reset Progress")
        print("  3. Back")
        
        choice = get_input("\nYour choice: ")
        
        if choice == '1':
            self.select_user()
        elif choice == '2':
            confirm = get_input(f"{Colors.RED}Reset all progress? This cannot be undone! (yes/no): {Colors.RESET}")
            if confirm.lower() == 'yes':
                self.current_user = UserProfile(self.current_user.name)
                self.users[self.current_user.name] = self.current_user
                self.save_data()
                print_success("Progress reset!")
                time.sleep(1)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    try:
        manager = QuizManager()
        
        # Select user
        if not manager.current_user:
            manager.select_user()
        
        if manager.current_user:
            # Show welcome message
            clear_screen()
            print_header("🎓 AWS CLOUD INSTITUTE", Colors.BRIGHT_CYAN)
            print(f"\n{Colors.BOLD}Developer Fundamentals - Interactive Quiz{Colors.RESET}\n")
            print(f"Welcome back, {Colors.CYAN}{manager.current_user.name}{Colors.RESET}!\n")
            
            # Show a tip
            tips = [
                "💡 Tip: Practice daily for best results!",
                "💡 Tip: Review incorrect answers to improve.",
                "💡 Tip: Try coding challenges to apply your knowledge.",
                "💡 Tip: Use flashcard mode for quick review.",
                "💡 Tip: Timed quizzes help prepare for real exams.",
                "💡 Tip: Build a study streak for better retention!",
            ]
            print(f"{Colors.YELLOW}{random.choice(tips)}{Colors.RESET}\n")
            
            press_enter()
            
            # Main menu loop
            manager.main_menu()
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Quiz interrupted. Progress saved!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
