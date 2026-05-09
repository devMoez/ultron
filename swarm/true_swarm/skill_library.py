"""
Skill library for storing and retrieving agent skills.
Skills are versioned and stored in the database.
"""
import json
import os
from pathlib import Path
from .db import get_connection

class SkillLibrary:
    def __init__(self):
        self.swarm_root = Path(__file__).resolve().parent
        self.skills_dir = self.swarm_root / "skills"
        self.skills_dir.mkdir(exist_ok=True)
    
    def add_skill(self, name: str, version: str, source: str, metadata: dict = None):
        """
        Add or update a skill in the library.
        source: either the skill code as a string, or a path to a file (relative to swarm root).
        """
        # If source is a file path, read the content
        if os.path.isfile(source):
            with open(source, 'r', encoding='utf-8') as f:
                source_code = f.read()
        else:
            # Assume source is the code itself
            source_code = source
        
        metadata_json = json.dumps(metadata or {})
        
        with get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO skills (name, version, source, metadata)
                VALUES (?, ?, ?, ?)
            """, (name, version, source_code, metadata_json))
            conn.commit()
    
    def get_skill(self, name: str, version: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve a skill by name and optionally version. If version is None, get the latest."""
        with get_connection() as conn:
            if version is None:
                cursor = conn.execute("""
                    SELECT name, version, source, metadata FROM skills
                    WHERE name = ?
                    ORDER BY version DESC
                    LIMIT 1
                """, (name,))
            else:
                cursor = conn.execute("""
                    SELECT name, version, source, metadata FROM skills
                    WHERE name = ? AND version = ?
                """, (name, version))
            row = cursor.fetchone()
            if row:
                return {
                    'name': row['name'],
                    'version': row['version'],
                    'source': row['source'],
                    'metadata': json.loads(row['metadata']) if row['metadata'] else {}
                }
            return None
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """List all skills with their latest version."""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT name, version, source, metadata FROM skills
                ORDER BY name, version DESC
            """)
            skills = []
            for row in cursor.fetchall():
                skills.append({
                    'name': row['name'],
                    'version': row['version'],
                    'source': row['source'],
                    'metadata': json.loads(row['metadata']) if row['metadata'] else {}
                })
            return skills
    
    def save_skill_to_file(self, name: str, version: str = None, file_path: str = None):
        """Save a skill's source code to a file."""
        skill = self.get_skill(name, version)
        if not skill:
            raise ValueError(f"Skill {name}@{version or 'latest'} not found")
        
        if file_path is None:
            file_path = self.swarm_root / "skills" / f"{name}_{skill['version']}.py"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(skill['source'])
        return file_path