"""
Lesson loading and management system
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import os


class LessonLoader:
    """Load and manage curriculum lessons"""

    def __init__(self, lessons_dir: Optional[Path] = None):
        """
        Initialize lesson loader

        Args:
            lessons_dir: Path to lessons directory (defaults to ../lessons)
        """
        if lessons_dir is None:
            # Get path relative to this file
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            lessons_dir = project_root / "lessons"

        self.lessons_dir = Path(lessons_dir)
        self._lesson_cache = {}
        self._topics_index = None

    def get_all_topics(self) -> Dict[str, List[Dict]]:
        """
        Get all available topics organized by level

        Returns:
            dict mapping level names to lists of topics
        """
        topics = {
            'Level 1: Foundations (Beginner)': [
                {
                    'name': 'Python Fundamentals',
                    'id': 'python',
                    'description': 'Review Python basics',
                    'status': 'available'
                },
                {
                    'name': 'NumPy Mastery',
                    'id': 'numpy',
                    'description': 'Array manipulation and operations',
                    'status': 'available'
                },
                {
                    'name': 'Pandas Deep Dive',
                    'id': 'pandas',
                    'description': 'Data manipulation with Pandas',
                    'status': 'available'
                },
                {
                    'name': 'Matplotlib & Seaborn',
                    'id': 'matplotlib',
                    'description': 'Data visualization',
                    'status': 'available'
                }
            ],
            'Level 2: Classical ML Pipeline (Intermediate)': [
                {
                    'name': 'Exploratory Data Analysis',
                    'id': 'eda',
                    'description': 'Understand and explore your data',
                    'status': 'locked'
                },
                {
                    'name': 'Data Preprocessing',
                    'id': 'preprocessing',
                    'description': 'Clean and prepare data for modeling',
                    'status': 'locked'
                },
                {
                    'name': 'Scikit-Learn Modeling',
                    'id': 'sklearn',
                    'description': 'Build machine learning models',
                    'status': 'locked'
                }
            ],
            'Level 3: Advanced Topics (Advanced)': [
                {
                    'name': 'Deep Learning with Keras',
                    'id': 'keras',
                    'description': 'Neural networks with Keras',
                    'status': 'locked'
                },
                {
                    'name': 'PyTorch Fundamentals',
                    'id': 'pytorch',
                    'description': 'Deep learning with PyTorch',
                    'status': 'locked'
                }
            ]
        }

        return topics

    def get_first_lesson(self, topic: str) -> Optional[Dict]:
        """
        Get the first lesson of a topic

        Args:
            topic: Topic name (e.g., 'numpy', 'pandas')

        Returns:
            Lesson dictionary or None
        """
        # Try to load from YAML files first
        lessons = self._load_topic_lessons_from_yaml(topic)
        if lessons:
            return lessons[0]

        # Fallback to sample lesson
        return self._get_sample_lesson(topic, 1)

    def get_next_lesson(self, topic: str, current_lesson_id: str) -> Optional[Dict]:
        """Get the next lesson in a topic"""
        lessons = self._load_topic_lessons_from_yaml(topic)
        if not lessons:
            # Fallback to sample lessons
            try:
                current_num = int(current_lesson_id.split('_')[-1])
                return self._get_sample_lesson(topic, current_num + 1)
            except (ValueError, IndexError):
                return None

        # Find current lesson and return next
        for i, lesson in enumerate(lessons):
            if lesson['id'] == current_lesson_id:
                if i + 1 < len(lessons):
                    return lessons[i + 1]
                return None
        return None

    def get_previous_lesson(self, topic: str, current_lesson_id: str) -> Optional[Dict]:
        """Get the previous lesson in a topic"""
        lessons = self._load_topic_lessons_from_yaml(topic)
        if not lessons:
            # Fallback to sample lessons
            try:
                current_num = int(current_lesson_id.split('_')[-1])
                if current_num > 1:
                    return self._get_sample_lesson(topic, current_num - 1)
                return None
            except (ValueError, IndexError):
                return None

        # Find current lesson and return previous
        for i, lesson in enumerate(lessons):
            if lesson['id'] == current_lesson_id:
                if i > 0:
                    return lessons[i - 1]
                return None
        return None

    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict]:
        """Load a lesson by its ID"""
        # Try all topics to find the lesson
        all_topics = ['python', 'numpy', 'pandas', 'matplotlib', 'sklearn', 'eda', 'preprocessing']

        for topic in all_topics:
            lessons = self._load_topic_lessons_from_yaml(topic)
            for lesson in lessons:
                if lesson['id'] == lesson_id:
                    return lesson

        # Fallback to sample lesson
        try:
            parts = lesson_id.rsplit('_', 1)
            topic = parts[0]
            lesson_num = int(parts[1])
            return self._get_sample_lesson(topic, lesson_num)
        except (ValueError, IndexError):
            return None

    def get_topic_lessons(self, topic: str) -> List[Dict]:
        """Get all lessons for a topic"""
        # Try to load from YAML files first
        lessons = self._load_topic_lessons_from_yaml(topic)
        if lessons:
            return lessons

        # Fallback to sample lessons
        sample_lessons = []
        for i in range(1, 6):  # 5 sample lessons
            lesson = self._get_sample_lesson(topic, i)
            if lesson:
                sample_lessons.append(lesson)
        return sample_lessons

    def _load_topic_lessons_from_yaml(self, topic: str) -> List[Dict]:
        """
        Load all lessons for a topic from YAML files

        Args:
            topic: Topic name (e.g., 'python', 'numpy', 'pandas')

        Returns:
            List of lesson dictionaries sorted by order
        """
        lessons = []

        # Map topic names to directory paths
        topic_dirs = {
            'python': self.lessons_dir / 'foundations' / 'python',
            'numpy': self.lessons_dir / 'foundations' / 'numpy',
            'pandas': self.lessons_dir / 'foundations' / 'pandas',
            'matplotlib': self.lessons_dir / 'foundations' / 'matplotlib',
            'sklearn': self.lessons_dir / 'intermediate' / 'sklearn',
            'eda': self.lessons_dir / 'intermediate' / 'eda',
            'preprocessing': self.lessons_dir / 'intermediate' / 'preprocessing',
        }

        topic_dir = topic_dirs.get(topic)
        if not topic_dir or not topic_dir.exists():
            return []

        # Load all YAML files in the topic directory
        yaml_files = sorted(topic_dir.glob('*.yaml'))

        for yaml_file in yaml_files:
            lesson = self.load_lesson_from_yaml(yaml_file)
            if lesson:
                lessons.append(lesson)

        # Sort by order field if present
        lessons.sort(key=lambda l: l.get('order', 999))

        return lessons

    def load_lesson_from_yaml(self, filepath: Path) -> Optional[Dict]:
        """
        Load a lesson from a YAML file

        Args:
            filepath: Path to YAML lesson file

        Returns:
            Lesson dictionary or None
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lesson_data = yaml.safe_load(f)
                return lesson_data.get('lesson')
        except Exception as e:
            print(f"Error loading lesson from {filepath}: {e}")
            return None

    def _get_sample_lesson(self, topic: str, lesson_num: int) -> Optional[Dict]:
        """
        Get a sample lesson for testing

        Args:
            topic: Topic name
            lesson_num: Lesson number

        Returns:
            Sample lesson dictionary
        """
        if lesson_num > 5:  # Only 5 sample lessons per topic
            return None

        lesson_id = f"{topic}_{lesson_num:02d}"

        # Sample lessons by topic
        if topic == "numpy":
            return self._get_numpy_sample_lesson(lesson_num)
        elif topic == "pandas":
            return self._get_pandas_sample_lesson(lesson_num)
        elif topic == "matplotlib":
            return self._get_matplotlib_sample_lesson(lesson_num)
        else:
            # Generic sample lesson
            return {
                'id': lesson_id,
                'level': 'beginner',
                'topic': topic,
                'subtopic': f'Lesson {lesson_num}',
                'order': lesson_num,
                'metadata': {
                    'duration': '15 min',
                    'difficulty': 'easy'
                },
                'content': {
                    'introduction': f'# {topic.title()} - Lesson {lesson_num}\n\nWelcome to this lesson!',
                    'concept': f'This is a sample lesson for {topic}.',
                    'examples': []
                },
                'exercise': {
                    'instruction': 'Complete the exercise below',
                    'setup_code': 'import numpy as np',
                    'starter_code': '# Your code here',
                    'solution': 'result = "sample"',
                    'validation': {
                        'type': 'value_check'
                    },
                    'hints': [
                        {'level': 1, 'text': 'This is a sample hint'}
                    ]
                }
            }

    def _get_numpy_sample_lesson(self, lesson_num: int) -> Dict:
        """Get sample NumPy lesson"""
        lessons = {
            1: {
                'id': 'numpy_01',
                'level': 'beginner',
                'topic': 'numpy',
                'subtopic': 'Array Creation',
                'order': 1,
                'metadata': {'duration': '10 min', 'difficulty': 'easy'},
                'content': {
                    'introduction': '# NumPy Array Creation\n\nLearn how to create NumPy arrays - the foundation of numerical computing in Python.',
                    'concept': '''## What are NumPy Arrays?

NumPy arrays are powerful n-dimensional array objects that allow for efficient numerical operations.

**Key Benefits:**
- Fast vectorized operations
- Memory efficient
- Mathematical operations are intuitive
- Foundation for pandas, scikit-learn, and more''',
                    'examples': [
                        {
                            'title': 'Creating Arrays from Lists',
                            'code': '''import numpy as np

# 1D array
arr1d = np.array([1, 2, 3, 4, 5])
print(arr1d)
print(f"Shape: {arr1d.shape}, Dtype: {arr1d.dtype}")

# 2D array
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2d)
print(f"Shape: {arr2d.shape}")''',
                            'output': '''[1 2 3 4 5]
Shape: (5,), Dtype: int64
[[1 2 3]
 [4 5 6]]
Shape: (2, 3)'''
                        }
                    ]
                },
                'exercise': {
                    'instruction': 'Create a 1D NumPy array containing the numbers 10, 20, 30, 40, 50 and store it in a variable called `result`.',
                    'setup_code': 'import numpy as np',
                    'starter_code': '# Your code here\nresult = ',
                    'solution': 'result = np.array([10, 20, 30, 40, 50])',
                    'validation': {
                        'type': 'array_check',
                        'checks': [
                            {'type': 'shape', 'expected': [5]},
                            {'type': 'values', 'expected': [10, 20, 30, 40, 50]}
                        ]
                    },
                    'hints': [
                        {'level': 1, 'text': 'Use the np.array() function with a list of numbers.'},
                        {'level': 2, 'text': 'The syntax is: np.array([10, 20, 30, 40, 50])'},
                        {'level': 3, 'text': 'result = np.array([10, 20, 30, 40, 50])'}
                    ]
                }
            },
            2: {
                'id': 'numpy_02',
                'level': 'beginner',
                'topic': 'numpy',
                'subtopic': 'Array Functions',
                'order': 2,
                'metadata': {'duration': '15 min', 'difficulty': 'easy'},
                'content': {
                    'introduction': '# NumPy Array Creation Functions\n\nLearn efficient ways to create arrays using NumPy functions.',
                    'concept': '''## Array Creation Functions

NumPy provides many functions for creating arrays:

- `np.zeros()` - Array filled with zeros
- `np.ones()` - Array filled with ones
- `np.arange()` - Array with evenly spaced values
- `np.linspace()` - Array with specified number of values
- `np.eye()` - Identity matrix''',
                    'examples': [
                        {
                            'title': 'Using Creation Functions',
                            'code': '''import numpy as np

# Array of zeros
zeros = np.zeros((3, 4))
print("Zeros:")
print(zeros)

# Array of ones
ones = np.ones((2, 3))
print("\\nOnes:")
print(ones)

# Range of values
range_arr = np.arange(0, 10, 2)
print("\\nRange:", range_arr)''',
                            'output': 'Arrays with specified values'
                        }
                    ]
                },
                'exercise': {
                    'instruction': 'Create a 2D array filled with zeros, with shape (3, 5). Store it in a variable called `result`.',
                    'setup_code': 'import numpy as np',
                    'starter_code': '# Your code here\nresult = ',
                    'solution': 'result = np.zeros((3, 5))',
                    'validation': {
                        'type': 'array_check',
                        'checks': [
                            {'type': 'shape', 'expected': [3, 5]},
                        ]
                    },
                    'hints': [
                        {'level': 1, 'text': 'Use np.zeros() with a tuple for the shape.'},
                        {'level': 2, 'text': 'Pass the shape as (3, 5) to np.zeros()'},
                        {'level': 3, 'text': 'result = np.zeros((3, 5))'}
                    ]
                }
            }
        }

        return lessons.get(lesson_num)

    def _get_pandas_sample_lesson(self, lesson_num: int) -> Optional[Dict]:
        """Get sample Pandas lesson"""
        # Similar structure for Pandas lessons
        return {
            'id': f'pandas_{lesson_num:02d}',
            'level': 'beginner',
            'topic': 'pandas',
            'subtopic': f'Pandas Lesson {lesson_num}',
            'order': lesson_num,
            'metadata': {'duration': '15 min', 'difficulty': 'easy'},
            'content': {
                'introduction': f'# Pandas - Lesson {lesson_num}\n\nLearn Pandas data manipulation.',
                'concept': 'Pandas concepts here...',
                'examples': []
            },
            'exercise': {
                'instruction': 'Complete the Pandas exercise',
                'setup_code': 'import pandas as pd',
                'starter_code': '# Your code here',
                'solution': 'result = pd.DataFrame()',
                'validation': {'type': 'dataframe_check', 'checks': []},
                'hints': [{'level': 1, 'text': 'Pandas hint'}]
            }
        }

    def _get_matplotlib_sample_lesson(self, lesson_num: int) -> Optional[Dict]:
        """Get sample Matplotlib lesson"""
        return {
            'id': f'matplotlib_{lesson_num:02d}',
            'level': 'beginner',
            'topic': 'matplotlib',
            'subtopic': f'Visualization Lesson {lesson_num}',
            'order': lesson_num,
            'metadata': {'duration': '20 min', 'difficulty': 'easy'},
            'content': {
                'introduction': f'# Matplotlib - Lesson {lesson_num}\n\nLearn data visualization.',
                'concept': 'Matplotlib concepts here...',
                'examples': []
            },
            'exercise': {
                'instruction': 'Create a visualization',
                'setup_code': 'import matplotlib.pyplot as plt\\nimport numpy as np',
                'starter_code': '# Your code here',
                'solution': 'plt.plot([1,2,3])',
                'validation': {'type': 'type_check', 'expected_type': 'list'},
                'hints': [{'level': 1, 'text': 'Matplotlib hint'}]
            }
        }
