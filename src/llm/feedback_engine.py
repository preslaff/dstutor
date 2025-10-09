"""
LLM-powered feedback and hint generation using Claude API
"""

from typing import Dict, Optional
import os


class FeedbackEngine:
    """Generate AI-powered feedback and hints using Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize feedback engine

        Args:
            api_key: Anthropic API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                print("Warning: anthropic package not installed. Install with: pip install anthropic")
            except Exception as e:
                print(f"Warning: Could not initialize Claude client: {e}")

    def generate_hint(self,
                     exercise_context: Dict,
                     user_code: str,
                     hint_level: int) -> str:
        """
        Generate a contextual hint based on the exercise and user's code

        Args:
            exercise_context: Dictionary with exercise details
            user_code: The code the user has written so far
            hint_level: Level of hint (1-3, increasing specificity)

        Returns:
            Hint text
        """
        if not self.client:
            return self._fallback_hint(hint_level)

        instruction = exercise_context.get('instruction', '')
        solution = exercise_context.get('solution', '')

        prompt = f"""You are a Data Science tutor helping a student with an exercise.

Exercise: {instruction}

The student needs a hint at level {hint_level}/3:
- Level 1: Gentle nudge, ask guiding questions, point them in the right direction
- Level 2: More specific guidance, mention relevant functions/methods without giving away the answer
- Level 3: Very specific guidance, show the structure without complete code

Student's current code (if any):
```python
{user_code if user_code else '(No code written yet)'}
```

Provide an encouraging hint at level {hint_level}. Keep it concise (2-3 sentences).
Do NOT give the complete solution."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error generating hint: {e}")
            return self._fallback_hint(hint_level)

    def generate_feedback(self,
                         exercise_context: Dict,
                         user_code: str,
                         is_correct: bool,
                         error_message: str = "") -> str:
        """
        Generate personalized feedback on user's solution

        Args:
            exercise_context: Dictionary with exercise details
            user_code: The code submitted by the user
            is_correct: Whether the solution was correct
            error_message: Error message if solution was incorrect

        Returns:
            Feedback text
        """
        if not self.client:
            return self._fallback_feedback(is_correct, error_message)

        instruction = exercise_context.get('instruction', '')

        if is_correct:
            prompt = f"""The student solved this Data Science exercise correctly:

Exercise: {instruction}

Student's solution:
```python
{user_code}
```

Provide encouraging feedback (2-3 sentences) that:
1. Congratulates them
2. Mentions what they did well
3. Suggests one interesting related concept or optimization (if applicable)

Be enthusiastic but concise!"""

        else:
            prompt = f"""The student's solution to this Data Science exercise has an issue:

Exercise: {instruction}

Student's code:
```python
{user_code}
```

Error/Issue: {error_message}

Provide constructive feedback (2-3 sentences) that:
1. Explains what went wrong in simple terms
2. Guides them toward the solution without giving it away completely
3. Encourages them to keep trying

Be supportive and educational!"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error generating feedback: {e}")
            return self._fallback_feedback(is_correct, error_message)

    def explain_concept(self, concept_name: str, context: str = "") -> str:
        """
        Explain a Data Science concept in beginner-friendly terms

        Args:
            concept_name: Name of the concept to explain
            context: Additional context about what to focus on

        Returns:
            Explanation text
        """
        if not self.client:
            return f"Explanation for {concept_name} (LLM not available)"

        prompt = f"""Explain the Data Science concept: {concept_name}

{f'Context: {context}' if context else ''}

Provide a clear, beginner-friendly explanation that includes:
1. What it is in simple terms
2. When and why to use it
3. A practical example
4. One common pitfall to avoid

Keep it concise (4-5 sentences) and use simple language.
Target audience: Data Science learners."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error explaining concept: {e}")
            return f"Could not generate explanation for {concept_name}"

    def suggest_next_steps(self, completed_lessons: list, user_level: str) -> str:
        """
        Suggest what the user should learn next

        Args:
            completed_lessons: List of completed lesson IDs
            user_level: User's current level (beginner, intermediate, advanced)

        Returns:
            Suggestion text
        """
        if not self.client:
            return "Continue with the next lesson in the curriculum!"

        prompt = f"""A Data Science student has completed these lessons:
{', '.join(completed_lessons)}

Their current level: {user_level}

Based on their progress, suggest:
1. What they should focus on next (1-2 topics)
2. Why these topics are important
3. One encouraging remark about their progress

Keep it concise and motivating (3-4 sentences)."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return "Continue with the next lesson in the curriculum!"

    def _fallback_hint(self, level: int) -> str:
        """Fallback hints when LLM is not available"""
        hints = {
            1: "Think about the problem step by step. What's the first thing you need to do?",
            2: "Look at the example code above. Can you apply a similar approach?",
            3: "Check the documentation for the relevant function. The solution structure is similar to the examples."
        }
        return hints.get(level, hints[1])

    def _fallback_feedback(self, is_correct: bool, error_message: str) -> str:
        """Fallback feedback when LLM is not available"""
        if is_correct:
            return "Correct! Great job solving this exercise. Keep up the good work!"
        else:
            return f"Not quite right. {error_message} Take another look and try again!"
