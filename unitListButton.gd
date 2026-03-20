extends Button
class_name UnitListButton

var myUnit : Node

func _pressed() -> void:
	Global.Main._on_roster_button_down()
	for unit in Global.Main.unitCards.get_children():
		print(unit)
		if unit == myUnit:
			unit.visible = true
		else:
			unit.visible = false
