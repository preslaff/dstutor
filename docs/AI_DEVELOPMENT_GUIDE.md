# AI Development Guide for DS-Tutor

This guide explains how to develop and enable the AI-powered features of the DS-Tutor extension using Claude API.

## Table of Contents
1. [Overview](#overview)
2. [Quick Setup](#quick-setup)
3. [Architecture](#architecture)
4. [Enabling AI Features](#enabling-ai-features)
5. [AI Capabilities](#ai-capabilities)
6. [Development Workflow](#development-workflow)
7. [Testing AI Features](#testing-ai-features)
8. [Advanced Customization](#advanced-customization)
9. [Troubleshooting](#troubleshooting)

---

## Overview

DS-Tutor uses Claude (Anthropic's AI) to provide:
- **Intelligent hints** - Context-aware progressive hints (3 levels)
- **Personalized feedback** - Detailed feedback on correct/incorrect solutions
- **Concept explanations** - On-demand explanations of Data Science concepts
- **Learning path suggestions** - Recommendations based on progress

**Key Design Principle**: AI features are **optional enhancements**. The extension works fully without AI, using fallback messages.

---

## Quick Setup

### 1. Get Your API Key

```bash
# Visit Anthropic Console
open https://console.anthropic.com/

# Navigate to: Settings → API Keys → Create Key
# Copy your API key (starts with 'sk-ant-...')
```

### 2. Configure the API Key

Choose one of three methods:

**Method A: Environment Variable (Recommended for Development)**
```bash
# Linux/Mac
export ANTHROPIC_API_KEY='sk-ant-api03-...'

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=sk-ant-api03-...

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='sk-ant-api03-...'

# Add to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.bashrc
source ~/.bashrc
```

**Method B: .env File (Recommended for Projects)**
```bash
# Create .env file in project root
cd /path/to/dstutor
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." > .env

# Install python-dotenv (already in requirements.txt)
pip install python-dotenv

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

**Method C: Direct Configuration (Future Feature)**
```python
# In Jupyter notebook (not yet implemented)
%dstutor config --api-key sk-ant-api03-...
```

### 3. Verify Setup

```python
# In a Jupyter notebook
import os
print("API Key set:", bool(os.getenv("ANTHROPIC_API_KEY")))

# Load extension
%load_ext dstutor
%dstutor init

# Check configuration
%dstutor config
# Look for: llm_enabled: True
```

### 4. Test AI Features

```python
# Start a lesson
%dstutor start python

# Try an exercise (intentionally wrong)
result = "wrong answer"

# Check solution - should get AI-powered feedback
%dstutor check

# Request AI-powered hint
%dstutor hint
```

---

## Architecture

### Component: `FeedbackEngine` (`dstutor/llm/feedback_engine.py`)

```python
class FeedbackEngine:
    """AI-powered feedback using Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key from env or parameter"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def generate_hint(self, exercise_context, user_code, hint_level):
        """Generate progressive hints (levels 1-3)"""

    def generate_feedback(self, exercise_context, user_code, is_correct, error_message):
        """Generate personalized feedback"""

    def explain_concept(self, concept_name, context):
        """Explain Data Science concepts"""

    def suggest_next_steps(self, completed_lessons, user_level):
        """Suggest learning path"""
```

### Integration Points

**1. TutorEngine Initialization** (`dstutor/core/tutor_engine.py:36-37`)
```python
api_key = os.getenv("ANTHROPIC_API_KEY")
self.feedback_engine = FeedbackEngine(api_key) if api_key else None
```

**2. Exercise Validation** (`dstutor/core/tutor_engine.py:270-277`)
```python
# Generate AI feedback if available and solution is incorrect
if self.feedback_engine and not is_correct:
    ai_feedback = self.feedback_engine.generate_feedback(
        exercise_context=exercise,
        user_code=user_code,
        is_correct=is_correct,
        error_message=feedback
    )
    feedback = ai_feedback
```

**3. Hint Generation** (`dstutor/core/tutor_engine.py:319-324`)
```python
# Generate AI hint if no predefined hint and LLM available
if self.feedback_engine:
    return self.feedback_engine.generate_hint(
        exercise_context=exercise,
        user_code="",
        hint_level=level
    )
```

---

## Enabling AI Features

### For End Users

**1. Install DS-Tutor**
```bash
pip install ds-tutor  # When published
# or for now:
pip install -e /path/to/dstutor
```

**2. Set API Key**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

**3. Use in Jupyter**
```python
%load_ext dstutor
%dstutor init
# AI features automatically enabled if key is set
```

### For Developers

**1. Clone and Install**
```bash
git clone https://github.com/preslaff/dstutor.git
cd dstutor
pip install -e ".[dev]"
```

**2. Configure API Key**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Or export directly
export ANTHROPIC_API_KEY='sk-ant-...'
```

**3. Run Development Environment**
```bash
jupyter lab
# or
jupyter notebook
```

**4. Test Changes**
```python
# Reload extension after code changes
%reload_ext dstutor
%load_ext dstutor
```

---

## AI Capabilities

### 1. Progressive Hints (3 Levels)

**Level 1: Gentle Nudge**
- Asks guiding questions
- Points in the right direction
- Doesn't give away the answer

**Level 2: Specific Guidance**
- Mentions relevant functions/methods
- Shows approach without complete code
- More directive than level 1

**Level 3: Detailed Help**
- Shows structure without complete solution
- Very specific guidance
- Just short of giving the answer

**Example Prompts Used:**
```python
prompt = f"""You are a Data Science tutor helping a student with an exercise.

Exercise: {instruction}

The student needs a hint at level {hint_level}/3:
- Level 1: Gentle nudge, ask guiding questions
- Level 2: More specific guidance, mention functions
- Level 3: Very specific guidance, show structure

Student's current code:
```python
{user_code if user_code else '(No code written yet)'}
```

Provide an encouraging hint at level {hint_level}.
Keep it concise (2-3 sentences).
Do NOT give the complete solution."""
```

**Model Used:** `claude-3-5-sonnet-20241022`
**Max Tokens:** 300

### 2. Personalized Feedback

**For Correct Solutions:**
- Congratulates the student
- Mentions what they did well
- Suggests related concepts or optimizations

**For Incorrect Solutions:**
- Explains what went wrong in simple terms
- Guides toward the solution
- Encourages them to keep trying

**Example Prompts:**
```python
# For incorrect solutions
prompt = f"""The student's solution has an issue:

Exercise: {instruction}

Student's code:
```python
{user_code}
```

Error/Issue: {error_message}

Provide constructive feedback (2-3 sentences) that:
1. Explains what went wrong in simple terms
2. Guides them toward the solution
3. Encourages them to keep trying

Be supportive and educational!"""
```

**Model Used:** `claude-3-5-sonnet-20241022`
**Max Tokens:** 400

### 3. Concept Explanations

Provides beginner-friendly explanations of Data Science concepts:
- What it is in simple terms
- When and why to use it
- Practical example
- Common pitfall to avoid

**Usage (Future Command):**
```python
%dstutor explain "broadcasting in NumPy"
%dstutor explain "groupby operations"
```

**Model Used:** `claude-3-5-sonnet-20241022`
**Max Tokens:** 600

### 4. Learning Path Suggestions

Analyzes completed lessons and suggests next steps:
- Personalized topic recommendations
- Explanation of why topics are important
- Motivational feedback

**Usage (Future Command):**
```python
%dstutor suggest
```

---

## Development Workflow

### Adding New AI Features

**1. Add Method to FeedbackEngine**

```python
# In dstutor/llm/feedback_engine.py

def new_ai_feature(self, param1: str, param2: str) -> str:
    """
    New AI-powered feature

    Args:
        param1: Description
        param2: Description

    Returns:
        Response text
    """
    if not self.client:
        return self._fallback_response()

    prompt = f"""Your instruction to Claude here...

    Context: {param1}
    Additional info: {param2}

    Provide output that...
    Keep it concise."""

    try:
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,  # Adjust based on expected response length
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except Exception as e:
        print(f"Error in new_ai_feature: {e}")
        return self._fallback_response()

def _fallback_response(self) -> str:
    """Fallback when LLM is not available"""
    return "Default response when AI is unavailable"
```

**2. Integrate with TutorEngine**

```python
# In dstutor/core/tutor_engine.py

def use_new_feature(self, param1, param2):
    """Use the new AI feature"""
    if not self.feedback_engine:
        return "AI features not available"

    return self.feedback_engine.new_ai_feature(param1, param2)
```

**3. Add Magic Command**

```python
# In dstutor/core/extension.py

elif command == "newfeature":
    if len(args) < 2:
        display(HTML('<div>Usage: %dstutor newfeature <param></div>'))
        return
    self._cmd_newfeature(args[1])

def _cmd_newfeature(self, param):
    """Handle new AI feature command"""
    try:
        result = self.tutor_engine.use_new_feature(param, context)
        display(HTML(f'<div>{result}</div>'))
    except Exception as e:
        display(HTML(f'<div>Error: {str(e)}</div>'))
```

### Best Practices

**1. Always Provide Fallbacks**
```python
if not self.client:
    return self._fallback_hint(level)
```

**2. Handle Errors Gracefully**
```python
try:
    response = self.client.messages.create(...)
    return response.content[0].text
except Exception as e:
    print(f"Error: {e}")
    return fallback_message
```

**3. Keep Prompts Concise**
- Be specific about desired output format
- Limit response length with max_tokens
- Specify tone (encouraging, supportive, educational)

**4. Use Appropriate Token Limits**
- Hints: 300 tokens (~225 words)
- Feedback: 400 tokens (~300 words)
- Explanations: 600 tokens (~450 words)
- Suggestions: 300 tokens (~225 words)

**5. Cache API Client**
```python
# Initialize once in __init__
self.client = anthropic.Anthropic(api_key=self.api_key)

# Not: creating new client for each request
```

---

## Testing AI Features

### Manual Testing in Jupyter

```python
# Test hint generation
%load_ext dstutor
%dstutor init
%dstutor start pandas

# Write incorrect code
result = "wrong"

# Test AI feedback
%dstutor check

# Test progressive hints
%dstutor hint 1
%dstutor hint 2
%dstutor hint 3
```

### Unit Testing (Recommended)

```python
# tests/test_feedback_engine.py

import pytest
from dstutor.llm.feedback_engine import FeedbackEngine

def test_feedback_engine_initialization():
    """Test FeedbackEngine initializes correctly"""
    # Without API key
    engine = FeedbackEngine(api_key=None)
    assert engine.client is None

    # With API key
    engine = FeedbackEngine(api_key="test-key")
    assert engine.client is not None

def test_fallback_hints():
    """Test fallback hints when AI unavailable"""
    engine = FeedbackEngine(api_key=None)

    hint1 = engine.generate_hint({}, "", 1)
    assert "step by step" in hint1.lower()

    hint2 = engine.generate_hint({}, "", 2)
    assert "example" in hint2.lower()

@pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"),
                   reason="API key not available")
def test_real_hint_generation():
    """Test real API hint generation (requires API key)"""
    engine = FeedbackEngine()

    exercise = {
        'instruction': 'Create a pandas Series with 5 numbers',
        'solution': 'result = pd.Series([1, 2, 3, 4, 5])'
    }

    hint = engine.generate_hint(exercise, "", 1)
    assert len(hint) > 0
    assert "Series" in hint or "pandas" in hint.lower()
```

### Integration Testing

```python
# tests/test_ai_integration.py

def test_tutor_engine_with_ai():
    """Test TutorEngine properly uses FeedbackEngine"""
    import os

    # Set test API key
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'

    from dstutor.core.tutor_engine import TutorEngine
    engine = TutorEngine()

    # Verify AI is enabled
    assert engine.feedback_engine is not None

    # Test hint generation
    engine.start_topic('python')
    hint = engine.get_hint(1)
    assert hint is not None
```

### Testing Without API Calls (Mocking)

```python
# tests/test_feedback_engine_mock.py

from unittest.mock import Mock, patch
import pytest

@patch('anthropic.Anthropic')
def test_hint_generation_mock(mock_anthropic):
    """Test hint generation with mocked API"""
    # Setup mock
    mock_client = Mock()
    mock_response = Mock()
    mock_response.content = [Mock(text="Try using pd.Series()")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    # Test
    engine = FeedbackEngine(api_key="test-key")
    hint = engine.generate_hint({'instruction': 'Create a Series'}, "", 1)

    assert hint == "Try using pd.Series()"
    mock_client.messages.create.assert_called_once()
```

---

## Advanced Customization

### Custom Prompt Templates

Create a prompt template system:

```python
# dstutor/llm/prompts.py

HINT_PROMPTS = {
    'beginner': """You are tutoring a beginner Data Science student...
    Keep explanations very simple and use analogies.""",

    'intermediate': """You are tutoring an intermediate student...
    You can use technical terms but explain them briefly.""",

    'advanced': """You are tutoring an advanced student...
    Focus on best practices and optimization."""
}

def get_hint_prompt(level: str, exercise: dict, user_code: str, hint_level: int) -> str:
    """Generate prompt based on user level"""
    base_prompt = HINT_PROMPTS.get(level, HINT_PROMPTS['beginner'])
    return f"""{base_prompt}

Exercise: {exercise['instruction']}
Student's code: {user_code}
Hint level: {hint_level}/3

Provide an appropriate hint."""
```

### Model Selection

Configure different models for different tasks:

```python
# dstutor/llm/feedback_engine.py

class FeedbackEngine:
    def __init__(self, api_key, model_config=None):
        self.models = model_config or {
            'hints': 'claude-3-5-sonnet-20241022',  # Fast, good quality
            'feedback': 'claude-3-5-sonnet-20241022',  # Detailed responses
            'explanations': 'claude-3-5-sonnet-20241022',  # Deep understanding
        }

    def generate_hint(self, ...):
        response = self.client.messages.create(
            model=self.models['hints'],  # Use configured model
            ...
        )
```

### Caching Responses

Implement caching to reduce API calls:

```python
# dstutor/llm/feedback_engine.py

from functools import lru_cache
import hashlib

class FeedbackEngine:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cache = {}

    def generate_hint(self, exercise_context, user_code, hint_level):
        # Create cache key
        cache_key = self._create_cache_key(
            exercise_context['instruction'],
            user_code,
            hint_level
        )

        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Generate hint
        hint = self._generate_hint_from_api(...)

        # Cache result
        self.cache[cache_key] = hint
        return hint

    def _create_cache_key(self, *args):
        """Create unique cache key from arguments"""
        content = '||'.join(str(arg) for arg in args)
        return hashlib.md5(content.encode()).hexdigest()
```

### Cost Monitoring

Track API usage:

```python
# dstutor/llm/feedback_engine.py

class FeedbackEngine:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.usage_stats = {
            'total_calls': 0,
            'total_tokens': 0,
            'calls_by_type': {}
        }

    def generate_hint(self, ...):
        response = self.client.messages.create(...)

        # Track usage
        self.usage_stats['total_calls'] += 1
        self.usage_stats['total_tokens'] += response.usage.total_tokens
        self.usage_stats['calls_by_type']['hints'] = \
            self.usage_stats['calls_by_type'].get('hints', 0) + 1

        return response.content[0].text

    def get_usage_report(self):
        """Get usage statistics"""
        return self.usage_stats
```

---

## Troubleshooting

### Issue: "API key not found"

**Symptoms:**
```python
%dstutor config
# Shows: llm_enabled: False
```

**Solutions:**
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Set it correctly
export ANTHROPIC_API_KEY='sk-ant-...'

# Restart Jupyter kernel
# Kernel → Restart Kernel
```

### Issue: "anthropic package not installed"

**Symptoms:**
```
Warning: anthropic package not installed
```

**Solution:**
```bash
pip install anthropic>=0.25.0

# Or reinstall with all dependencies
pip install -e ".[dev]"
```

### Issue: API calls timing out

**Symptoms:**
- Hints/feedback take very long
- TimeoutError exceptions

**Solutions:**
```python
# Increase timeout in client initialization
self.client = anthropic.Anthropic(
    api_key=api_key,
    timeout=60.0  # 60 seconds
)

# Or reduce max_tokens
response = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,  # Reduced from 300
    ...
)
```

### Issue: Rate limiting (429 errors)

**Symptoms:**
```
Error generating hint: 429 Too Many Requests
```

**Solutions:**
```python
# Add retry logic with exponential backoff
import time
from anthropic import RateLimitError

def generate_hint_with_retry(self, ...):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = self.client.messages.create(...)
            return response.content[0].text
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                return self._fallback_hint(level)
```

### Issue: Unexpected responses

**Symptoms:**
- Hints are too vague or too specific
- Feedback doesn't match user level

**Solutions:**
```python
# Refine prompts with more specific instructions
prompt = f"""You are a Data Science tutor.

IMPORTANT:
- Keep response under 3 sentences
- Use simple language (explain like to a beginner)
- Do not provide complete code
- Focus on guiding, not telling

Exercise: {instruction}
..."""

# Add response validation
response_text = response.content[0].text
if len(response_text.split()) < 10:  # Too short
    # Try again with different prompt
    pass
```

### Issue: High costs

**Symptoms:**
- API bills higher than expected

**Solutions:**
```python
# 1. Implement caching (see Advanced Customization)
# 2. Reduce max_tokens
# 3. Use hints from YAML when available

def get_hint(self, level):
    # Check YAML hints first
    predefined_hints = exercise.get('hints', [])
    for hint in predefined_hints:
        if hint.get('level') == level:
            return hint.get('text')

    # Only use AI if no predefined hint
    if self.feedback_engine:
        return self.feedback_engine.generate_hint(...)
```

### Debugging AI Responses

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or add debug prints
def generate_hint(self, ...):
    print(f"[DEBUG] Generating hint level {hint_level}")
    print(f"[DEBUG] Exercise: {exercise_context.get('instruction')[:50]}...")

    response = self.client.messages.create(...)

    print(f"[DEBUG] Tokens used: {response.usage.total_tokens}")
    print(f"[DEBUG] Response: {response.content[0].text[:100]}...")

    return response.content[0].text
```

---

## Cost Estimation

**Pricing (as of 2024):**
- Claude 3.5 Sonnet: $3 per million input tokens, $15 per million output tokens

**Typical Usage per Student:**
```
Average per lesson:
- 3 hints: 3 × 300 tokens = 900 tokens
- 2 feedback checks: 2 × 400 tokens = 800 tokens
- Total: ~1,700 tokens/lesson (~$0.03)

For 57 lessons: ~$1.71 per student
```

**Ways to Reduce Costs:**
1. Cache common responses
2. Use YAML hints when available
3. Implement rate limiting per user
4. Use smaller models for simple tasks (future)

---

## Future Enhancements

### Planned Features

1. **Conversation Memory**
   - Remember previous interactions in session
   - Build on earlier explanations

2. **Adaptive Difficulty**
   - Adjust hint detail based on student performance
   - Provide harder challenges for advanced students

3. **Code Review**
   - Style suggestions
   - Best practices recommendations
   - Performance optimization tips

4. **Interactive Q&A**
   - `%dstutor ask "What is broadcasting?"`
   - Natural language queries about lessons

5. **Progress Analytics**
   - AI-generated progress reports
   - Personalized learning recommendations

---

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude API Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Best Practices for Prompting](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Token Counting](https://docs.anthropic.com/claude/docs/models-overview#model-comparison)

---

## Support

For issues with AI features:
1. Check this guide's troubleshooting section
2. Review logs for error messages
3. Test with simple exercises first
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - API key status (don't share the actual key!)
