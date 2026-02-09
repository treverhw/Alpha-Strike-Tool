extends Control

@onready var unitCards = get_node("MainContainer/UnitCardContainer")
@onready var unitList = get_node("MainContainer/UnitListContainer")

func _ready() -> void:
	update()

func update() -> void:
	
	for unit in unitCards.get_children():
		var newButton = unitList.get_child(0).duplicate()
		unitList.add_child(newButton)
		newButton.myUnit = unit
		newButton.text = unit.stats.callsign
		newButton.visible = true
		

func _on_quit_button_down() -> void:
	get_tree().quit()
