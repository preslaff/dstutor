"""
Core orchestration engine for DS-Tutor
"""

from typing import Dict, Optional, List, Any
from pathlib import Path
from ..curriculum.lesson_loader import LessonLoader
from ..utils.progress_tracker import ProgressTracker
from ..ui.cell_injector import CellInjector
from .validator import CodeValidator
from ..llm.feedback_engine import FeedbackEngine
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip


class TutorEngine:
    """
    Main orchestrator for the DS-Tutor system

    Responsibilities:
    - Manage learning sessions
    - Load and display lessons
    - Coordinate validation and feedback
    - Track progress
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id

        # Initialize components
        self.lesson_loader = LessonLoader()
        self.progress_tracker = ProgressTracker(user_id)
        self.cell_injector = CellInjector()
        self.validator = CodeValidator()

        # Initialize LLM feedback engine (if API key available)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.feedback_engine = FeedbackEngine(api_key) if api_key else None

        # Session state
        self.current_topic = None
        self.current_lesson_id = None
        self.current_lesson = None
        self.current_exercise_id = None
        self.hints_used = 0

        # Configuration
        self.config = {
            'auto_validate': True,
            'hint_style': 'progressive',
            'feedback_verbosity': 'normal',
            'difficulty': 'medium',
        }

    def start_topic(self, topic: str) -> Dict[str, Any]:
        """
        Start learning a topic

        Args:
            topic: Topic name (e.g., 'numpy', 'pandas')

        Returns:
            dict with 'success' and 'message' keys
        """
        try:
            # Load first lesson of topic
            first_lesson = self.lesson_loader.get_first_lesson(topic)

            if not first_lesson:
                return {
                    'success': False,
                    'message': f'Topic "{topic}" not found or has no lessons'
                }

            self.current_topic = topic
            self.current_lesson_id = first_lesson['id']
            self.current_lesson = first_lesson
            self.hints_used = 0

            return {
                'success': True,
                'message': f'Started topic: {topic}',
                'lesson': first_lesson
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error starting topic: {str(e)}'
            }

    def next_lesson(self) -> Dict[str, Any]:
        """Move to the next lesson"""
        if not self.current_lesson_id:
            return {'success': False, 'message': 'No active lesson'}

        try:
            # Mark current lesson as completed
            if self.current_lesson_id:
                self.progress_tracker.mark_lesson_complete(self.current_lesson_id)

            # Get next lesson
            next_lesson = self.lesson_loader.get_next_lesson(
                self.current_topic,
                self.current_lesson_id
            )

            if not next_lesson:
                return {
                    'success': False,
                    'message': 'No more lessons in this topic. Great job! 🎉'
                }

            self.current_lesson_id = next_lesson['id']
            self.current_lesson = next_lesson
            self.hints_used = 0

            return {
                'success': True,
                'message': 'Loaded next lesson',
                'lesson': next_lesson
            }

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def previous_lesson(self) -> Dict[str, Any]:
        """Move to the previous lesson"""
        if not self.current_lesson_id:
            return {'success': False, 'message': 'No active lesson'}

        try:
            prev_lesson = self.lesson_loader.get_previous_lesson(
                self.current_topic,
                self.current_lesson_id
            )

            if not prev_lesson:
                return {
                    'success': False,
                    'message': 'This is the first lesson'
                }

            self.current_lesson_id = prev_lesson['id']
            self.current_lesson = prev_lesson
            self.hints_used = 0

            return {
                'success': True,
                'message': 'Loaded previous lesson',
                'lesson': prev_lesson
            }

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def goto_lesson(self, lesson_id: str) -> Dict[str, Any]:
        """Jump to a specific lesson"""
        try:
            lesson = self.lesson_loader.get_lesson_by_id(lesson_id)

            if not lesson:
                return {'success': False, 'message': f'Lesson "{lesson_id}" not found'}

            self.current_topic = lesson.get('topic', self.current_topic)
            self.current_lesson_id = lesson_id
            self.current_lesson = lesson
            self.hints_used = 0

            return {
                'success': True,
                'message': f'Jumped to lesson: {lesson_id}',
                'lesson': lesson
            }

        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def display_current_lesson(self):
        """Display the current lesson in the notebook"""
        if not self.current_lesson:
            return

        from IPython.display import display, HTML

        lesson = self.current_lesson
        topic = self.current_topic or "Unknown"

        # Display lesson header
        all_lessons = self.lesson_loader.get_topic_lessons(topic)
        current_index = next((i for i, l in enumerate(all_lessons) if l['id'] == lesson['id']), 0)
        total_lessons = len(all_lessons)
        progress_pct = ((current_index + 1) / total_lessons * 100) if total_lessons > 0 else 0

        header_html = f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; border-radius: 10px; margin: 15px 0; box-shadow: 0 3px 5px rgba(0,0,0,0.1);">
            <h2 style="margin: 0 0 8px 0;">📚 {topic.title()} - {lesson.get('subtopic', 'Lesson')}</h2>
            <p style="margin: 5px 0; opacity: 0.9; font-size: 1.1em;">
                Lesson {current_index + 1} of {total_lessons} •
                Level: {lesson.get('level', 'beginner').title()} •
                Duration: {lesson.get('metadata', {}).get('duration', '15 min')}
            </p>
            <div style="background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; margin-top: 12px; overflow: hidden;">
                <div style="background: white; height: 100%; width: {progress_pct}%; border-radius: 4px;"></div>
            </div>
        </div>
        """
        display(HTML(header_html))

        # Use cell injector to add lesson content
        self.cell_injector.inject_lesson(self.current_lesson, tutor_engine=self)

        # Display navigation instructions (no widgets)
        nav_html = """
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px; margin: 20px 0; border: 2px solid #dee2e6;">
            <h3 style="margin: 0 0 10px 0; color: #495057;">📌 Navigation Commands</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-family: monospace;">
                <div style="padding: 8px; background: white; border-radius: 4px;">
                    <code>%dstutor next</code> → Next lesson
                </div>
                <div style="padding: 8px; background: white; border-radius: 4px;">
                    <code>%dstutor previous</code> → Previous lesson
                </div>
                <div style="padding: 8px; background: white; border-radius: 4px;">
                    <code>%dstutor hint</code> → Get a hint
                </div>
                <div style="padding: 8px; background: white; border-radius: 4px;">
                    <code>%dstutor solution</code> → Show solution
                </div>
            </div>
        </div>
        """
        display(HTML(nav_html))

    def validate_exercise(self, user_code: str, exercise_id: str = None) -> Dict[str, Any]:
        """
        Validate user's exercise solution

        Args:
            user_code: The code submitted by the user
            exercise_id: Optional exercise ID (uses current if not provided)

        Returns:
            dict with validation results
        """
        if not self.current_lesson:
            return {'success': False, 'message': 'No active lesson'}

        exercise = self.current_lesson.get('exercise')
        if not exercise:
            return {'success': False, 'message': 'Current lesson has no exercise'}

        try:
            # Validate the code
            is_correct, feedback = self.validator.validate(
                user_code,
                exercise.get('solution'),
                exercise.get('validation', {})
            )

            # Record attempt
            self.progress_tracker.record_exercise_attempt(
                exercise_id or self.current_lesson['id'],
                user_code,
                is_correct,
                self.hints_used
            )

            # Generate AI feedback if available
            if self.feedback_engine and not is_correct:
                ai_feedback = self.feedback_engine.generate_feedback(
                    exercise_context=exercise,
                    user_code=user_code,
                    is_correct=is_correct,
                    error_message=feedback
                )
                feedback = ai_feedback

            return {
                'success': True,
                'is_correct': is_correct,
                'feedback': feedback
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Validation error: {str(e)}'
            }

    def get_hint(self, level: int = 1) -> Optional[str]:
        """
        Get a hint for the current exercise

        Args:
            level: Hint level (1-3, increasing specificity)

        Returns:
            Hint text or None
        """
        if not self.current_lesson:
            return None

        exercise = self.current_lesson.get('exercise')
        if not exercise:
            return None

        hints = exercise.get('hints', [])

        # Track hint usage
        self.hints_used = max(self.hints_used, level)

        # Return predefined hint if available
        for hint in hints:
            if hint.get('level') == level:
                return hint.get('text') or hint.get('code')

        # Generate AI hint if no predefined hint and LLM available
        if self.feedback_engine:
            return self.feedback_engine.generate_hint(
                exercise_context=exercise,
                user_code="",  # Could capture from notebook
                hint_level=level
            )

        return None

    def get_solution(self) -> Optional[str]:
        """Get the solution for the current exercise"""
        if not self.current_lesson:
            return None

        exercise = self.current_lesson.get('exercise')
        if not exercise:
            return None

        # Mark that solution was viewed
        self.hints_used = 999  # Special value indicating solution viewed

        return exercise.get('solution')

    def reset_current_lesson(self):
        """Reset the current lesson (clear progress)"""
        self.hints_used = 0
        # Could also clear exercise attempts from DB

    def get_topics(self) -> Dict[str, List[Dict]]:
        """
        Get all available topics organized by level

        Returns:
            dict mapping level names to lists of topics
        """
        return self.lesson_loader.get_all_topics()

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        config_copy = self.config.copy()
        config_copy['user_id'] = self.user_id
        config_copy['llm_enabled'] = self.feedback_engine is not None
        config_copy['current_topic'] = self.current_topic or 'None'
        config_copy['current_lesson'] = self.current_lesson_id or 'None'
        return config_copy

    def update_config(self, key: str, value: Any):
        """Update configuration"""
        if key in self.config:
            self.config[key] = value
