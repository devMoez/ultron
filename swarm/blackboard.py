"""
Blackboard implementation for task coordination.
Provides atomic task claiming and result publishing using SQLite.
"""
import sqlite3
import json
import time
import uuid
from typing import List, Optional, Dict, Any
from .db import get_connection, init_db

class Blackboard:
    def __init__(self):
        # Ensure DB is initialized
        init_db()
    
    def post_task(self, description: str, required_skills: List[str] = None, 
                  priority: int = 0, project_path: str = "") -> int:
        """Post a new task to the blackboard. Returns task ID."""
        required_skills = required_skills or []
        with get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks 
                (description, required_skills, priority, project_path, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                description,
                json.dumps(required_skills),
                priority,
                project_path,
                time.time()
            ))
            task_id = cursor.lastrowid
            conn.commit()
        return task_id
    
    def claim_task(self, agent_id: int, agent_skills: List[str]) -> Optional[Dict[str, Any]]:
        """
        Atomically claim a task that matches agent's skills.
        Returns task dict if claimed, None if no suitable task.
        Uses SELECT ... FOR UPDATE to prevent race conditions.
        """
        with get_connection() as conn:
            # Start transaction
            conn.execute("BEGIN IMMEDIATE")
            
            # Find a queued task that matches agent's skills
            # We'll do a simple skill match: task requires subset of agent's skills
            cursor = conn.execute("""
                SELECT id, description, required_skills, priority, project_path
                FROM tasks 
                WHERE status = 'queued'
                ORDER BY priority DESC, created_at ASC
                LIMIT 10
            """)
            
            # Check each task for skill match (in Python for simplicity)
            # In production, we might want to do this in SQL with JSON functions
            rows = cursor.fetchall()
            task_to_claim = None
            
            for row in rows:
                required = json.loads(row['required_skills']) if row['required_skills'] else []
                # Check if agent has all required skills
                if all(skill in agent_skills for skill in required):
                    task_to_claim = dict(row)
                    break
            
            if task_to_claim:
                # Claim the task atomically
                conn.execute("""
                    UPDATE tasks 
                    SET status = 'claimed', 
                        assigned_agent = ?,
                        claimed_at = ?
                    WHERE id = ? AND status = 'queued'
                """, (agent_id, time.time(), task_to_claim['id']))
                
                # Verify we actually claimed it (another agent might have taken it)
                cursor = conn.execute(
                    "SELECT status FROM tasks WHERE id = ?", 
                    (task_to_claim['id'],)
                )
                if cursor.fetchone()['status'] == 'claimed':
                    conn.commit()
                    return task_to_claim
                else:
                    conn.rollback()
                    return None
            else:
                conn.rollback()
                return None
    
    def complete_task(self, task_id: int, result: str, success: bool = True):
        """Mark a task as completed with result."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE tasks 
                SET status = ?, 
                    result = ?,
                    completed_at = ?
                WHERE id = ?
            """, (
                'done' if success else 'failed',
                result,
                time.time(),
                task_id
            ))
            conn.commit()
    
    def fail_task(self, task_id: int, error: str):
        """Mark a task as failed, increment retry count."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE tasks 
                SET status = 'failed',
                    result = ?,
                    completed_at = ?,
                    retry_count = retry_count + 1
                WHERE id = ?
            """, (error, time.time(), task_id))
            conn.commit()
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get task details by ID."""
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", 
                (task_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_queued_count(self) -> int:
        """Get number of queued tasks."""
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE status = 'queued'"
            )
            return cursor.fetchone()['count']
    
    def get_agent_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all agents."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    a.name,
                    a.status,
                    a.success_rate,
                    a.tasks_completed,
                    COUNT(t.id) as active_tasks
                FROM agents a
                LEFT JOIN tasks t ON a.id = t.assigned_agent AND t.status IN ('claimed', 'done', 'failed')
                GROUP BY a.id
                ORDER BY a.tasks_completed DESC
            """)
            return [dict(row) for row in cursor.fetchall()]