# Getting Started with DS-Tutor

**Last Updated:** January 2025
**Status:** Documentation for platform in development
**Note:** Platform testing in progress - instructions below are theoretical and need validation

---

## ⚠️ Important Notice

**DS-Tutor is currently in development.** The curriculum is 100% complete (57 lessons), but the Jupyter extension platform has not yet been tested in a real environment. This guide describes how the platform is *intended* to work, but functionality needs to be validated.

**Current Status:**
- ✅ **Curriculum:** 100% complete (57 lessons ready)
- 🚧 **Platform:** Code complete, testing in progress
- 🎯 **Beta:** Target Q2 2025

---

## Quick Installation

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Basic familiarity with Jupyter notebooks

### Step 1: Clone and Install

**Note:** DS-Tutor is not yet published to PyPI. Install from source:

```bash
# Clone the repository
git clone https://github.com/yourusername/ds-tutor.git
cd ds-tutor

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .
```

This will install DS-Tutor and all required dependencies.

### Step 2: Set Up API Key (Optional but Recommended)

DS-Tutor uses Claude AI for intelligent hints and feedback. To enable this feature:

1. Get an API key from [Anthropic Console](https://console.anthropic.com/)

2. Set the API key as an environment variable:

**Windows:**
```cmd
setx ANTHROPIC_API_KEY "your-api-key-here"
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

Or create a `.env` file in your working directory:
```
ANTHROPIC_API_KEY=your-api-key-here
```

**Note:** DS-Tutor will work without an API key, but you'll get basic hints instead of AI-powered personalized feedback.

---

## 🧪 Testing the Platform (Current Phase)

### 1. Start Jupyter Notebook

```bash
jupyter notebook
```

### 2. Create a New Notebook

Create a new Python notebook to test the extension.

### 3. Load the Extension (Untested)

In the first cell, try:

```python
%load_ext src
```

**Expected:** Welcome message should appear
**If it fails:** Report the error - this helps us fix it!

### 4. Initialize the Tutor (Untested)

```python
%dstutor init
```

**Expected:** Setup confirmation and progress tracking initialized
**If it fails:** Check error message and report

### 5. Explore Available Topics (Untested)

```python
%dstutor topics
```

**Expected:** List of 5 topics (Python, NumPy, Pandas, Matplotlib, Scikit-Learn)
**If it fails:** Lesson loading system needs debugging

### 6. Start Learning! (Untested)

```python
%dstutor start python
```

**Expected:**
- Lesson content displays
- Examples show with explanations
- Interactive exercise appears
- Navigation widget shows

**If it fails:** Please document what happens!

---

## 📚 Complete Curriculum

All 57 lessons are ready! Here's what you can learn:

### Module 1: Python Fundamentals (10 lessons, ~4.5 hours)
1. Variables and Types
2. Strings
3. Lists
4. Dictionaries
5. Control Flow
6. Functions
7. List Comprehensions
8. Error Handling
9. File I/O
10. Modules and Packages

### Module 2: NumPy Mastery (10 lessons, ~4.3 hours)
1. Array Creation
2. Array Attributes
3. Array Indexing
4. Array Slicing
5. Array Operations
6. Universal Functions
7. Broadcasting
8. Statistical Operations
9. Linear Algebra
10. Random Numbers

### Module 3: Pandas Deep Dive (15 lessons, ~7.8 hours)
1. Series Basics
2. DataFrames
3. Reading Data
4. Data Selection
5. Filtering Data
6. Data Cleaning
7. Handling Missing Data
8. GroupBy Operations
9. Merging DataFrames
10. Pivot Tables
11. String Operations
12. DateTime Operations
13. Apply Functions
14. Data Aggregation
15. Advanced Indexing

### Module 4: Matplotlib Visualization (10 lessons, ~4.8 hours)
1. Line Plots
2. Scatter Plots
3. Bar Charts
4. Histograms
5. Subplots
6. Customization
7. Styles and Themes
8. Advanced Plots
9. Seaborn Integration
10. Saving Figures

### Module 5: Scikit-Learn & ML (12 lessons, ~6.2 hours)
1. Introduction to ML
2. Train-Test Split
3. Linear Regression
4. Logistic Regression
5. Decision Trees
6. Random Forests
7. Evaluating Classification Models
8. Evaluating Regression Models
9. Preprocessing and Feature Scaling
10. Cross-Validation
11. Hyperparameter Tuning
12. Feature Selection

**Total:** 57 lessons, ~27.6 hours of content

---

## 🎯 How It Should Work

### Lesson Structure

Each lesson includes:

1. **Introduction** - Overview of what you'll learn
2. **Concepts** - Explanation of key ideas
3. **Examples** - Working code demonstrations (5-7 per lesson)
4. **Exercise** - Hands-on practice
5. **Validation** - Automatic checking of your solution
6. **Hints** - 3 levels of progressive help
7. **Solution** - Complete solution code
8. **Challenges** - Follow-up exercises

### Working Through Exercises

**Intended workflow:**

1. **Read the exercise instructions** carefully
2. **Write your code** in a cell below the exercise
3. **Execute the cell** - validation should happen automatically
4. **Get feedback** - See if your solution is correct

Example:
```python
# Exercise: Create an array with values 10, 20, 30, 40, 50
import numpy as np

result = np.array([10, 20, 30, 40, 50])
```

---

## 🆘 Getting Help (When Platform Works)

### Need a Hint?

```python
%dstutor hint
```

**Should provide:** Gentle nudge in the right direction

### Need More Help?

```python
%dstutor hint 2  # More specific hint
%dstutor hint 3  # Very specific hint
```

Hints get progressively more detailed.

### Want to See the Solution?

```python
%dstutor solution
```

**Note:** Try to solve it yourself first! Learning happens through struggle.

---

## 🧭 Navigating Lessons (Planned)

### Move to Next Lesson

```python
%dstutor next
```

### Go Back

```python
%dstutor previous
```

### Jump to a Specific Lesson

```python
%dstutor goto numpy_05
```

### Reset Current Lesson

```python
%dstutor reset
```

---

## 📊 Tracking Progress (Planned)

### View Your Progress Dashboard

```python
%dstutor progress
```

**Should show:**
- Lessons completed
- Exercises solved
- Accuracy percentage
- Current streak
- Topic-by-topic progress

### View Configuration

```python
%dstutor config
```

---

## 📖 Command Reference

### All Magic Commands (Theoretical)

| Command | Description | Status |
|---------|-------------|--------|
| `%dstutor init` | Initialize the tutor | 🚧 Untested |
| `%dstutor topics` | List all available topics | 🚧 Untested |
| `%dstutor start <topic>` | Start learning a topic | 🚧 Untested |
| `%dstutor next` | Go to next lesson | 🚧 Untested |
| `%dstutor previous` | Go to previous lesson | 🚧 Untested |
| `%dstutor goto <lesson_id>` | Jump to specific lesson | 🚧 Untested |
| `%dstutor hint [level]` | Get a hint (1-3) | 🚧 Untested |
| `%dstutor solution` | Show the solution | 🚧 Untested |
| `%dstutor progress` | View progress dashboard | 🚧 Untested |
| `%dstutor reset` | Reset current lesson | 🚧 Untested |
| `%dstutor config` | View configuration | 🚧 Untested |
| `%dstutor help` | Show help message | 🚧 Untested |

---

## 💡 Learning Tips

### 1. **Practice Daily**
Even 15-20 minutes per day is better than long infrequent sessions.

### 2. **Don't Skip Exercises**
The exercises are where real learning happens. Try to solve them yourself before looking at hints.

### 3. **Experiment**
Modify example code to see what happens. Break things and figure out why!

### 4. **Use Hints Wisely**
- Try solving first
- Use hint level 1 if stuck
- Only use higher levels if really needed
- Avoid jumping straight to the solution

### 5. **Review Regularly**
Go back to previous lessons occasionally to reinforce concepts.

### 6. **Take Notes**
Add markdown cells with your own notes and insights.

---

## 📅 Recommended Learning Schedules

### Intensive (4-6 weeks)
- **Time:** 6-8 hours/week
- **Pace:** 2-3 lessons per day
- **Duration:** 4-6 weeks
- **Best for:** Career changers, bootcamp style

### Relaxed (12-16 weeks)
- **Time:** 2-3 hours/week
- **Pace:** 4-5 lessons per week
- **Duration:** 12-16 weeks
- **Best for:** Working professionals

### Weekend Warrior (3-4 months)
- **Time:** 4-5 hours/weekend
- **Pace:** 6-8 lessons per week
- **Duration:** 3-4 months
- **Best for:** Students, hobbyists

---

## 🔧 Troubleshooting

### Extension Won't Load

**Problem:** `ModuleNotFoundError` when loading extension

**Solution:**
```bash
cd path/to/ds-tutor
pip install -e .
```

Make sure you're in the project directory and have activated your virtual environment.

### API Key Not Working

**Problem:** Getting basic hints instead of AI feedback

**Solution:**
1. Check your API key is set correctly
2. Verify it in the notebook:
```python
import os
print(os.getenv("ANTHROPIC_API_KEY"))
```
3. Restart the Jupyter kernel after setting the environment variable

### Database Issues

**Problem:** Progress not saving

**Solution:**
The progress database is stored in `~/.dstutor/progress.db`. If it gets corrupted:
```python
import os
from pathlib import Path

# Remove the database (will reset ALL progress)
db_path = Path.home() / ".dstutor" / "progress.db"
if db_path.exists():
    os.remove(db_path)
```

Then reinitialize: `%dstutor init`

### Validation Not Working

**Problem:** Code seems correct but validation fails

**Solution:**
1. Check that your result is stored in a variable named `result`
2. Make sure data types match exactly (array vs list, int vs float)
3. Use `%dstutor solution` to compare with expected solution
4. Check for subtle differences (spaces, case, etc.)

---

## 🎓 Expected Learning Outcomes

After completing all 57 lessons, you should be able to:

### Data Manipulation
- Load, clean, and transform datasets
- Handle missing and messy data
- Merge and join multiple data sources
- Aggregate and pivot data
- Work with dates, times, and text

### Numerical Computing
- Create and manipulate arrays efficiently
- Perform vectorized operations
- Use broadcasting for complex operations
- Calculate statistics
- Apply linear algebra

### Data Visualization
- Create all fundamental plot types
- Build multi-panel visualizations
- Customize plots professionally
- Generate publication-ready figures
- Use Seaborn for statistical plots

### Machine Learning
- Understand ML workflow
- Prepare data for modeling
- Build classification models
- Build regression models
- Evaluate model performance
- Tune hyperparameters
- Select important features
- Use cross-validation

**Skill Level:** Intermediate Data Scientist
**Ready For:** Real-world projects, Kaggle competitions, data science interviews

---

## 🐛 Found a Bug?

Since DS-Tutor is in development, bugs are expected!

**Please report:**
1. What command you ran
2. What error you got
3. What you expected to happen
4. Your environment (OS, Python version, Jupyter version)

**Where to report:**
- GitHub Issues (preferred)
- Email: [your-email]
- Discussion forum: [link]

---

## 🤝 Want to Help?

### Ways to Contribute

1. **Test the Platform**
   - Try the installation
   - Run commands
   - Report bugs
   - Suggest improvements

2. **Improve Documentation**
   - Fix typos
   - Clarify instructions
   - Add examples
   - Translate

3. **Create Content**
   - Suggest new lessons
   - Create practice datasets
   - Write challenges
   - Record tutorials

4. **Develop Features**
   - Fix bugs
   - Add functionality
   - Improve UI
   - Optimize performance

---

## 📚 Additional Resources

### Official Documentation
- **README.md** - Project overview
- **DESIGN.md** - Technical architecture
- **docs/FOUNDATIONS_STATUS.md** - Curriculum status
- **docs/PROJECT_STATUS.md** - Development status

### External Resources
- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
- [Scikit-Learn Documentation](https://scikit-learn.org/stable/)

### Learning Resources
- [Python for Data Analysis (Book)](https://wesmckinney.com/book/)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [DataCamp](https://www.datacamp.com/)
- [Real Python](https://realpython.com/)

---

## 🎯 Current Status Summary

**Curriculum:** ✅ 100% Complete
- All 57 lessons created
- All exercises validated
- All hints and solutions written
- Production-ready content

**Platform:** 🚧 In Development
- Framework code complete (~2,400 lines)
- Needs testing in Jupyter
- Needs integration validation
- Target beta: Q2 2025

**Your Role:**
If you're reading this, you might be one of our first testers! Your feedback is invaluable. Try the platform, report issues, and help us make DS-Tutor better!

---

## 🚀 Next Steps

1. **Install DS-Tutor** following the instructions above
2. **Try loading the extension** and report results
3. **Test basic commands** and document behavior
4. **Explore the curriculum** in the `/lessons/` directory
5. **Join the community** and stay updated
6. **Provide feedback** to help us improve

---

**Thank you for your interest in DS-Tutor! Together we're building the best way to learn Data Science.** 🎓📊🤖

---

## 📧 Contact

- **GitHub:** [repository-link]
- **Email:** [your-email]
- **Discord:** [server-invite] (if applicable)
- **Twitter:** [handle] (if applicable)

---

**Remember:** DS-Tutor is in active development. Expect rough edges, but also expect rapid improvements. Your patience and feedback help make this better for everyone!
