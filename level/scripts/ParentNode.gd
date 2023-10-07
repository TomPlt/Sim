extends Node2D

func _ready():
	for node in get_tree().get_nodes_in_group("GraphComponentsGroup"):
		if node.has_signal("edge_activated"):
			node.connect("edge_activated", Callable(self, "_on_edge_activated"))

func _on_edge_activated(node1_name, node2_name):
	for child in get_children():
		if child is Node2D:  # Make sure child is of type Node2D or its subclass
			if child.name == node1_name or child.name == node2_name:
				child.get_node("circle").color = Color(0, 1, 0)
				child.node_active = true

func _on_graph_bot_edge_activate(node1_name, node2_name):
	for child in get_children():
		if node1_name == int(str(child.name)) or node2_name == int(str(child.name)):
			child.get_child(0).color = Color(1, 0, 0)
