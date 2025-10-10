"""
Main IPython extension for DS-Tutor
"""

from IPython.core.magic import Magics, line_magic, magics_class
from IPython.display import display, HTML
from .tutor_engine import TutorEngine
import sys


@magics_class
class DSTutorMagics(Magics):
    """Magic commands for DS-Tutor"""

    def __init__(self, shell):
        super().__init__(shell)
        self.tutor_engine = None
        self.current_session = None
        self._initialized = False

    @line_magic
    def dstutor(self, line):
        """
        Main magic command for DS-Tutor

        Usage:
            %dstutor init                 - Initialize the tutor
            %dstutor start <topic>        - Start learning a topic
            %dstutor check                - Check your solution
            %dstutor next                 - Go to next lesson
            %dstutor previous             - Go to previous lesson
            %dstutor hint [level]         - Get a hint
            %dstutor solution             - Show solution
            %dstutor progress             - Show progress dashboard
            %dstutor topics               - List available topics
            %dstutor reset                - Reset current lesson
            %dstutor goto <lesson_id>     - Jump to specific lesson
            %dstutor config               - Show configuration
        """
        args = line.strip().split()

        if not args:
            self._show_help()
            return

        command = args[0].lower()

        # Initialize command doesn't require engine to be initialized
        if command == "init":
            self._cmd_init()
            return

        # All other commands require initialization
        if not self._initialized:
            display(HTML(
                '<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">'
                '⚠️ DS-Tutor not initialized. Run <code>%dstutor init</code> first.'
                '</div>'
            ))
            return

        # Route commands
        if command == "start":
            if len(args) < 2:
                display(HTML('<div style="color: #d9534f;">❌ Please specify a topic: %dstutor start <topic></div>'))
                return
            self._cmd_start(args[1])

        elif command == "next":
            self._cmd_next()

        elif command == "previous" or command == "prev":
            self._cmd_previous()

        elif command == "hint":
            level = int(args[1]) if len(args) > 1 else 1
            self._cmd_hint(level)

        elif command == "solution":
            self._cmd_solution()

        elif command == "progress":
            self._cmd_progress()

        elif command == "topics":
            self._cmd_topics()

        elif command == "reset":
            self._cmd_reset()

        elif command == "goto":
            if len(args) < 2:
                display(HTML('<div style="color: #d9534f;">❌ Please specify lesson ID: %dstutor goto <lesson_id></div>'))
                return
            self._cmd_goto(args[1])

        elif command == "check" or command == "validate":
            self._cmd_check()

        elif command == "config":
            self._cmd_config()

        elif command == "help":
            self._show_help()

        else:
            display(HTML(f'<div style="color: #d9534f;">❌ Unknown command: {command}</div>'))
            self._show_help()

    def _cmd_init(self):
        """Initialize DS-Tutor"""
        try:
            self.tutor_engine = TutorEngine()
            self._initialized = True

            # Show welcome message (pure HTML, no widgets)
            welcome_html = """
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
                               font-family: monospace; font-weight: 500;">%dstutor start python</code>
                </div>
            </div>
            """
            display(HTML(welcome_html))

            display(HTML(
                '<div style="color: #5cb85c; padding: 10px; border-left: 4px solid #5cb85c; margin-top: 10px;">'
                '✅ DS-Tutor initialized successfully!'
                '</div>'
            ))
        except Exception as e:
            display(HTML(
                f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">'
                f'❌ Initialization failed: {str(e)}'
                '</div>'
            ))

    def _cmd_start(self, topic):
        """Start learning a topic"""
        try:
            result = self.tutor_engine.start_topic(topic)
            if result['success']:
                # Inject lesson content into notebook
                self.tutor_engine.display_current_lesson()
            else:
                display(HTML(f'<div style="color: #d9534f;">❌ {result["message"]}</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_next(self):
        """Move to next lesson"""
        try:
            result = self.tutor_engine.next_lesson()
            if result['success']:
                self.tutor_engine.display_current_lesson()
            else:
                display(HTML(f'<div style="color: #f0ad4e;">⚠️ {result["message"]}</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_previous(self):
        """Move to previous lesson"""
        try:
            result = self.tutor_engine.previous_lesson()
            if result['success']:
                self.tutor_engine.display_current_lesson()
            else:
                display(HTML(f'<div style="color: #f0ad4e;">⚠️ {result["message"]}</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_hint(self, level):
        """Get a hint"""
        try:
            hint = self.tutor_engine.get_hint(level)
            if hint:
                stars = '⭐' * level
                remaining = 3 - level
                hint_html = f"""
                <div style="padding: 20px; background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; margin: 15px 0;">
                    <h3 style="color: #856404; margin: 0 0 10px 0;">💡 Hint (Level {level}/3) {stars}</h3>
                    <p style="color: #856404; margin: 0; line-height: 1.6; white-space: pre-wrap;">{hint}</p>
                    <p style="color: #856404; margin: 15px 0 0 0; font-size: 0.9em;">
                        {remaining} more hint{'s' if remaining != 1 else ''} available - use <code>%dstutor hint {level + 1}</code>
                    </p>
                </div>
                """
                display(HTML(hint_html))
            else:
                display(HTML('<div style="color: #f0ad4e; padding: 10px; border-left: 4px solid #f0ad4e;">⚠️ No hint available for current exercise</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_solution(self):
        """Show solution"""
        try:
            solution = self.tutor_engine.get_solution()
            if solution:
                from html import escape
                escaped_solution = escape(solution)
                solution_html = f"""
                <div style="padding: 20px; background: #d1ecf1; border: 2px solid #17a2b8; border-radius: 8px; margin: 15px 0;">
                    <h3 style="color: #0c5460; margin: 0 0 15px 0;">📝 Solution</h3>
                    <pre style="background: #fff; padding: 15px; border-radius: 5px; overflow-x: auto; color: #0c5460;"><code>{escaped_solution}</code></pre>
                    <p style="color: #0c5460; margin: 15px 0 0 0; font-style: italic;">
                        Study the solution and try to understand the approach.
                        You can continue to the next lesson when ready!
                    </p>
                </div>
                """
                display(HTML(solution_html))
            else:
                display(HTML('<div style="color: #f0ad4e; padding: 10px; border-left: 4px solid #f0ad4e;">⚠️ No solution available</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_progress(self):
        """Show progress dashboard"""
        try:
            stats = self.tutor_engine.progress_tracker.get_progress_stats()

            html = f"""
            <div style="padding: 25px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h2 style="margin: 0 0 20px 0; color: #333;">🎯 Your Progress</h2>

                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 15px 0; color: #666;">📊 Overall Stats</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div style="padding: 15px; background: #e3f2fd; border-radius: 5px;">
                            <div style="font-size: 2em; font-weight: bold; color: #1976d2;">{stats.get('completed_lessons', 0)}</div>
                            <div style="color: #666;">Lessons Completed</div>
                        </div>
                        <div style="padding: 15px; background: #e8f5e9; border-radius: 5px;">
                            <div style="font-size: 2em; font-weight: bold; color: #388e3c;">{stats.get('correct_exercises', 0)}</div>
                            <div style="color: #666;">Exercises Solved</div>
                        </div>
                        <div style="padding: 15px; background: #fff3e0; border-radius: 5px;">
                            <div style="font-size: 2em; font-weight: bold; color: #f57c00;">{stats.get('accuracy', 0):.0%}</div>
                            <div style="color: #666;">Accuracy</div>
                        </div>
                    </div>
                </div>

                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <p style="color: #666; margin: 0;">Keep up the great work! 🚀</p>
                </div>
            </div>
            """

            display(HTML(html))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_topics(self):
        """List available topics"""
        try:
            topics = self.tutor_engine.get_topics()

            html = '<div style="padding: 15px; background: #f8f9fa; border-radius: 5px;">'
            html += '<h3 style="margin-top: 0;">📚 Available Topics</h3>'

            for level, level_topics in topics.items():
                html += f'<h4 style="color: #007bff; margin-top: 15px;">{level}</h4>'

                # Add development note for advanced topics
                if 'Advanced' in level:
                    html += '<p style="color: #f0ad4e; font-style: italic; margin: 5px 0;">🚧 Currently in development - Coming soon!</p>'

                html += '<ul style="list-style: none; padding-left: 0;">'
                for topic in level_topics:
                    status = topic.get('status', 'locked')
                    topic_id = topic.get('id', '')
                    icon = '✅' if status == 'completed' else '🔄' if status == 'in_progress' else '🔒' if status == 'locked' else '📖'

                    # Create the topic line with command
                    html += f'<li style="margin: 8px 0;">'
                    html += f'<strong>{icon} {topic["name"]}</strong> - {topic["description"]}'

                    # Add command to start the topic
                    if 'Advanced' in level:
                        html += f' <span style="color: #999; font-style: italic;">(Coming soon)</span>'
                    else:
                        html += f' <code style="background: rgba(255,255,255,0.95); color: #2c3e50; padding: 2px 6px; border-radius: 3px; font-family: monospace; margin-left: 8px;">%dstutor start {topic_id}</code>'
                    html += '</li>'
                html += '</ul>'

            html += '</div>'
            display(HTML(html))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_reset(self):
        """Reset current lesson"""
        try:
            self.tutor_engine.reset_current_lesson()
            display(HTML('<div style="color: #5cb85c;">✅ Lesson reset successfully</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_goto(self, lesson_id):
        """Jump to specific lesson"""
        try:
            result = self.tutor_engine.goto_lesson(lesson_id)
            if result['success']:
                self.tutor_engine.display_current_lesson()
            else:
                display(HTML(f'<div style="color: #d9534f;">❌ {result["message"]}</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_check(self):
        """Check/validate the user's solution"""
        try:
            # Get the last executed code from IPython history
            hist = list(self.shell.history_manager.get_range(output=False))
            if not hist:
                display(HTML('<div style="color: #f0ad4e; padding: 10px; border-left: 4px solid #f0ad4e;">⚠️ No code history found. Write and run your solution first.</div>'))
                return

            # Get the most recent non-magic command
            last_code = None
            for session, line_num, code in reversed(hist):
                if not code.strip().startswith('%'):
                    last_code = code
                    break

            if not last_code:
                display(HTML('<div style="color: #f0ad4e; padding: 10px; border-left: 4px solid #f0ad4e;">⚠️ No code to check. Write and run your solution first.</div>'))
                return

            # Validate the code
            result = self.tutor_engine.validate_exercise(last_code)
            if result['success']:
                is_correct = result['is_correct']
                message = result['feedback']

                if is_correct:
                    feedback_html = f"""
                    <div style="padding: 20px; background: #d4edda; border: 2px solid #28a745; border-radius: 8px; margin: 15px 0;">
                        <h3 style="color: #155724; margin: 0 0 10px 0;">✅ Correct! Well Done!</h3>
                        <p style="color: #155724; margin: 0;">{message}</p>
                    </div>
                    """
                else:
                    feedback_html = f"""
                    <div style="padding: 20px; background: #f8d7da; border: 2px solid #dc3545; border-radius: 8px; margin: 15px 0;">
                        <h3 style="color: #721c24; margin: 0 0 10px 0;">⚠️ Not Quite Right</h3>
                        <p style="color: #721c24; margin: 0;">{message}</p>
                        <p style="color: #721c24; margin: 10px 0 0 0; font-style: italic;">
                            💡 Try again or use <code>%dstutor hint</code> for help
                        </p>
                    </div>
                    """
                display(HTML(feedback_html))
            else:
                display(HTML(f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">❌ {result.get("message", "Validation error")}</div>'))

        except Exception as e:
            display(HTML(f'<div style="color: #d9534f; padding: 10px; border-left: 4px solid #d9534f;">❌ Error checking solution: {str(e)}</div>'))

    def _cmd_config(self):
        """Show configuration"""
        try:
            config = self.tutor_engine.get_config()

            html = '<div style="padding: 15px; background: #f8f9fa; border-radius: 5px;">'
            html += '<h3 style="margin-top: 0;">⚙️ Configuration</h3>'
            html += '<table style="width: 100%; border-collapse: collapse;">'

            for key, value in config.items():
                html += f'<tr><td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>{key}:</strong></td>'
                html += f'<td style="padding: 8px; border-bottom: 1px solid #ddd;">{value}</td></tr>'

            html += '</table></div>'
            display(HTML(html))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _show_help(self):
        """Show help message"""
        help_html = """
        <div style="padding: 15px; background: #f8f9fa; border-radius: 5px; font-family: monospace;">
            <h3 style="margin-top: 0;">🎓 DS-Tutor Commands</h3>
            <table style="width: 100%;">
                <tr><td><code>%dstutor init</code></td><td>Initialize the tutor</td></tr>
                <tr><td><code>%dstutor start &lt;topic&gt;</code></td><td>Start learning a topic</td></tr>
                <tr><td><code>%dstutor check</code></td><td>Check your solution</td></tr>
                <tr><td><code>%dstutor next</code></td><td>Go to next lesson</td></tr>
                <tr><td><code>%dstutor previous</code></td><td>Go to previous lesson</td></tr>
                <tr><td><code>%dstutor hint [level]</code></td><td>Get a hint (levels 1-3)</td></tr>
                <tr><td><code>%dstutor solution</code></td><td>Show solution</td></tr>
                <tr><td><code>%dstutor progress</code></td><td>Show progress dashboard</td></tr>
                <tr><td><code>%dstutor topics</code></td><td>List available topics</td></tr>
                <tr><td><code>%dstutor reset</code></td><td>Reset current lesson</td></tr>
                <tr><td><code>%dstutor goto &lt;id&gt;</code></td><td>Jump to specific lesson</td></tr>
                <tr><td><code>%dstutor config</code></td><td>Show configuration</td></tr>
                <tr><td><code>%dstutor help</code></td><td>Show this help message</td></tr>
            </table>
        </div>
        """
        display(HTML(help_html))


def load_ipython_extension(ipython):
    """
    Load the IPython extension

    This function is called automatically when the extension is loaded with:
        %load_ext dstutor
    """
    ipython.register_magics(DSTutorMagics)

    # Display welcome message
    welcome_html = """
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; border-radius: 10px; margin: 10px 0;">
        <h2 style="margin: 0 0 10px 0;">🎓 DS-Tutor Extension Loaded!</h2>
        <p style="margin: 5px 0;">AI-Powered Data Science Learning in Jupyter</p>
        <p style="margin: 10px 0 0 0; font-size: 0.9em;">
            Get started with <code style="background: rgba(255,255,255,0.2); padding: 2px 6px;
            border-radius: 3px;">%dstutor init</code>
        </p>
    </div>
    """
    display(HTML(welcome_html))


def unload_ipython_extension(ipython):
    """Unload the IPython extension"""
    pass
