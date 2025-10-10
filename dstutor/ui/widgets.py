"""
Interactive widgets for DS-Tutor UI
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output, Markdown
from typing import Dict, Any, Optional


class WelcomeWidget:
    """Welcome screen widget"""

    def __init__(self, tutor_engine):
        self.engine = tutor_engine

    def display(self):
        """Display welcome widget"""
        html = """
        <div style="padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="margin: 0 0 15px 0; font-size: 2.5em;">🎓 Welcome to DS-Tutor!</h1>
            <p style="font-size: 1.2em; margin: 10px 0;">
                AI-Powered Data Science Learning in Jupyter Notebooks
            </p>
            <hr style="border: none; border-top: 2px solid rgba(255,255,255,0.3); margin: 20px 0;">
            <div style="font-size: 1.1em;">
                <p><strong>📚 Learn:</strong> NumPy, Pandas, Matplotlib, Scikit-learn, and more</p>
                <p><strong>🤖 AI Guidance:</strong> Get intelligent hints and personalized feedback</p>
                <p><strong>✨ Interactive:</strong> Code, learn, and get instant validation</p>
            </div>
            <div style="margin-top: 25px; padding: 15px; background: rgba(255,255,255,0.1);
                        border-radius: 8px; text-align: left;">
                <p style="margin: 0; font-size: 1.1em;"><strong>Get Started:</strong></p>
                <code style="background: rgba(255,255,255,0.95); color: #2c3e50; padding: 8px 12px;
                           border-radius: 5px; display: inline-block; margin-top: 10px;
                           font-family: monospace; font-weight: 500;">%dstutor topics</code>
                <span style="margin: 0 10px;">or</span>
                <code style="background: rgba(255,255,255,0.95); color: #2c3e50; padding: 8px 12px;
                           border-radius: 5px; display: inline-block;
                           font-family: monospace; font-weight: 500;">%dstutor start numpy</code>
            </div>
        </div>
        """
        display(HTML(html))


class TutorNavigationWidget:
    """Main navigation and control widget"""

    def __init__(self, tutor_engine):
        self.engine = tutor_engine
        self.output = widgets.Output()

    def display(self):
        """Display navigation widget"""
        if not self.engine.current_lesson:
            return

        lesson = self.engine.current_lesson
        topic = self.engine.current_topic or "Unknown"

        # Progress calculation
        all_lessons = self.engine.lesson_loader.get_topic_lessons(topic)
        current_index = next((i for i, l in enumerate(all_lessons) if l['id'] == lesson['id']), 0)
        total_lessons = len(all_lessons)
        progress_pct = ((current_index + 1) / total_lessons * 100) if total_lessons > 0 else 0

        # Create header
        header_html = f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; border-radius: 10px; margin: 15px 0; box-shadow: 0 3px 5px rgba(0,0,0,0.1);">
            <h3 style="margin: 0 0 8px 0;">📚 {topic.title()} - {lesson.get('subtopic', 'Lesson')}</h3>
            <p style="margin: 5px 0; opacity: 0.9;">
                Lesson {current_index + 1} of {total_lessons} •
                Level: {lesson.get('level', 'beginner').title()} •
                Duration: {lesson.get('metadata', {}).get('duration', '15 min')}
            </p>
            <div style="background: rgba(255,255,255,0.2); height: 8px; border-radius: 4px; margin-top: 12px; overflow: hidden;">
                <div style="background: white; height: 100%; width: {progress_pct}%; border-radius: 4px; transition: width 0.3s;"></div>
            </div>
        </div>
        """
        display(HTML(header_html))

        # Create navigation buttons
        prev_button = widgets.Button(
            description='◄ Previous',
            button_style='info',
            tooltip='Go to previous lesson',
            layout=widgets.Layout(width='auto')
        )

        next_button = widgets.Button(
            description='Next ►',
            button_style='success',
            tooltip='Go to next lesson',
            layout=widgets.Layout(width='auto')
        )

        hint_button = widgets.Button(
            description='💡 Hint',
            button_style='warning',
            tooltip='Get a hint',
            layout=widgets.Layout(width='auto')
        )

        solution_button = widgets.Button(
            description='📝 Solution',
            button_style='danger',
            tooltip='Show solution',
            layout=widgets.Layout(width='auto')
        )

        # Button click handlers
        def on_prev_click(b):
            with self.output:
                clear_output()
                result = self.engine.previous_lesson()
                if result['success']:
                    self.engine.display_current_lesson()
                else:
                    print(result['message'])

        def on_next_click(b):
            with self.output:
                clear_output()
                result = self.engine.next_lesson()
                if result['success']:
                    self.engine.display_current_lesson()
                else:
                    print(result['message'])

        def on_hint_click(b):
            with self.output:
                clear_output()
                hint = self.engine.get_hint(self.engine.hints_used + 1)
                if hint:
                    feedback_widget = FeedbackWidget()
                    feedback_widget.show_hint(hint, self.engine.hints_used)

        def on_solution_click(b):
            with self.output:
                clear_output()
                solution = self.engine.get_solution()
                if solution:
                    feedback_widget = FeedbackWidget()
                    feedback_widget.show_solution(solution)

        prev_button.on_click(on_prev_click)
        next_button.on_click(on_next_click)
        hint_button.on_click(on_hint_click)
        solution_button.on_click(on_solution_click)

        # Layout buttons
        button_box = widgets.HBox(
            [prev_button, next_button, hint_button, solution_button],
            layout=widgets.Layout(
                justify_content='center',
                margin='10px 0'
            )
        )

        display(button_box)
        display(self.output)


