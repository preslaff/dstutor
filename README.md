# 🎓 DS-Tutor: AI-Powered Data Science Learning in Jupyter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Lessons](https://img.shields.io/badge/Lessons-57%2F57-green.svg)]()
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

**Learn Data Science by doing, right in your Jupyter notebooks, with AI-powered guidance every step of the way.**

DS-Tutor is an interactive Jupyter notebook extension that provides personalized, hands-on Data Science education. From Python fundamentals to machine learning with scikit-learn, learn progressively with real-time feedback, intelligent hints, and adaptive difficulty.

---

## 📢 Project Status

**🎯 What's Complete:**
- ✅ **Full Curriculum**: All 57 lessons written and ready (Python, NumPy, Pandas, Matplotlib, Scikit-Learn)
- ✅ **Learning Materials**: Concepts, examples, exercises, solutions, and hints
- ✅ **Structured Content**: YAML-based lesson format for easy integration

**🚧 What's In Development:**
- 🔲 Jupyter notebook extension (magic commands like `%dstutor start`)
- 🔲 Auto-validation system for exercises
- 🔲 AI-powered feedback integration
- 🔲 Interactive widgets and progress tracking

**📅 Timeline:**
- **Now**: All educational content ready for review and contribution
- **Q2 2025**: Beta release with working Jupyter extension
- **Q3 2025**: Public v1.0 release on PyPI

**💡 How You Can Help:**
- Review lesson content and provide feedback
- Report issues or suggest improvements
- Contribute to the platform development
- Star the repo to show support! ⭐

---

## ✨ Features

### 🎓 **Comprehensive Curriculum (100% Complete)** ✅
- **57 lessons** covering Python fundamentals through intermediate ML
- **Foundations**: Python (10), NumPy (10), Pandas (15), Matplotlib (10)
- **Intermediate**: Scikit-Learn (12) - complete ML pipeline
- **150+ exercises** with solutions and progressive hints
- **Real-world examples** in every lesson
- **Progressive difficulty** that grows with you

### 📖 **Rich Learning Materials** ✅
- Clear concept explanations for every topic
- 5-7 code examples per lesson with expected outputs
- Hands-on exercises to practice skills
- 3-level hint system (gentle → detailed → solution)
- Follow-up challenges to deepen understanding
- Additional resources and documentation links

### 🎯 **Structured Learning Path** ✅
- Prerequisites tracked between lessons
- Recommended learning sequences
- Module-based organization (5 modules)
- Estimated time for each lesson
- Clear learning objectives

### 🚧 **Platform Features (Coming Soon)**
These features are planned for the Jupyter extension:
- 🔲 **Magic Commands**: `%dstutor start`, `%dstutor hint`, etc.
- 🔲 **Auto-Validation**: Instant feedback on exercise completion
- 🔲 **AI-Powered Hints**: Contextual help from Claude AI
- 🔲 **Progress Tracking**: Visual dashboard and statistics
- 🔲 **Interactive Widgets**: Beautiful UI in Jupyter notebooks

---

## 🚀 Quick Start

### Installation

> **Note**: DS-Tutor is currently in active development and not yet published to PyPI. Install from source:

```bash
# Clone the repository
git clone https://github.com/yourusername/ds-tutor.git
cd ds-tutor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

**Coming soon**: `pip install ds-tutor` (v0.1.0 release planned)

### Explore the Curriculum Now

While the Jupyter extension is under development, you can explore all 57 lessons:

```bash
# Navigate to lessons directory
cd lessons/

# View lesson structure
lessons/
├── foundations/
│   ├── python/         # 10 Python lessons
│   ├── numpy/          # 10 NumPy lessons
│   ├── pandas/         # 15 Pandas lessons
│   └── matplotlib/     # 10 Matplotlib lessons
└── intermediate/
    └── sklearn/        # 12 Scikit-Learn lessons
