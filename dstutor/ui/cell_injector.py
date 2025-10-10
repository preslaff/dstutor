"""
Cell injection system for adding content to notebooks
"""

from IPython.display import display, Javascript, Markdown, Code
from typing import Dict, List, Any


class CellInjector:
    """Inject cells into the Jupyter notebook"""

    def inject_lesson(self, lesson: Dict[str, Any], tutor_engine=None):
        """
        Inject complete lesson structure into notebook

        Args:
            lesson: Lesson dictionary with content, examples, and exercises
            tutor_engine: Reference to TutorEngine for interactive widgets
        """
        content = lesson.get('content', {})

        # Inject lesson title and introduction
        if content.get('introduction'):
            self._inject_markdown(content['introduction'])

        # Inject concept explanation
        if content.get('concept'):
            self._inject_markdown(content['concept'])

        # Inject examples
        examples = content.get('examples', [])
        for example in examples:
            if example.get('title'):
                self._inject_markdown(f"### 💡 Example: {example['title']}")

            if example.get('code'):
                self._inject_code(example['code'], auto_run=False)

            if example.get('output'):
                self._inject_markdown(f"**Expected Output:**\n```\n{example['output']}\n```")

        # Inject exercise using simple HTML/Markdown approach (no widgets)
        exercise = lesson.get('exercise')
        if exercise:
            self._inject_exercise_simple(exercise, tutor_engine)

    def _inject_markdown(self, content: str):
        """Inject a markdown cell"""
        display(Markdown(content))

    def _inject_code(self, code: str, auto_run: bool = False):
        """
        Inject a code cell

        Args:
            code: Code content
            auto_run: Whether to auto-execute the cell
        """
        # For now, display as code block
        # Full cell injection requires JavaScript
        display(Markdown(f"```python\n{code}\n```"))

        if auto_run:
            # Would execute code here
            pass

    def _inject_exercise_simple(self, exercise: Dict[str, Any], tutor_engine):
        """
        Inject exercise using simple HTML/Markdown (no widgets)

        Args:
            exercise: Exercise dictionary
            tutor_engine: Reference to TutorEngine for validation
        """
        from IPython.display import HTML, Code

        instruction = exercise.get('instruction', 'Complete the exercise')
        setup_code = exercise.get('setup_code', '')
        starter_code = exercise.get('starter_code', '# Your code here\n')

        # Exercise header with instruction
        header_html = f"""
        <div style="padding: 20px; background: #fff3cd; border-left: 5px solid #ffc107;
                    margin: 20px 0; border-radius: 5px;">
            <h2 style="margin: 0 0 15px 0; color: #856404;">✏️ Exercise</h2>
            <div style="color: #856404; line-height: 1.8; white-space: pre-wrap;">{instruction}</div>
        </div>
        """
        display(HTML(header_html))

        # Setup code if present
        if setup_code.strip():
            setup_html = """
            <div style="margin: 15px 0 8px 0; font-weight: bold;">
                📋 Setup Code (Copy and run this first):
            </div>
            """
            display(HTML(setup_html))

            # Display setup code in a code block
            display(Code(setup_code, language='python'))

        # Starter code
        starter_html = """
        <div style="margin: 20px 0 8px 0; font-weight: bold;">
            ✍️ Your Solution (Copy the starter code below):
        </div>
        """
        display(HTML(starter_html))

        # Display starter code
        display(Code(starter_code, language='python'))

        # Instructions for user
        instructions_html = f"""
        <div style="padding: 15px; background: #e7f3ff; border-left: 4px solid #2196f3;
                    margin: 15px 0; border-radius: 5px;">
            <h4 style="margin: 0 0 10px 0; color: #1565c0;">📝 How to Complete This Exercise:</h4>
            <ol style="margin: 5px 0; padding-left: 20px; color: #1565c0;">
                <li>Create a new code cell below (Click "+ Code" or press B)</li>
                <li>Copy the starter code above into your cell</li>
                <li>Complete the exercise</li>
                <li>Run your code to test it</li>
                <li>Use <code>%dstutor check</code> to validate your solution ✅</li>
                <li>Use <code>%dstutor hint</code> if you need help</li>
                <li>Use <code>%dstutor solution</code> to see the answer</li>
                <li>Use <code>%dstutor next</code> when ready to continue</li>
            </ol>
        </div>
        """
        display(HTML(instructions_html))

    def _inject_exercise(self, exercise: Dict[str, Any], lesson_id: str):
        """
        Inject exercise cell with instructions (fallback method)

        Args:
            exercise: Exercise dictionary
            lesson_id: Current lesson ID
        """
        instruction = exercise.get('instruction', '')
        setup_code = exercise.get('setup_code', '')
        starter_code = exercise.get('starter_code', '# Your code here\n')

        # Inject exercise header
        exercise_md = f"""
---

## ✏️ Exercise

{instruction}
"""
        self._inject_markdown(exercise_md)

        # Setup code - inject as actual code cell if present
        if setup_code:
            self._inject_markdown("**Setup Code** (Run this first):")
            self.inject_code_cell(setup_code)

        # Inject starter code as actual editable code cell
        self._inject_markdown("**Your Solution:**")
        self.inject_code_cell(starter_code)

        # Inject tip
        self._inject_markdown("💡 **Tip:** Use `%dstutor hint` if you need help!")

    def inject_markdown_cell(self, content: str):
        """
        Inject a new markdown cell using JavaScript

        Args:
            content: Markdown content
        """
        # Escape content for JavaScript - escape newlines and special chars
        escaped_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n').replace('\r', '')

        js_code = f"""
        // Try JupyterLab API first, then fall back to classic Notebook
        if (typeof window.jupyterapp !== 'undefined') {{
            // JupyterLab
            window.jupyterapp.commands.execute('notebook:insert-cell-below').then(() => {{
                const notebook = window.jupyterapp.shell.currentWidget.content;
                window.jupyterapp.commands.execute('notebook:change-cell-to-markdown');
                const cell = notebook.activeCell;
                if (cell) {{
                    cell.model.value.text = `{escaped_content}`;
                }}
            }});
        }} else if (typeof Jupyter !== 'undefined' && Jupyter.notebook) {{
            // Classic Notebook
            var cell = Jupyter.notebook.insert_cell_below('markdown');
            cell.set_text(`{escaped_content}`);
            cell.render();
            Jupyter.notebook.select_next();
        }} else {{
            console.error('Unable to insert cell: Neither JupyterLab nor Classic Notebook API detected');
        }}
        """

        display(Javascript(js_code))

    def inject_code_cell(self, code: str):
        """
        Inject a new code cell using JavaScript

        Args:
            code: Python code content
        """
        # Escape content for JavaScript - escape newlines and special chars
        escaped_code = code.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n').replace('\r', '')

        js_code = f"""
        // Try JupyterLab API first, then fall back to classic Notebook
        if (typeof window.jupyterapp !== 'undefined') {{
            // JupyterLab
            window.jupyterapp.commands.execute('notebook:insert-cell-below').then(() => {{
                const notebook = window.jupyterapp.shell.currentWidget.content;
                const cell = notebook.activeCell;
                if (cell) {{
                    cell.model.value.text = `{escaped_code}`;
                }}
            }});
        }} else if (typeof Jupyter !== 'undefined' && Jupyter.notebook) {{
            // Classic Notebook
            var cell = Jupyter.notebook.insert_cell_below('code');
            cell.set_text(`{escaped_code}`);
            Jupyter.notebook.select_next();
        }} else {{
            console.error('Unable to insert cell: Neither JupyterLab nor Classic Notebook API detected');
        }}
        """

        display(Javascript(js_code))

    def inject_lesson_cells(self, lesson: Dict[str, Any]):
        """
        Inject complete lesson as actual notebook cells (advanced)

        This creates real notebook cells using JavaScript
        """
        content = lesson.get('content', {})

        # Title cell
        if content.get('introduction'):
            self.inject_markdown_cell(content['introduction'])

        # Concept cell
        if content.get('concept'):
            self.inject_markdown_cell(content['concept'])

        # Example cells
        for example in content.get('examples', []):
            if example.get('title'):
                self.inject_markdown_cell(f"### 💡 {example['title']}")

            if example.get('code'):
                self.inject_code_cell(example['code'])

        # Exercise cells
        exercise = lesson.get('exercise')
        if exercise:
            self.inject_markdown_cell(f"## ✏️ Exercise\n\n{exercise.get('instruction', '')}")

            if exercise.get('setup_code'):
                self.inject_code_cell(exercise['setup_code'])

            if exercise.get('starter_code'):
                self.inject_code_cell(exercise['starter_code'])
