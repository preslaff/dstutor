"""
Main IPython extension for DS-Tutor
"""

from IPython.core.magic import Magics, line_magic, magics_class
from IPython.display import display, HTML
from .tutor_engine import TutorEngine
from ..ui.widgets import TutorNavigationWidget, WelcomeWidget
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

            # Show welcome widget
            welcome = WelcomeWidget(self.tutor_engine)
            welcome.display()

            display(HTML(
                '<div style="color: #5cb85c; padding: 10px; border-left: 4px solid #5cb85c; margin-top: 10px;">'
                '✅ DS-Tutor initialized successfully!<br>'
                'Get started with <code>%dstutor topics</code> or <code>%dstutor start numpy</code>'
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
                from ..ui.widgets import FeedbackWidget
                feedback = FeedbackWidget()
                feedback.show_hint(hint, level)
            else:
                display(HTML('<div style="color: #f0ad4e;">⚠️ No hint available for current exercise</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_solution(self):
        """Show solution"""
        try:
            solution = self.tutor_engine.get_solution()
            if solution:
                from ..ui.widgets import FeedbackWidget
                feedback = FeedbackWidget()
                feedback.show_solution(solution)
            else:
                display(HTML('<div style="color: #f0ad4e;">⚠️ No solution available</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_progress(self):
        """Show progress dashboard"""
        try:
            from ..ui.widgets import ProgressDashboard
            dashboard = ProgressDashboard(self.tutor_engine.progress_tracker)
            dashboard.display()
        except Exception as e:
            display(HTML(f'<div style="color: #d9534f;">❌ Error: {str(e)}</div>'))

    def _cmd_topics(self):
        """List available topics"""
        try:
            topics = self.tutor_engine.get_topics()

            html = '<div style="padding: 15px; background: #f8f9fa; border-radius: 5px;">'
            html += '<h3 style="margin-top: 0;">📚 Available Topics</h3>'

            for level, level_topics in topics.items():
                html += f'<h4 style="color: #007bff; margin-top: 15px;">{level}</h4>'
                html += '<ul style="list-style: none; padding-left: 0;">'
                for topic in level_topics:
                    status = topic.get('status', 'locked')
                    icon = '✅' if status == 'completed' else '🔄' if status == 'in_progress' else '🔒' if status == 'locked' else '📖'
                    html += f'<li style="margin: 8px 0;"><strong>{icon} {topic["name"]}</strong> - {topic["description"]}</li>'
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
