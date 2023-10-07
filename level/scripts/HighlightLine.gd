extends Area2D

var originalColors = []
var playerColor: Color = Color(0, 1, 0)
var defaultColor: Color = Color(1, 1, 1)
var enemyColor: Color = Color(1, 0, 0)

@export var node1_name : String
@export var node2_name : String

signal edge_activated(node1_name, node2_name)

func _ready():
	# Store the original colors of all child Line2D nodes
	for child in get_children():
#		add_to_group("GraphComponentsGroup")
		if child is Line2D:
			originalColors.append(child.default_color)

func _on_mouse_entered():
	for i in range(originalColors.size()):
		if get_child(i) is Line2D:
			if get_child(i).default_color != Color(1, 0, 0):
				get_child(i).default_color = playerColor  # Green

func _on_mouse_exited():
	for i in range(originalColors.size()):
		if get_child(i) is Line2D:
			if get_child(i).default_color != Color(1, 0, 0):
				get_child(i).default_color = originalColors[i]

func _on_input_event(_viewport, event, _shape_idx):
	if event is InputEventMouseButton and event.pressed:
		for i in range(originalColors.size()):
			if get_child(i) is Line2D:
				if originalColors[i] != playerColor:
					originalColors[i] = playerColor
					edge_activated.emit(node1_name, node2_name)
				get_child(i).default_color = originalColors[i]
