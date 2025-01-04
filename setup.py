import os

def create_project_structure():
    # Base directory (assuming you're in E:/Hiring_Assistant)
    base_dir = os.getcwd()
    
    # Create directories
    directories = [
        'chatbot',
        'utils'
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
        # Create __init__.py in each directory
        with open(os.path.join(base_dir, directory, '__init__.py'), 'w') as f:
            pass

    # Create main files
    files = {
        'app.py': '',
        'chatbot/bot.py': '',
        'chatbot/prompts.py': '',
        'utils/data_handler.py': '',
        'requirements.txt': 'streamlit\ntransformers\ntorch\npython-dotenv',
        'README.md': '# TalentScout Hiring Assistant\n\nAn intelligent chatbot for initial candidate screening.'
    }
    
    for file_path, content in files.items():
        with open(os.path.join(base_dir, file_path), 'w') as f:
            f.write(content)

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully!")