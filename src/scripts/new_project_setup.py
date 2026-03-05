import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import subprocess
import bpy
from pathlib import Path
from config import PROJECT_SAVE_DIRECTORY

NEW_PROJECT_NAME = 'road_test_2'

def create_and_save(directory: str, file_name: str) -> str:
  """
  Create a new blender file with {file_name} and save it in {save_dir}

  Returns:
   - filepath
  """

  Path(directory).mkdir(parents=True, exist_ok=True)

  file_path = os.path.join(directory, f"{file_name}.blend")
  bpy.ops.wm.save_mainfile(filepath=file_path)

  print(f"✓ Created and saved file: {file_path}")
  return file_path

def create_nurbs_path(length: float) -> bpy.types.Object | None:
  """
  TO-DO: Update this to accommodate more than NURBS curves
  Create initial geometry

  Args:
    - length: float - the length of the geometry
  
  Returns:
    - Geometry
  """
  bpy.ops.curve.primitive_nurbs_path_add(radius=1, align='WORLD', location=(0,0,0))
  curve_obj = bpy.context.active_object
  if curve_obj:
    curve_obj.name = 'NURBSPath'
    print(f"✓ Created NURBS path")
    return curve_obj
  else:
    print(f"Failed to create object")

def main(project_name: str):
  file_path = create_and_save(PROJECT_SAVE_DIRECTORY, project_name)

  curve_obj = create_nurbs_path(400)
  print(f"file_path: {file_path}")
  bpy.ops.wm.save_mainfile()
  print("All operations complete!")
  subprocess.Popen(["open", file_path])


if __name__ == "__main__":
  main(NEW_PROJECT_NAME)