```

**Each lesson is a YAML file containing:**
- Introduction and learning objectives
- Detailed concept explanations
- 5-7 code examples with outputs
- Hands-on exercises
- Solutions and 3-level hints
- Follow-up challenges

**Example**: Open `lessons/foundations/python/python_01_variables_types.yaml` to see a complete lesson structure.

### Once Released (Coming Soon)

1. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Load the Extension**
   ```python
   %load_ext dstutor
   ```

3. **Initialize Your Learning Journey**
   ```python
   %dstutor init
   ```

4. **Start Learning!**
   ```python
   %dstutor start python
   ```

The extension will guide you through interactive lessons with automatic feedback.

---

## 📚 Complete Curriculum Plan

### 🎓 Learning Methodology

DS-Tutor follows a **progressive, project-based** learning approach:

1. **Learn by Doing**: Every lesson includes hands-on exercises
2. **Build on Fundamentals**: Each lesson assumes knowledge from previous lessons
3. **Real-World Focus**: Examples use actual data science workflows
4. **Adaptive Difficulty**: Lessons start simple and gradually increase in complexity
5. **AI-Powered Feedback**: Get personalized help when you need it

### 📊 Curriculum Overview

**Total: 57 Lessons | Estimated Time: 50-70 hours**

```
Foundations (Beginner)       ████████████████████ 45 lessons (100%)
├─ Python                    ██████ 10 lessons
├─ NumPy                     ██████ 10 lessons
├─ Pandas                    ████████████ 15 lessons
└─ Matplotlib                ██████ 10 lessons

