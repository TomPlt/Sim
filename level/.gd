extends Node2D

var node_active: bool 

func _ready():
	node_active = false

func _on_line_1_color_change_graph(name):
	node_active = true
	print(node_active)
	$sprite.modulate = Color(0, 1, 1) # green shade, children not affected

