"""
True Swarm Agent: homogeneous workers that bid on tasks, execute them,
learn from outcomes, and update memory.
"""
import json
import time
import uuid
import threading
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from db import get_connection
from blackboard import Blackboard
from skill_library import SkillLibrary

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger("TrueSwarmAgent")

class TrueSwarmAgent:
    def __init__(self, agent_id: int = None, name: str = None):
        self.agent_id = agent_id
        self.name = name or f"agent-{uuid.uuid4().hex[:8]}"
        self.blackboard = Blackboard()
        self.skill_lib = SkillLibrary()
        self.running = False
        self.thread = None
        self.last_heartbeat = time.time()
        
        # Ensure agent exists in DB
        self._ensure_agent_record()
    
    def _ensure_agent_record(self):
        """Create or update agent record in DB."""
        with get_connection() as conn:
            if self.agent_id is None:
                # Insert new agent
                cursor = conn.execute("""
                    INSERT INTO agents (name, status, last_heartbeat, skills, success_rate, tasks_completed, created_at)
                    VALUES (?, 'idle', ?, ?, ?, ?, ?)
                """, (
                    self.name,
                    time.time(),
                    json.dumps([]),  # empty skills initially
                    0.0,
                    0,
                    time.time()
                ))
                self.agent_id = cursor.lastrowid
                conn.commit()
                logger.info(f"Registered new agent {self.name} with ID {self.agent_id}")
            else:
                # Update heartbeat
                conn.execute("""
                    UPDATE agents 
                    SET last_heartbeat = ?, status = 'idle'
                    WHERE id = ?
                """, (time.time(), self.agent_id))
                conn.commit()
    
    def get_skills(self) -> List[str]:
        """Get current skill list from DB."""
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT skills FROM agents WHERE id = ?", 
                (self.agent_id,)
            )
            row = cursor.fetchone()
            if row and row['skills']:
                return json.loads(row['skills'])
            return []
    
    def update_skills(self, skills: List[str]):
        """Update agent's skill list."""
        with get_connection() as conn:
            conn.execute("""
                UPDATE agents 
                SET skills = ?
                WHERE id = ?
            """, (json.dumps(skills), self.agent_id))
            conn.commit()
    
    def bid_for_task(self, task: Dict[str, Any]) -> float:
        """
        Compute confidence bid for a task.
        Higher is better.
        Factors: skill match, priority, agent's success rate, load.
        Returns 0.0 if agent cannot perform task (missing required skills).
        """
        required = json.loads(task.get('required_skills', '[]'))
        agent_skills = self.get_skills()
        
        # If missing any required skill, cannot bid (or bid very low)
        if not all(skill in agent_skills for skill in required):
            return 0.0
        
        # Skill match ratio (how many of agent's skills are useful)
        if agent_skills:
            match_ratio = len([s for s in agent_skills if s in required]) / len(agent_skills)
        else:
            match_ratio = 0.0
        
        # Priority factor (normalize 0-1, assume priority 0-10)
        priority = task.get('priority', 0)
        priority_factor = min(priority / 10.0, 1.0) if priority > 0 else 0.5
        
        # Success rate factor (higher is better)
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT success_rate FROM agents WHERE id = ?", 
                (self.agent_id,)
            )
            success_rate = cursor.fetchone()['success_rate'] or 0.0
        
        # Combine factors (weights can be tuned)
        confidence = (0.4 * match_ratio + 
                      0.3 * priority_factor + 
                      0.3 * success_rate)
        
        # Add small randomness to break ties
        confidence += (uuid.uuid4().int % 1000) / 10000.0
        
        return min(confidence, 1.0)
    
    def claim_and_execute(self):
        """Main loop: look for tasks, bid, claim if highest bidder, execute."""
        # In a real swarm, we'd have multiple agents bidding via blackboard.
        # For simplicity, we'll have each agent try to claim a task it can do.
        # To avoid race conditions, blackboard.claim_taks already does atomic check.
        # So we just try to claim a task; if we get it, we were the successful bidder.
        
        task = self.blackboard.claim_task(self.agent_id, self.get_skills())
        if task is None:
            return False  # No task claimed
        
        logger.info(f"Agent {self.name} claimed task {task['id']}: {task['description'][:50]}...")
        
        # Update agent status to busy
        with get_connection() as conn:
            conn.execute("""
                UPDATE agents 
                SET status = 'busy', last_heartbeat = ?
                WHERE id = ?
            """, (time.time(), self.agent_id))
            conn.commit()
        
        # Execute the task
        try:
            result = self._execute_task(task)
            success = True
            logger.info(f"Task {task['id']} completed successfully")
        except Exception as e:
            result = str(e)
            success = False
            logger.error(f"Task {task['id']} failed: {e}")
        
        # Report result to blackboard
        if success:
            self.blackboard.complete_task(task['id'], result, success=True)
        else:
            self.blackboard.fail_task(task['id'], result)
        
        # Update agent statistics and memory
        self._update_after_task(task, success, result)
        
        # Set agent back to idle
        with get_connection() as conn:
            conn.execute("""
                UPDATE agents 
                SET status = 'idle', last_heartbeat = ?
                WHERE id = ?
            """, (time.time(), self.agent_id))
            conn.commit()
        
        return True
    
    def _execute_task(self, task: Dict[str, Any]) -> str:
        """
        Execute a task by loading required skills and running them.
        For now, we assume skills are Python modules that define a `run` function.
        In future, this could be more generic.
        """
        required_skills = json.loads(task.get('required_skills', '[]'))
        if not required_skills:
            # No specific skills needed, maybe just a description
            return f"Task completed: {task['description']}"
        
        # For each required skill, try to load and execute
        results = []
        for skill_name in required_skills:
            skill = self.skill_lib.get_skill(skill_name)
            if not skill:
                raise ValueError(f"Skill {skill_name} not found in library")
            
            # In a real implementation, we'd dynamically load and execute the skill.
            # For now, we'll just note that we used the skill.
            results.append(f"Applied skill {skill_name}")
            
            # Record usage in episodic memory
            self._record_episodic_event('skill_used', {
                'skill': skill_name,
                'task_id': task['id'],
                'timestamp': time.time()
            })
        
        # If we have a specific handler for the task description, we could call it.
        # For now, just return that we applied the skills.
        return "; ".join(results)
    
    def _update_after_task(self, task: Dict[str, Any], success: bool, result: str):
        """Update agent's success rate, tasks completed, and memory."""
        # Update success rate (exponential moving average)
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT success_rate, tasks_completed FROM agents WHERE id = ?", 
                (self.agent_id,)
            )
            row = cursor.fetchone()
            old_success = row['success_rate'] or 0.0
            completed = row['tasks_completed'] or 0
            
            # New success rate: weight recent result more heavily
            alpha = 0.3  # learning rate
            new_success = old_success * (1 - alpha) + (1.0 if success else 0.0) * alpha
            
            conn.execute("""
                UPDATE agents 
                SET success_rate = ?, 
                    tasks_completed = ?
                WHERE id = ?
            """, (new_success, completed + 1, self.agent_id))
            
            # Record in episodic memory
            self._record_episodic_event('task_completed', {
                'task_id': task['id'],
                'success': success,
                'result': result[:500],  # truncate
                'timestamp': time.time()
            })
            
            # Optionally update semantic memory: reinforce skills used
            if success:
                required = json.loads(task.get('required_skills', '[]'))
                for skill_name in required:
                    self._reinforce_skill(skill_name)
            
            conn.commit()
    
    def _record_episodic_event(self, event_type: str, data: Dict[str, Any]):
        """Write an event to episodic memory."""
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO episodic_memory (agent_id, timestamp, event_type, data)
                VALUES (?, ?, ?, ?)
            """, (
                self.agent_id,
                time.time(),
                event_type,
                json.dumps(data)
            ))
            conn.commit()
    
    def _reinforce_skill(self, skill_name: str):
        """Increase weight/reputation of a skill in semantic memory."""
        with get_connection() as conn:
            # Get current weight
            cursor = conn.execute(
                "SELECT value FROM semantic_memory WHERE key = ?", 
                (f"skill_weight:{skill_name}",)
            )
            row = cursor.fetchone()
            current_weight = float(row['value']) if row else 1.0
            
            # Increase weight (could be more sophisticated)
            new_weight = min(current_weight + 0.1, 5.0)  # cap at 5.0
            
            conn.execute("""
                INSERT OR REPLACE INTO semantic_memory (key, value, updated_at)
                VALUES (?, ?, ?)
            """, (f"skill_weight:{skill_name}", str(new_weight), time.time()))
            conn.commit()
    
    def start(self):
        """Start the agent's main loop in a background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info(f"Agent {self.name} started")
    
    def stop(self):
        """Stop the agent's main loop."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info(f"Agent {self.name} stopped")
    
    def _run_loop(self):
        """Main loop: claim and execute tasks, sleep when none available."""
        while self.running:
            try:
                claimed = self.claim_and_execute()
                if not claimed:
                    # No task claimed, sleep a bit
                    time.sleep(1)
                else:
                    # After executing a task, maybe yield briefly
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in agent loop: {e}")
                time.sleep(5)  # back off on error
        
        # Ensure agent is marked offline
        with get_connection() as conn:
            conn.execute("""
                UPDATE agents 
                SET status = 'offline', last_heartbeat = ?
                WHERE id = ?
            """, (time.time(), self.agent_id))
            conn.commit()

# For testing
if __name__ == "__main__":
    import time
    agent = TrueSwarmAgent()
    agent.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()