Intermediate (ML Pipeline)   ████████ 12 lessons (100%)
└─ Scikit-Learn              ████████ 12 lessons
```

---

## 📖 Detailed Curriculum

### 🔰 LEVEL 1: FOUNDATIONS (45 Lessons)

Complete these in order to build a solid foundation in Data Science tools.

---

#### 🐍 **Module 1: Python Fundamentals** (10 lessons, ~5 hours)

**Why Start Here?**
Even if you know Python, these lessons cover the specific patterns and idioms used throughout Data Science.

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `python_01` | Variables & Types | 20 min | int, float, str, bool, type conversion |
| `python_02` | Strings | 30 min | Slicing, methods, f-strings |
| `python_03` | Lists | 30 min | Indexing, methods, mutability |
| `python_04` | Dictionaries | 30 min | Key-value pairs, methods, iteration |
| `python_05` | Control Flow | 30 min | if/elif/else, comparison, logical operators |
| `python_06` | Loops | 30 min | for, while, break, continue, enumerate |
| `python_07` | Functions | 35 min | def, parameters, return, *args, **kwargs |
| `python_08` | Comprehensions | 30 min | List/dict comprehensions, conditionals |
| `python_09` | Tuples & Sets | 25 min | Immutability, uniqueness, set operations |
| `python_10` | Error Handling | 30 min | try/except/finally, exception types |

**Learning Path**: Complete sequentially. Each lesson builds vocabulary for the next.

**Milestone**: After completing Python, you'll be ready to work with NumPy arrays and Pandas DataFrames.

---

#### 🔢 **Module 2: NumPy Mastery** (10 lessons, ~6 hours)

**Why NumPy?**
NumPy is the foundation of all numerical computing in Python. Pandas and scikit-learn are built on top of NumPy.

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `numpy_01` | Arrays Intro | 30 min | ndarray, shape, dtype, array creation |
| `numpy_02` | Array Indexing | 35 min | Slicing, fancy indexing, boolean indexing |
| `numpy_03` | Array Operations | 35 min | Element-wise ops, universal functions |
| `numpy_04` | Broadcasting | 40 min | Shape compatibility, automatic expansion |
| `numpy_05` | Aggregations | 30 min | sum, mean, std, min, max, axis parameter |
| `numpy_06` | Reshaping Arrays | 35 min | reshape, flatten, transpose, newaxis |
| `numpy_07` | Stacking & Splitting | 30 min | vstack, hstack, split, concatenate |
| `numpy_08` | Linear Algebra | 35 min | dot product, matrix multiplication, inv |
| `numpy_09` | Random Numbers | 30 min | rand, randn, randint, seed, choice |
| `numpy_10` | Performance Tips | 35 min | Vectorization, memory layout, views vs copies |

**Prerequisites**: Python basics (Module 1)

**Learning Path**:
- Complete `numpy_01-03` first (array fundamentals)
- `numpy_04` (broadcasting) is crucial - spend extra time here
- `numpy_05-07` (operations) can be done in any order
- `numpy_08-10` (advanced topics) build on everything

**Milestone**: You'll be comfortable with array manipulation, the core skill for Data Science.

---

#### 🐼 **Module 3: Pandas Deep Dive** (15 lessons, ~9 hours)

**Why Pandas?**
Pandas is THE tool for data manipulation. 80% of Data Science work is data wrangling with Pandas.

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `pandas_01` | Series Basics | 30 min | 1D labeled arrays, indexing, attributes |
| `pandas_02` | DataFrames Intro | 35 min | 2D tables, columns, rows, info() |
| `pandas_03` | Reading Data | 30 min | read_csv, read_excel, parameters |
| `pandas_04` | Indexing with loc/iloc | 40 min | Label vs position, boolean indexing |
| `pandas_05` | Selecting Data | 35 min | Column selection, filtering, queries |
| `pandas_06` | Adding/Modifying Columns | 30 min | Assignment, calculated columns, drop |
| `pandas_07` | Sorting & Ranking | 30 min | sort_values, sort_index, rank |
| `pandas_08` | Missing Data | 35 min | isna, dropna, fillna, imputation |
| `pandas_09` | GroupBy Basics | 40 min | Grouping, aggregation, transform |
| `pandas_10` | GroupBy Advanced | 40 min | Multiple aggregations, named agg |
| `pandas_11` | Pivot Tables | 35 min | pivot_table, margins, aggfunc |
| `pandas_12` | Time Series | 35 min | DatetimeIndex, resample, rolling |
| `pandas_13` | DateTime Operations | 35 min | to_datetime, dt accessor, Timedelta |
| `pandas_14` | Apply & Map | 35 min | apply, map, lambda, custom functions |
| `pandas_15` | Advanced Filtering | 30 min | query, isin, between, string methods |

**Prerequisites**: Python basics (Module 1), NumPy fundamentals (Module 2, lessons 1-5)

**Learning Path**:
- **Phase 1 (Basics)**: `pandas_01-03` - Learn Series, DataFrames, data loading
- **Phase 2 (Selection)**: `pandas_04-06` - Master data selection and modification
- **Phase 3 (Manipulation)**: `pandas_07-08` - Sorting and handling missing data
- **Phase 4 (Aggregation)**: `pandas_09-11` - GroupBy and pivot tables (most powerful!)
- **Phase 5 (Advanced)**: `pandas_12-15` - Time series, apply/map, advanced filtering

**Critical Lessons**:
- `pandas_04` (loc/iloc): Core skill - practice extensively
- `pandas_09-10` (GroupBy): This is where Pandas shines
- `pandas_14` (Apply): Unlock custom transformations

**Milestone**: You can load, clean, transform, and analyze any tabular dataset.

---

#### 📊 **Module 4: Matplotlib Visualization** (10 lessons, ~6 hours)

**Why Matplotlib?**
Visualization is crucial for understanding data. Matplotlib gives you complete control over your plots.

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `matplotlib_01` | Plotting Basics | 30 min | plot, figure, axes, basic customization |
| `matplotlib_02` | Line Plots | 35 min | Multiple lines, styles, markers, legends |
| `matplotlib_03` | Scatter Plots | 30 min | plt.scatter, colors, sizes, alpha |
| `matplotlib_04` | Bar Charts | 35 min | Vertical/horizontal bars, grouped bars |
| `matplotlib_05` | Histograms | 35 min | Distributions, bins, density plots |
| `matplotlib_06` | Subplots | 40 min | Multiple plots, layouts, sharing axes |
| `matplotlib_07` | Customization | 35 min | Colors, fonts, styles, grids, spines |
| `matplotlib_08` | Saving Figures | 25 min | savefig, DPI, formats, bbox_inches |
| `matplotlib_09` | Advanced Plots | 40 min | Box plots, violin plots, heatmaps |
| `matplotlib_10` | Real-World Examples | 40 min | Complete workflows, publication-quality |

**Prerequisites**: Python (Module 1), NumPy basics (numpy_01-05), Pandas basics (pandas_01-06)

**Learning Path**:
- **Phase 1 (Fundamentals)**: `matplotlib_01-03` - Basic plot types
- **Phase 2 (More Types)**: `matplotlib_04-05` - Bars and distributions
- **Phase 3 (Composition)**: `matplotlib_06-07` - Subplots and styling
- **Phase 4 (Advanced)**: `matplotlib_08-10` - Production-ready visualizations

**Pro Tips**:
- Always start with `matplotlib_01` to understand figure/axes architecture
- `matplotlib_06` (Subplots) is essential for dashboards
- Practice `matplotlib_07` (Customization) to make professional plots

**Milestone**: You can create publication-quality visualizations to explore and present data.

---

### 🚀 LEVEL 2: INTERMEDIATE - MACHINE LEARNING (12 Lessons)

Build complete machine learning pipelines with scikit-learn.

---

#### 🤖 **Module 5: Scikit-Learn & Machine Learning** (12 lessons, ~7 hours)

**Why Scikit-Learn?**
Industry-standard library for classical machine learning. Powers most production ML systems.

**Part 1: ML Fundamentals & Models** (Lessons 1-6)

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `sklearn_01` | Intro to ML | 30 min | Supervised vs unsupervised, fit/predict, first model |
| `sklearn_02` | Train-Test Split | 30 min | Avoiding overfitting, stratification, random_state |
| `sklearn_03` | Linear Regression | 30 min | Coefficients, R², making predictions |
| `sklearn_04` | Logistic Regression | 30 min | Classification, probabilities, multiclass |
| `sklearn_05` | Decision Trees | 30 min | Tree structure, max_depth, feature importance |
| `sklearn_06` | Random Forests | 30 min | Ensemble learning, n_estimators, OOB score |

**Part 2: Evaluation & Optimization** (Lessons 7-12)

| Lesson | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| `sklearn_07` | Evaluating Classification | 30 min | Confusion matrix, precision, recall, F1, ROC-AUC |
| `sklearn_08` | Evaluating Regression | 30 min | MSE, RMSE, MAE, R², residual analysis |
| `sklearn_09` | Preprocessing & Scaling | 35 min | StandardScaler, encoders, pipelines |
| `sklearn_10` | Cross-Validation | 30 min | K-fold, stratified, reliable evaluation |
| `sklearn_11` | Hyperparameter Tuning | 35 min | GridSearchCV, RandomizedSearchCV |
| `sklearn_12` | Feature Selection | 35 min | SelectKBest, RFE, feature importance |

**Prerequisites**:
- **Required**: All Foundation modules (Python, NumPy, Pandas, Matplotlib)
- **Especially**: Pandas (for data manipulation), NumPy (arrays), Matplotlib (plotting results)

**Learning Path**:

**Phase 1: Get Started (Lessons 1-2)**
- `sklearn_01`: Understand the ML workflow
- `sklearn_02`: Learn proper train-test splitting
- *Goal*: Understand the basics before diving into algorithms

**Phase 2: Learn Algorithms (Lessons 3-6)**
- `sklearn_03-04`: Start with regression and classification fundamentals
- `sklearn_05-06`: Move to tree-based models (more powerful!)
- *Goal*: Build intuition for when to use each algorithm

**Phase 3: Evaluate Properly (Lessons 7-8)**
- `sklearn_07`: Master classification metrics
- `sklearn_08`: Master regression metrics
- *Goal*: Know how to measure model performance

**Phase 4: Build Production Pipelines (Lessons 9-12)**
- `sklearn_09`: Preprocessing (critical for real data!)
- `sklearn_10`: Cross-validation (reliable evaluation)
- `sklearn_11`: Hyperparameter tuning (optimize performance)
- `sklearn_12`: Feature selection (simplify models)
- *Goal*: Build complete, production-ready ML pipelines

**Critical Lessons**:
- `sklearn_02` (Train-Test Split): Avoid the #1 beginner mistake
- `sklearn_07-08` (Evaluation): Choose the right metrics for your problem
- `sklearn_09` (Preprocessing): Real data is never clean
- `sklearn_10` (Cross-Validation): Get reliable performance estimates

**Real-World Workflow**:
```python
# This is what you'll be able to do after Module 5:

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# 1. Build pipeline (preprocessing + model)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])

