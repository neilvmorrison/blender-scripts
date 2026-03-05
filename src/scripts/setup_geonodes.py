import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.geonodes import GeometryNodeBuilder

def create_geonodes():
  builder = GeometryNodeBuilder("ProceduralMesh")

  input_node = builder.get_input_node()
  output_node = builder.get_output_node()

  input_node.location = (-400, 0)
  output_node.location = (600, 0)

  subdiv = builder.add_node("GeometryNodeSubdivideMesh", label="Subdivide", location=(200, 100))
  cube = builder.add_node('GeometryNodeMeshCube', label="TestCube", location=(0,100))

  builder.set_param(cube, 'Size', (2.0, 2.0, 1.0))

  builder.connect(cube, 'Mesh', subdiv, 'Mesh')
  builder.connect(subdiv, 'Mesh', output_node, 'Geometry')

  print("Success!")

create_geonodes()