class FeedbackWidget:
    """Display feedback, hints, and solutions"""

    def __init__(self):
        self.output = widgets.Output()

    def show_feedback(self, is_correct: bool, message: str):
        """Show validation feedback"""
        if is_correct:
            html = f"""
            <div style="padding: 20px; background: #d4edda; border: 2px solid #28a745; border-radius: 8px; margin: 15px 0;">
                <h3 style="color: #155724; margin: 0 0 10px 0;">✅ Correct! Well Done!</h3>
                <p style="color: #155724; margin: 0;">{message}</p>
            </div>
            """
        else:
            html = f"""
            <div style="padding: 20px; background: #f8d7da; border: 2px solid #dc3545; border-radius: 8px; margin: 15px 0;">
                <h3 style="color: #721c24; margin: 0 0 10px 0;">⚠️ Not Quite Right</h3>
                <p style="color: #721c24; margin: 0;">{message}</p>
                <p style="color: #721c24; margin: 10px 0 0 0; font-style: italic;">
                    💡 Try again or use <code>%dstutor hint</code> for help
                </p>
            </div>
            """

        display(HTML(html))

    def show_hint(self, hint_text: str, level: int):
        """Show a hint"""
        stars = '⭐' * level
        remaining = 3 - level

        html = f"""
        <div style="padding: 20px; background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #856404; margin: 0 0 10px 0;">💡 Hint (Level {level}/3) {stars}</h3>
            <p style="color: #856404; margin: 0; line-height: 1.6;">{hint_text}</p>
            <p style="color: #856404; margin: 15px 0 0 0; font-size: 0.9em;">
                {remaining} more hint{'s' if remaining != 1 else ''} available - use <code>%dstutor hint {level + 1}</code>
            </p>
        </div>
        """

        display(HTML(html))

    def show_solution(self, solution: str):
        """Show the solution"""
        html = f"""
        <div style="padding: 20px; background: #d1ecf1; border: 2px solid #17a2b8; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #0c5460; margin: 0 0 15px 0;">📝 Solution</h3>
            <pre style="background: #fff; padding: 15px; border-radius: 5px; overflow-x: auto; color: #0c5460;"><code>{solution}</code></pre>
            <p style="color: #0c5460; margin: 15px 0 0 0; font-style: italic;">
                Study the solution and try to understand the approach.
                You can continue to the next lesson when ready!
            </p>
        </div>
        """

        display(HTML(html))


