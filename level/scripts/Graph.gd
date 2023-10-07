extends Node2D

enum Turn {
	PLAYER,
	BOT
}

var GameOverScreen = preload("res://level/gameover.tscn")
var player_matrix = Array()
var bot_matrix = Array()
var current_turn = Turn.PLAYER

signal bot_edge_activate(node1_name, node2_name)

func _ready():
	var n = $GraphComponents/Nodes.get_child_count()
	for i in range(n):
		player_matrix.append([])
		bot_matrix.append([])
		for j in range(n):
			player_matrix[i].append(0)
			bot_matrix[i].append(0)

	for node in get_tree().get_nodes_in_group("GraphComponentsGroup"):
		if node.has_signal("edge_activated") and not node.is_connected("edge_activated", Callable(self, "_on_edge_activated")):
			node.connect("edge_activated", Callable(self, "_on_edge_activated"))

func has_triangle(matrix) -> bool:
	var n = matrix.size()
	for i in range(n):
		for j in range(n):
			for k in range(n):
				# Check if these nodes form a triangle
				if i != j and j != k and i != k and matrix[i][j] != 0 and matrix[j][k] != 0 and matrix[k][i] != 0:
					return true
	return false

func _on_edge_activated(node1_name, node2_name):
	if current_turn == Turn.PLAYER:
		player_matrix[int(node1_name)][int(node2_name)] = 1 
		player_matrix[int(node2_name)][int(node1_name)] = 1
		player_matrix[int(node1_name)][int(node1_name)] += 1 
		player_matrix[int(node2_name)][int(node2_name)] += 1 
		
		print("Player: ", int(node1_name), " ", int(node2_name))
		var found_triangle = has_triangle(player_matrix)
		if found_triangle:
			print('Player lost the game')
			show_game_over_screen("Player Lost")
		else: end_player_turn()

func bot_turn():
	var unconnected_edges = get_unconnected_edges()
	if unconnected_edges.size() > 0:
		var random_edge = unconnected_edges[randi() % unconnected_edges.size()]
		var i = int(random_edge[0])
		var j = int(random_edge[1])
		bot_matrix[i][j] = 1
		bot_matrix[j][i] = 1
		bot_edge_activate.emit(i, j)
		print("Bot: ", i, " ", j)
		if has_triangle(bot_matrix):
			print("Bot has lost the game")
			show_game_over_screen("Bot Lost")
		else:
			end_bot_turn()
			
func end_player_turn():
	current_turn = Turn.BOT
	bot_turn()

func end_bot_turn():
	current_turn = Turn.PLAYER

func get_unconnected_edges():
	var all_edges = []  # List of all edges in the graph
	var n = player_matrix.size()
	for i in range(n):
		for j in range(i+1, n):  # We start from i+1 to avoid repeated edges (i.e., (1,2) and (2,1))
			all_edges.append([i, j])
	var unconnected = []
	for edge in all_edges:
		var i = edge[0]
		var j = edge[1]
		if player_matrix[i][j] == 0 and bot_matrix[i][j] == 0:
			unconnected.append(edge)
	return unconnected

func show_game_over_screen(message: String):
	var game_over_instance = GameOverScreen.instantiate()
		# Connect the restart_game signal from the GameOverScreen instance to the _restart_game method
	game_over_instance.connect("restart_game", Callable(self, "_restart_game"))
	add_child(game_over_instance)
	game_over_instance.get_child(1).get_node("Message").text = message

func _restart_game():
	# Example: To simply reload the current scene.
	get_tree().reload_current_scene()