# 2. Define hyperparameter search
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [10, 20, None]
}

# 3. Tune with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# 4. Evaluate
print(f"Best score: {grid_search.best_score_}")
print(f"Test score: {grid_search.score(X_test, y_test)}")
```

**Milestone**: You can build, evaluate, and optimize complete machine learning pipelines on real datasets.

---

## 🎯 How to Use This Curriculum

### 📅 Recommended Learning Schedule

**Option 1: Intensive (4-6 weeks)**
- **Week 1**: Python + NumPy fundamentals
- **Week 2**: NumPy advanced + Pandas basics
- **Week 3**: Pandas advanced + Matplotlib
- **Week 4**: Scikit-learn models & evaluation
- **Week 5-6**: Scikit-learn optimization & practice projects

**Option 2: Relaxed (12-16 weeks)**
- **Weeks 1-3**: Python fundamentals (3-4 lessons/week)
- **Weeks 4-6**: NumPy (3-4 lessons/week)
- **Weeks 7-11**: Pandas (3 lessons/week)
- **Weeks 12-14**: Matplotlib (3-4 lessons/week)
- **Weeks 15-16**: Scikit-learn (6 lessons/week)

**Option 3: Weekend Warrior (3-4 months)**
- **Weekends only**: 2-3 lessons per weekend session
- Focus on one module at a time
- Complete practice projects between modules

### 🎓 Learning Tips

#### Before Starting
1. ✅ Install Jupyter Notebook and DS-Tutor extension
2. ✅ Set up your Claude API key for AI assistance
3. ✅ Create a dedicated notebook for notes and experiments
4. ✅ Set realistic goals (consistency > intensity)

#### During Lessons
1. 📖 **Read the concept explanation** before coding
2. 💻 **Type the code** yourself (don't copy-paste)
3. 🔬 **Experiment** - modify examples to test your understanding
4. 📝 **Take notes** in markdown cells
5. 🤔 **Try before hints** - struggle is part of learning
6. ✅ **Complete exercises** before moving on

#### After Each Module
1. 📊 **Build a mini-project** using the skills learned
2. 📚 **Review previous lessons** if concepts feel shaky
3. 🎯 **Practice with real datasets** from Kaggle or UCI
4. 📖 **Read documentation** to go deeper
5. 💬 **Explain concepts** to someone (or your rubber duck)

### 🚫 Common Pitfalls to Avoid

1. ❌ **Skipping Python fundamentals** - Even if you know Python, review Module 1
2. ❌ **Rushing through NumPy** - It's the foundation; take your time
3. ❌ **Not practicing Pandas enough** - You'll use this 80% of the time
4. ❌ **Ignoring visualizations** - Matplotlib seems tedious but is essential
5. ❌ **Jumping to models too quickly** - Master preprocessing first
6. ❌ **Only reading, not coding** - You must write code to learn
7. ❌ **Skipping exercises** - Exercises solidify understanding

### ✅ Success Indicators

You're ready to move on when:
- ✅ You can complete exercises without hints
- ✅ You can modify examples to solve new problems
- ✅ You understand WHY the code works, not just HOW
- ✅ You can explain concepts in your own words

---

## 📖 Usage Guide

> **Note**: The magic commands shown below are the planned interface for the Jupyter extension (currently in development). For now, you can explore all lesson content in the `/lessons/` directory.

### Basic Commands (Coming Soon)

#### Starting a Lesson
```python
# Show all available topics
%dstutor topics

