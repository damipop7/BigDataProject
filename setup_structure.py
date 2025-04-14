import os

def create_project_structure():
    # Define the directory structure
    directories = [
        "data/raw",
        "data/processed",
        "models",
        "notebooks",
        "src/data",
        "src/features",
        "src/models",
        "tests"
    ]
    
    # Create directories
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        
    # Create __init__.py files
    init_paths = [
        "src",
        "src/data",
        "src/features",
        "src/models",
        "tests"
    ]
    
    for path in init_paths:
        with open(os.path.join(path, "__init__.py"), "w") as f:
            pass
            
    # Create .gitkeep in empty directories
    with open("models/.gitkeep", "w") as f:
        pass

if __name__ == "__main__":
    create_project_structure()