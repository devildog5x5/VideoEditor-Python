"""
Project Manager
Handles saving and loading video editor projects
"""

import json
import os
from datetime import datetime

class ProjectManager:
    """Manages video editor projects"""
    
    def __init__(self):
        self.current_project = None
    
    def create_new(self):
        """Create a new project"""
        return {
            'name': 'Untitled Project',
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def save(self, filepath, project_data):
        """Save project to file"""
        project = {
            'metadata': self.current_project or self.create_new(),
            'data': project_data,
            'version': '1.0'
        }
        
        project['metadata']['modified'] = datetime.now().isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(project, f, indent=2)
        
        self.current_project = project['metadata']
    
    def load(self, filepath):
        """Load project from file"""
        with open(filepath, 'r') as f:
            project = json.load(f)
        
        self.current_project = project.get('metadata', {})
        return project.get('data', {})
    
    def get_project_info(self):
        """Get current project information"""
        return self.current_project