class ExerciseWidget:
    """Interactive exercise widget with code editor"""

    def __init__(self, exercise: Dict[str, Any], tutor_engine):
        self.exercise = exercise
        self.engine = tutor_engine
        self.output = widgets.Output()

    def display(self):
        """Display exercise with code editor"""
        instruction = self.exercise.get('instruction', 'Complete the exercise')
        setup_code = self.exercise.get('setup_code', '')
        starter_code = self.exercise.get('starter_code', '# Your code here\n')

        # Exercise header
        header_html = """
        <div style="padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; margin: 15px 0 5px 0;">
            <h3 style="margin: 0; color: #856404;">✏️ Exercise</h3>
        </div>
        """
        display(HTML(header_html))

        # Display instruction as markdown (to preserve formatting)
        instruction_md = f"""
<div style="padding: 0 15px 15px 15px; background: #fff3cd; margin: 0 0 15px 0;">

{instruction}

</div>
"""
        display(Markdown(instruction_md))

        # Setup code (if exists)
        if setup_code.strip():
            setup_html = """
            <div style="margin: 10px 0;">
                <strong>Setup Code (Run this first):</strong>
            </div>
            """
            display(HTML(setup_html))

            setup_area = widgets.Textarea(
                value=setup_code,
                layout=widgets.Layout(width='100%', height='100px'),
                style={'font_family': 'monospace'}
            )
            setup_area.disabled = False  # Allow running setup
            display(setup_area)

            run_setup_btn = widgets.Button(
                description='▶ Run Setup',
                button_style='info',
                layout=widgets.Layout(width='150px', margin='5px 0 15px 0')
            )

            def run_setup(b):
                with self.output:
                    clear_output()
                    try:
                        exec(setup_area.value, globals())
                        print("✓ Setup code executed successfully!")
                    except Exception as e:
                        print(f"Error in setup: {e}")

            run_setup_btn.on_click(run_setup)
            display(run_setup_btn)

        # Solution code editor
        solution_html = """
        <div style="margin: 15px 0 5px 0;">
            <strong>Your Solution:</strong>
        </div>
        """
        display(HTML(solution_html))

        code_editor = widgets.Textarea(
            value=starter_code,
            placeholder='# Write your code here...',
            layout=widgets.Layout(width='100%', height='200px'),
            style={'font_family': 'monospace', 'font_size': '14px'}
        )
        display(code_editor)

        # Action buttons
        run_button = widgets.Button(
            description='▶ Run Code',
            button_style='success',
            layout=widgets.Layout(width='120px', margin='10px 5px 0 0')
        )

        check_button = widgets.Button(
            description='✓ Check Answer',
            button_style='primary',
            layout=widgets.Layout(width='140px', margin='10px 5px 0 0')
        )

        hint_button = widgets.Button(
            description='💡 Get Hint',
            button_style='warning',
            layout=widgets.Layout(width='120px', margin='10px 0 0 0')
        )

        # Button handlers
        def run_code(b):
            with self.output:
                clear_output()
                try:
                    exec(code_editor.value, globals())
                except Exception as e:
                    print(f"Error: {e}")

        def check_answer(b):
            with self.output:
                clear_output()
                result = self.engine.validate_exercise(code_editor.value)
                if result['success']:
                    feedback_widget = FeedbackWidget()
                    feedback_widget.show_feedback(result['is_correct'], result['feedback'])
                else:
                    print(f"Validation error: {result.get('message', 'Unknown error')}")

        def show_hint(b):
            with self.output:
                clear_output()
                hint = self.engine.get_hint(self.engine.hints_used + 1)
                if hint:
                    feedback_widget = FeedbackWidget()
                    feedback_widget.show_hint(hint, self.engine.hints_used)
                else:
                    print("No hints available for this exercise")

        run_button.on_click(run_code)
        check_button.on_click(check_answer)
        hint_button.on_click(show_hint)

        button_box = widgets.HBox([run_button, check_button, hint_button])
        display(button_box)

        # Output area
        display(self.output)

        # Tip
        tip_html = """
        <div style="margin: 15px 0; padding: 10px; background: #e7f3ff; border-left: 3px solid #2196f3;">
            <small>💡 <strong>Tip:</strong> Run your code first to test it, then check your answer when ready!</small>
        </div>
        """
        display(HTML(tip_html))


class ProgressDashboard:
    """Progress tracking dashboard"""

    def __init__(self, progress_tracker):
        self.tracker = progress_tracker

    def display(self):
        """Display progress dashboard"""
        stats = self.tracker.get_progress_stats()

        # Get topic-specific progress
        topics_progress = self._get_topics_progress()

        html = f"""
        <div style="padding: 25px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="margin: 0 0 20px 0; color: #333;">🎯 Your Progress</h2>

            <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="margin: 0 0 15px 0; color: #666;">📊 Overall Stats</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="padding: 15px; background: #e3f2fd; border-radius: 5px;">
                        <div style="font-size: 2em; font-weight: bold; color: #1976d2;">{stats['completed_lessons']}</div>
                        <div style="color: #666;">Lessons Completed</div>
                    </div>
                    <div style="padding: 15px; background: #e8f5e9; border-radius: 5px;">
                        <div style="font-size: 2em; font-weight: bold; color: #388e3c;">{stats['correct_exercises']}</div>
                        <div style="color: #666;">Exercises Solved</div>
                    </div>
                    <div style="padding: 15px; background: #fff3e0; border-radius: 5px;">
                        <div style="font-size: 2em; font-weight: bold; color: #f57c00;">{stats['accuracy']:.0%}</div>
                        <div style="color: #666;">Accuracy</div>
                    </div>
                </div>
            </div>

            <div style="background: white; padding: 20px; border-radius: 8px;">
                <h3 style="margin: 0 0 15px 0; color: #666;">📚 Topic Progress</h3>
                {topics_progress}
            </div>
        </div>
        """

        display(HTML(html))

    def _get_topics_progress(self) -> str:
        """Get HTML for topics progress bars"""
        # This would query actual progress
        # For now, showing example structure
        topics = [
            {'name': 'Python Fundamentals', 'progress': 100, 'status': 'completed'},
            {'name': 'NumPy Mastery', 'progress': 100, 'status': 'completed'},
            {'name': 'Pandas Deep Dive', 'progress': 65, 'status': 'in_progress'},
            {'name': 'Matplotlib & Seaborn', 'progress': 0, 'status': 'locked'},
        ]

        html = ""
        for topic in topics:
            status_icon = '✅' if topic['status'] == 'completed' else '🔄' if topic['status'] == 'in_progress' else '🔒'
            color = '#28a745' if topic['status'] == 'completed' else '#007bff' if topic['status'] == 'in_progress' else '#6c757d'

            html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-weight: 500;">{status_icon} {topic['name']}</span>
                    <span style="color: {color}; font-weight: bold;">{topic['progress']}%</span>
                </div>
                <div style="background: #e9ecef; height: 10px; border-radius: 5px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {topic['progress']}%;
                               border-radius: 5px; transition: width 0.3s;"></div>
                </div>
            </div>
            """

        return html