# Start learning a specific topic
%dstutor start python          # Begin Python lessons
%dstutor start numpy           # Begin NumPy lessons
%dstutor start pandas          # Begin Pandas lessons
%dstutor start sklearn         # Begin scikit-learn lessons
```

#### During Lessons
```python
# Get a hint for the current exercise
%dstutor hint

# Get a more detailed hint
%dstutor hint 2

# Show the complete solution
%dstutor solution

# Move to the next lesson
%dstutor next

# Go back to previous lesson
%dstutor previous
```

#### Progress & Navigation
```python
# View your progress dashboard
%dstutor progress

# List completed lessons
%dstutor completed

# Reset current lesson (start over)
%dstutor reset

# Jump to a specific lesson
%dstutor goto pandas_03
```

### Example Learning Session

```python
# 1. Load the extension
%load_ext dstutor

# 2. Start learning Pandas
%dstutor start pandas

# --- Lesson content appears automatically ---
# --- Work through the examples ---

# 3. Try the exercise
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.loc[df['A'] > 1, 'B']

# ✅ Automatic validation happens when you run the cell
# Feedback widget appears with results

# 4. Need help?
%dstutor hint

# 5. Move on when ready
%dstutor next
```

---

## 🛠️ Configuration

### API Keys

DS-Tutor uses Claude AI for intelligent feedback. Set up your API key:

```python
# Option 1: In your notebook
%dstutor config --api-key YOUR_ANTHROPIC_API_KEY

