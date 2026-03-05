import bpy
from mathutils import Vector

class GeometryNodeBuilder:
  """
  Helper Class to programmatically create GeoNode setups in blender
  """

  def __init__(self, obj_name = "GeometryObject"):
    """init with Blender object, create node tree"""
    # create or get object
    if obj_name not in bpy.data.objects:
      mesh = bpy.data.meshes.new(obj_name)
      self.obj = bpy.data.objects.new(obj_name, mesh)
      bpy.context.collection.objects.link(self.obj)
    else:
      self.obj = bpy.data.objects[obj_name]
    
    # create or get modifier
    if "GeometryNodes" not in self.obj.modifiers:
      self.modifier = self.obj.modifiers.new("GeometryNodes", "NODES")
    else:
      self.modifier = self.obj.modifiers["GeometryNodes"]

    # create or get node tree
    if self.modifier.node_group is None:
      self.tree = bpy.data.node_groups.new("GeometryNodes", "GeometryNodeTree")
      self.modifier.node_group = self.tree
      # New trees are empty — create the Group Input/Output nodes and default sockets
      self.tree.nodes.new("NodeGroupInput")
      self.tree.nodes.new("NodeGroupOutput")
      self.tree.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
      self.tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    else:
      self.tree = self.modifier.node_group
    
    # clear nodes if exist - optional
    # self.clear_nodes()

    self.nodes = self.tree.nodes
    self.links = self.tree.links

  def clear_nodes(self):
    """
    Remove all nodes except Group Input/Output
    """
    if self.nodes:
      nodes_to_remove = [n for n in self.nodes if n.type not in ('GROUP_INPUT', "GROUP_OUTPUT")]

      for node in nodes_to_remove:
        self.nodes.remove(node)
  
  def add_node(self, node_type, label=None, location=(0,0)):
    """
      Add a node to the tree

      Args:
        node_type: Blender node type (e.g., 'GeometryNodeMesh${Cube|Plane}')
        label: Custom label for the node
        location: (x, y) tuple for the note position within editor
      
      Returns:
        The created node
    """
    node = self.nodes.new(type=node_type)
    if label:
      node.label = label
    
    node.location = location
    return node
  
  def add_node_group(self, group_name, label=None, location=(0,0)):
    """
    Add a node group to the tree

    Args:
      group_name: name of the node group to instance
      label: custom label for the node
      location: (x,y) tuple for node position
    
    Returns:
      The group node
    """

    node = self.nodes.new(type="GeometryNodeGroup")
    node.node_tree = bpy.data.node_groups[group_name]

    if label:
      node.label = label

    node.location = location

    return node
  
  def connect(self, source_node, source_socket, destination_node, destination_socket):
    """
    Connect two nodes

    Args:
      - source_node: the source node
      - source_socket: the source nodes socket
      - destination_node: the destination node
      - destination_socket: the destination node's socket

    Returns:
      - Void
    """
    print(self, source_node, destination_node)
    source_output = source_node.outputs[source_socket]
    destination_input = destination_node.inputs[destination_socket]
    self.links.new(source_output, destination_input)

  def set_param(self, node, param_name, value):
    """
    Set a node parameter value

    Args:
      - node: the node
      - param_name: the name of the parameter
      - value: value to set on parameter
    
    Returns:
      - Void
    """

    if param_name in node.inputs:
      node.inputs[param_name].default_value = value
    else:
      setattr(node, param_name, value)

  def get_input_node(self):
    """
    Get group input node

    Args:
      - none
    
    Returns:
      - Group Input node
    """
    return next(n for n in self.nodes if n.type == "GROUP_INPUT")

  def get_output_node(self):
    """
    Get group output node

    Args:
      - None

    Returns:
      - Group Output node
    """
    return next(n for n in self.nodes if n.type == "GROUP_OUTPUT")

  def inspect_node(self, node):
    """Print all inputs and outputs of a node — useful for discovering socket names."""
    print(f"Node: {node.name} (type: {node.type})")
    print("  Inputs:")
    for i, inp in enumerate(node.inputs):
      print(f"    [{i}] '{inp.name}' ({inp.type})")
    print("  Outputs:")
    for i, out in enumerate(node.outputs):
      print(f"    [{i}] '{out.name}' ({out.type})")
