extends TextureButton
class_name Pip

func _on_button_down() -> void:
	var past : bool = false
	for button in get_parent().get_children():
		if button == self:
			past = true
		elif past == true:
			button.set_pressed_no_signal(true)
		else:
			button.set_pressed_no_signal(false)