# Option 2: Environment variable
export ANTHROPIC_API_KEY=your_key_here

# Option 3: .env file in your project
# Create .env file with:
ANTHROPIC_API_KEY=your_key_here
```

Get your API key at: [Anthropic Console](https://console.anthropic.com/)

### Preferences

Customize your learning experience:

```python
# Set difficulty preference
%dstutor config --difficulty medium  # easy, medium, hard

# Enable/disable auto-validation
%dstutor config --auto-validate on

# Set hint style
%dstutor config --hint-style progressive  # progressive, direct

# Choose feedback verbosity
%dstutor config --feedback verbose  # brief, normal, verbose
```

---

## 📊 Example Lesson Flow

Here's what a typical lesson looks like:

### 1. Lesson Introduction (Markdown Cell)
```markdown
# Pandas DataFrame Indexing

Learn how to select specific rows and columns using .loc[] and .iloc[]

**Learning Objectives:**
- Understand label-based vs position-based indexing
- Use .loc[] for conditional selection
- Combine row and column selection
```

### 2. Concept Explanation (Markdown Cell)
```markdown
## Two Main Indexing Methods

- **.loc[]**: Label-based (use row/column names)
- **.iloc[]**: Position-based (use integer positions)

Both support single values, lists, slices, and boolean masks.
```

### 3. Example Code (Code Cell - Auto-executed)
```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

# Select rows where age > 28
result = df.loc[df['age'] > 28, ['name', 'city']]
print(result)
```

### 4. Exercise (Code Cell - Your Turn!)
```python
# Exercise: Select all rows where age >= 30
# Return only 'name' and 'city' columns
# Store result in variable called 'result'

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 32],
    'city': ['NYC', 'LA', 'Chicago', 'Boston', 'Seattle']
})

# Your code here
result =
```

### 5. Instant Feedback

**If Correct:**
```
✅ Perfect! Well done!

