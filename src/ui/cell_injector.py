"""
Cell injection system for adding content to notebooks
"""

from IPython.display import display, Javascript, Markdown, Code
from typing import Dict, List, Any


class CellInjector:
    """Inject cells into the Jupyter notebook"""

    def inject_lesson(self, lesson: Dict[str, Any]):
        """
        Inject complete lesson structure into notebook

        Args:
            lesson: Lesson dictionary with content, examples, and exercises
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

        # Inject exercise
        exercise = lesson.get('exercise')
        if exercise:
            self._inject_exercise(exercise, lesson['id'])

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

    def _inject_exercise(self, exercise: Dict[str, Any], lesson_id: str):
        """
        Inject exercise cell with instructions

        Args:
            exercise: Exercise dictionary
            lesson_id: Current lesson ID
        """
        instruction = exercise.get('instruction', '')
        setup_code = exercise.get('setup_code', '')
        starter_code = exercise.get('starter_code', '')

        # Inject exercise header
        exercise_md = f"""
---

## ✏️ Exercise

{instruction}

**Setup Code** (Run this first):
"""
        self._inject_markdown(exercise_md)

        # Setup code
        if setup_code:
            display(Markdown(f"```python\n{setup_code}\n```"))

        # Starter code prompt
        starter_md = f"""
**Your Solution:**

{f'```python\\n{starter_code}\\n```' if starter_code else '*Write your code here*'}

---
💡 **Tip:** Use `%dstutor hint` if you need help!
"""
        self._inject_markdown(starter_md)

    def inject_markdown_cell(self, content: str):
        """
        Inject a new markdown cell using JavaScript

        Args:
            content: Markdown content
        """
        # Escape content for JavaScript
        escaped_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

        js_code = f"""
        var cell = Jupyter.notebook.insert_cell_below('markdown');
        cell.set_text(`{escaped_content}`);
        cell.render();
        Jupyter.notebook.select_next();
        """

        display(Javascript(js_code))

    def inject_code_cell(self, code: str):
        """
        Inject a new code cell using JavaScript

        Args:
            code: Python code content
        """
        # Escape content for JavaScript
        escaped_code = code.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

        js_code = f"""
        var cell = Jupyter.notebook.insert_cell_below('code');
        cell.set_text(`{escaped_code}`);
        Jupyter.notebook.select_next();
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
