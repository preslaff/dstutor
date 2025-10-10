"""
Progress tracking system using SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List


class ProgressTracker:
    """Track user progress through the curriculum"""

    def __init__(self, user_id: str = "default"):
        """
        Initialize progress tracker

        Args:
            user_id: Unique user identifier
        """
        self.user_id = user_id

        # Create .dstutor directory in user's home
        self.data_dir = Path.home() / ".dstutor"
        self.data_dir.mkdir(exist_ok=True)

        self.db_path = self.data_dir / "progress.db"
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)

        # Lessons table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                user_id TEXT,
                lesson_id TEXT,
                status TEXT DEFAULT 'not_started',
                attempts INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                time_spent INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, lesson_id)
            )
        """)

        # Exercises table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                user_id TEXT,
                exercise_id TEXT,
                submitted_code TEXT,
                is_correct BOOLEAN,
                hints_used INTEGER,
                submitted_at TIMESTAMP,
                PRIMARY KEY (user_id, exercise_id, submitted_at)
            )
        """)

        # User stats table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id TEXT PRIMARY KEY,
                total_lessons_completed INTEGER DEFAULT 0,
                total_exercises_completed INTEGER DEFAULT 0,
                total_time_spent INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                last_active TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

        # Initialize user stats if not exists
        self._init_user_stats()

    def _init_user_stats(self):
        """Initialize user stats record"""
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT OR IGNORE INTO user_stats (user_id, last_active)
            VALUES (?, ?)
        """, (self.user_id, datetime.now()))

        conn.commit()
        conn.close()

    def mark_lesson_complete(self, lesson_id: str):
        """
        Mark a lesson as completed

        Args:
            lesson_id: Lesson identifier
        """
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT OR REPLACE INTO lessons
            (user_id, lesson_id, status, completed_at)
            VALUES (?, ?, 'completed', ?)
        """, (self.user_id, lesson_id, datetime.now()))

        # Update user stats
        conn.execute("""
            UPDATE user_stats
            SET total_lessons_completed = total_lessons_completed + 1,
                last_active = ?
            WHERE user_id = ?
        """, (datetime.now(), self.user_id))

        conn.commit()
        conn.close()

    def record_exercise_attempt(self,
                                exercise_id: str,
                                code: str,
                                is_correct: bool,
                                hints_used: int):
        """
        Record an exercise submission

        Args:
            exercise_id: Exercise identifier
            code: Submitted code
            is_correct: Whether the solution was correct
            hints_used: Number of hints used
        """
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            INSERT INTO exercises
            (user_id, exercise_id, submitted_code, is_correct, hints_used, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.user_id, exercise_id, code, is_correct, hints_used, datetime.now()))

        # Update lesson attempts
        conn.execute("""
            INSERT OR REPLACE INTO lessons
            (user_id, lesson_id, attempts)
            VALUES (?, ?, COALESCE((SELECT attempts FROM lessons WHERE user_id = ? AND lesson_id = ?), 0) + 1)
        """, (self.user_id, exercise_id, self.user_id, exercise_id))

        # Update user stats if correct
        if is_correct:
            conn.execute("""
                UPDATE user_stats
                SET total_exercises_completed = total_exercises_completed + 1,
                    last_active = ?
                WHERE user_id = ?
            """, (datetime.now(), self.user_id))

        conn.commit()
        conn.close()

    def get_progress_stats(self) -> Dict:
        """
        Get overall progress statistics

        Returns:
            dict with progress metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get user stats
        cursor.execute("""
            SELECT total_lessons_completed, total_exercises_completed,
                   total_time_spent, current_streak
            FROM user_stats
            WHERE user_id = ?
        """, (self.user_id,))

        stats = cursor.fetchone()

        if not stats:
            return {
                'completed_lessons': 0,
                'total_exercises': 0,
                'correct_exercises': 0,
                'accuracy': 0.0,
                'current_streak': 0
            }

        # Get exercise accuracy
        cursor.execute("""
            SELECT
                COUNT(DISTINCT exercise_id) as total,
                SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct
            FROM (
                SELECT exercise_id, is_correct
                FROM exercises
                WHERE user_id = ?
                GROUP BY exercise_id
                HAVING is_correct = 1
            )
        """, (self.user_id,))

        exercise_stats = cursor.fetchone()

        conn.close()

        return {
            'completed_lessons': stats[0],
            'total_exercises': exercise_stats[0] if exercise_stats[0] else 0,
            'correct_exercises': exercise_stats[1] if exercise_stats[1] else 0,
            'accuracy': (exercise_stats[1] / exercise_stats[0]) if exercise_stats[0] and exercise_stats[0] > 0 else 0.0,
            'current_streak': stats[3],
            'total_time': stats[2]
        }

    def get_lesson_status(self, lesson_id: str) -> str:
        """
        Get status of a specific lesson

        Args:
            lesson_id: Lesson identifier

        Returns:
            Status string ('not_started', 'in_progress', 'completed')
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status FROM lessons
            WHERE user_id = ? AND lesson_id = ?
        """, (self.user_id, lesson_id))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 'not_started'

    def get_topic_progress(self, topic: str) -> Dict:
        """
        Get progress for a specific topic

        Args:
            topic: Topic name

        Returns:
            dict with topic progress
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Count completed lessons starting with topic name
        cursor.execute("""
            SELECT COUNT(*) FROM lessons
            WHERE user_id = ? AND lesson_id LIKE ? AND status = 'completed'
        """, (self.user_id, f"{topic}_%"))

        completed = cursor.fetchone()[0]

        conn.close()

        # Assume 10 lessons per topic (would be dynamic in production)
        total = 10

        return {
            'topic': topic,
            'completed': completed,
            'total': total,
            'progress_pct': (completed / total * 100) if total > 0 else 0
        }

    def update_streak(self):
        """Update user's current streak"""
        conn = sqlite3.connect(self.db_path)

        # Logic to calculate streak based on last_active dates
        # For now, simple implementation

        conn.execute("""
            UPDATE user_stats
            SET current_streak = current_streak + 1,
                last_active = ?
            WHERE user_id = ?
        """, (datetime.now(), self.user_id))

        conn.commit()
        conn.close()

    def reset_lesson(self, lesson_id: str):
        """
        Reset progress for a specific lesson

        Args:
            lesson_id: Lesson identifier
        """
        conn = sqlite3.connect(self.db_path)

        conn.execute("""
            DELETE FROM lessons
            WHERE user_id = ? AND lesson_id = ?
        """, (self.user_id, lesson_id))

        conn.execute("""
            DELETE FROM exercises
            WHERE user_id = ? AND exercise_id = ?
        """, (self.user_id, lesson_id))

        conn.commit()
        conn.close()

    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """
        Get recent activity

        Args:
            limit: Number of recent items to return

        Returns:
            List of recent activity dicts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT exercise_id, is_correct, submitted_at
            FROM exercises
            WHERE user_id = ?
            ORDER BY submitted_at DESC
            LIMIT ?
        """, (self.user_id, limit))

        results = cursor.fetchall()
        conn.close()

        return [
            {
                'exercise_id': row[0],
                'is_correct': bool(row[1]),
                'submitted_at': row[2]
            }
            for row in results
        ]