Your solution efficiently uses .loc[] for both filtering and column
selection. This is the idiomatic pandas approach.

💡 Pro tip: You can also chain multiple conditions with & and |

🎯 Ready for the next challenge!
```

**If Incorrect:**
```
⚠️ Almost there!

Your filtering condition is correct, but check your column selection.

Need a hint? Use: %dstutor hint
```

### 6. Progressive Hints

```python
%dstutor hint  # First hint
```
```
💡 Hint 1/3:
Think about the structure: df.loc[rows, columns]
Your row condition looks good!
```

```python
%dstutor hint 2  # More specific
```
```
💡 Hint 2/3:
Use a list ['name', 'city'] for the columns parameter
Structure: df.loc[df['age'] >= 30, ['name', 'city']]
```

```python
%dstutor solution  # Complete solution
```
```
💡 Solution:
result = df.loc[df['age'] >= 30, ['name', 'city']]

This filters rows where age >= 30 and selects only name and city columns.
```

---

## 🎯 Practice Projects

After completing each module, reinforce your learning with these projects:

### After Python Fundamentals
- 📝 **Text Analyzer**: Count words, find patterns, analyze frequency
- 🎲 **Game Simulator**: Build a dice game with functions and loops

### After NumPy
- 📊 **Statistical Calculator**: Compute stats on numerical arrays
- 🎨 **Image Manipulation**: Basic operations on image arrays

### After Pandas
- 📈 **Sales Dashboard**: Analyze sales data with groupby and pivots
- 🧹 **Data Cleaner**: Clean messy CSV files automatically

### After Matplotlib
- 📊 **Visualization Suite**: Create a dashboard with multiple plot types
- 📉 **Stock Tracker**: Visualize stock price trends

### After Scikit-Learn
- 🏠 **House Price Predictor**: Regression project with feature engineering
- 🎯 **Customer Churn Predictor**: Classification with model tuning
- 📊 **Complete ML Pipeline**: End-to-end project from data to deployment

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Lessons

Lessons are defined in YAML format. See `/lessons/` directory for examples.

```yaml
lesson:
  id: "pandas_new_lesson"
  level: "beginner"
  topic: "pandas"
  subtopic: "Your Topic"
  order: 16

  content:
    introduction: |
      # Your Lesson Title
      Learn something awesome!

    concept: |
      ## Detailed explanation here

    examples:
      - title: "Example Name"
        code: |
          # Your example code
        output: |
          # Expected output

  exercise:
    instruction: "Do something cool"
    solution: "# Solution code"
    validation:
      type: "value_check"
      checks:
        - variable: "result"
          type: "dataframe"
```

### Reporting Issues

Found a bug or have a suggestion?

1. Check [existing issues](https://github.com/yourusername/ds-tutor/issues)
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ds-tutor.git
cd ds-tutor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/
```

---

## 📋 Requirements

### Minimum Requirements
- Python 3.8+
- Jupyter Notebook 6.5+ or JupyterLab 3.0+
- 4GB RAM
- Internet connection (for AI features)

### Dependencies
```
ipython>=8.0.0
jupyter>=1.0.0
ipywidgets>=8.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
anthropic>=0.25.0
pyyaml>=6.0
```

---

## 🗺️ Roadmap

### 🚧 Current Status (v0.1.0-dev) - IN DEVELOPMENT
**Curriculum: 100% Complete** ✅
- ✅ Python fundamentals (10 lessons)
- ✅ NumPy complete curriculum (10 lessons)
- ✅ Pandas complete curriculum (15 lessons)
- ✅ Matplotlib complete curriculum (10 lessons)
- ✅ Scikit-learn complete curriculum (12 lessons)
- ✅ **57 total lessons - fully written and ready!**

**Platform: In Development** 🚧
- 🔲 Jupyter notebook extension framework
- 🔲 Magic command system (%dstutor)
- 🔲 Auto-validation engine
- 🔲 AI feedback integration (Claude API)
- 🔲 Progress tracking system
- 🔲 Interactive widgets

