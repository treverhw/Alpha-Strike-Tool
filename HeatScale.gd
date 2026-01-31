extends AnimatedSprite2D

func frameSwap(n : int):
	if frame == n:
		frame = 0
	else:
		frame = n

func _on_first_button_down() -> void:
	frameSwap(1)

func _on_second_button_down() -> void:
	frameSwap(2)

func _on_third_button_down() -> void:
	frameSwap(3)

func _on_shutdown_button_down() -> void:
	frameSwap(4)
