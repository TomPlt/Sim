extends Node2D

func _on_graph_bot_edge_activate(node1_name, node2_name):
#	print(node1_name, node2_name)
	for child in get_children():
		if node1_name == int(child.node1_name) and node2_name == int(child.node2_name):
			child.get_child(0).default_color = Color(1, 0, 0)
		pass
		
	