**Target**: Public beta release Q2 2025

### Coming Soon (v0.2.0)
- 🔲 Advanced widgets and improved UI
- 🔲 Practice mode with random exercises
- 🔲 Project templates and guided projects
- 🔲 Performance improvements
- 🔲 Extended datasets library
- 🔲 Community lesson sharing

### Future (v0.3.0+)
- 🔲 Deep learning lessons (Keras, PyTorch)
- 🔲 Advanced ML topics (NLP, Computer Vision)
- 🔲 Time series forecasting module
- 🔲 MLOps and deployment lessons
- 🔲 JupyterLab sidebar extension
- 🔲 Collaborative learning features
- 🔲 Certificate generation
- 🔲 Google Colab support

---

## 💡 Frequently Asked Questions

### Is DS-Tutor ready to use?
The **curriculum is 100% complete** with all 57 lessons written and ready to explore in the `/lessons/` directory. The **Jupyter extension** (magic commands, auto-validation, AI feedback) is currently in development. Target beta release: Q2 2025.

### Can I use the lessons now?
**Yes!** All lesson content is available in YAML format in the repository. You can read through lessons, copy examples, and work through exercises manually. The interactive Jupyter extension is coming soon.

### How can I contribute?
- Review lessons and provide feedback on content quality
- Report typos or suggest improvements via GitHub issues
- Help build the Jupyter extension (see `/src/` for platform code)
- Share the project with others interested in Data Science education

### When will this be on PyPI?
We plan to publish `ds-tutor` to PyPI once the Jupyter extension reaches beta quality (Q2 2025 target). For now, install from source to explore the curriculum.

### Does this work in Google Colab?
Not yet, but Colab support is planned for v0.2.0 after the initial Jupyter release.

### How long does it take to complete the curriculum?
- **Python Fundamentals**: 5 hours
- **NumPy**: 6 hours
- **Pandas**: 9 hours
- **Matplotlib**: 6 hours
- **Scikit-Learn**: 7 hours
- **Total**: 50-70 hours at your own pace

### Is this suitable for complete beginners?
Yes! Start with Module 1 (Python Fundamentals). We assume no prior programming knowledge.

### Can I use the lessons in my own teaching?
Yes! All content is MIT licensed. Feel free to use, modify, and share the lessons for educational purposes. Attribution is appreciated but not required.

### What datasets are included?
All lessons use real datasets including:
- Classic ML datasets (iris, breast cancer, housing, california housing)
- Synthetic data for demonstrations
- Real-world examples (sales, time series, etc.)
- All datasets are loaded via sklearn or created programmatically

---

## 🙏 Acknowledgments

DS-Tutor is built on the shoulders of giants:

- **Anthropic** - Claude AI for intelligent feedback
- **Jupyter** - The amazing notebook environment
- **NumPy, Pandas, Matplotlib** - The foundations of Data Science
- **Scikit-learn** - Making ML accessible
- **IPyWidgets** - Interactive notebook interfaces

Special thanks to the open-source Data Science community for inspiration and best practices.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Documentation**: [Read the Docs](https://ds-tutor.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ds-tutor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ds-tutor/discussions)
- **Email**: support@dstutor.dev

---

## 🌟 Star Us!

If DS-Tutor helps you learn Data Science, please star the repo on GitHub! ⭐

Your support helps us continue developing free educational resources.

---

## 🚀 Get Started Now!

```bash
# Clone and install
git clone https://github.com/yourusername/ds-tutor.git
cd ds-tutor
pip install -e .

# Start Jupyter
jupyter notebook
```

Then in your notebook:
```python
%load_ext dstutor
%dstutor init
%dstutor start python
```

**Ready to become a Data Scientist? Start your journey today! 🎓📊🤖**

---

Made with ❤️ for Data Science learners everywhere
