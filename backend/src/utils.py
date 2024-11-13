import os
import sys


def add_root_to_path():
    # Add the project root directory to sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    print(f"Adding `{project_root}` to sys.path")
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


# Add root to path whenever someone imports utils
add_root_to_path()
