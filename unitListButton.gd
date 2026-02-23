extends Button
class_name UnitListButton

var myUnit : Node

func _pressed() -> void:
	for unit in get_parent().get_parent().get_node("UnitCardContainer").get_children():
		if unit == myUnit:
			unit.visible = true
		else:
			unit.visible = false
