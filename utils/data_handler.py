import json
import os
from datetime import datetime

class DataHandler:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_candidate_data(self, candidate_info):
        """Save candidate information to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        candidate_name = candidate_info.get('name', 'unknown').replace(' ', '_').lower()
        filename = f"{candidate_name}_{timestamp}.json"
        
        # Add timestamp to candidate info
        candidate_info['submission_time'] = datetime.now().isoformat()
        
        file_path = os.path.join(self.data_dir, filename)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(candidate_info, f, indent=4)
            return True, file_path
        except Exception as e:
            return False, str(e)

    def get_candidate_data(self, filename):
        """Retrieve candidate information from a JSON file"""
        file_path = os.path.join(self.data_dir, filename)
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            return None