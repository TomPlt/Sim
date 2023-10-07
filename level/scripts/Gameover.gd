extends Control

# In GameOverScreen.gd
signal restart_game

func _on_button_button_down():
	print("signal sent")
	emit_signal("restart_game")
