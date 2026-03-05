import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import subprocess
import bpy
from pathlib import Path
from config import PROJECT_SAVE_DIRECTORY

NEW_PROJECT_NAME = 'road_test_2'

def create_and_save(directory: str, file_name: str) -> str:
  """
  Create a new blender file with {file_name} and save it in {directory}

  Returns:
   - filepath
  """

  Path(directory).mkdir(parents=True, exist_ok=True)

  file_path = os.path.join(directory, f"{file_name}.blend")
  bpy.ops.wm.save_mainfile(filepath=file_path)

  print(f"✓ Created and saved file: {file_path}")
  return file_path


def main(project_name: str):
  file_path = create_and_save(PROJECT_SAVE_DIRECTORY, project_name)
  subprocess.Popen(["open", file_path])


if __name__ == "__main__":
  main(NEW_PROJECT_NAME)
