extends Area2D

var originalColors = []

func _ready():
	# Store the original colors of all child Line2D nodes
	for child in get_children():
		if child is Line2D:		originalColors.append(child.default_color)

func _on_mouse_entered():
	for i in range(originalColors.size()):
		if get_child(i) is Line2D:
			get_child(i).default_color = Color(0, 1, 0)  # Green

func _on_mouse_exited():
	for i in range(originalColors.size()):
		if get_child(i) is Line2D:
			get_child(i).default_color = originalColors[i]
