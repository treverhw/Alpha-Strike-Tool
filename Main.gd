extends Control

@onready var unitCards = get_node("MainContainer/UnitCardContainer")
@onready var unitList = get_node("MainContainer/UnitListContainer")

func _ready() -> void:
	update()

func update() -> void:
	
	for button in unitList.get_children():
		unitList.remove_child(button)
		button.queue_free()

	for unit in unitCards.get_children():
		var newButton = UnitListButton.new()
		newButton.myUnit = unit
		newButton.text = unit.stats.variant
		newButton.visible = true
		unitList.add_child(newButton)

func _on_search_button_down() -> void:
	var search = load("res://UnitSearch.tscn").instantiate()
	add_child(search)

func _on_quit_button_down() -> void:
	get_tree().quit()
