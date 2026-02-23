extends Control

@onready var unitCards = get_node("MainContainer/UnitCardContainer")
@onready var unitList = get_node("MainContainer/UnitListContainer")

const unitCard = preload("res://UnitCard.tscn")

func _ready() -> void:
	update()

func generateUnitCard(res: Resource) -> void:
	var card = unitCard.instantiate()
	card.stats = res
	card.visible = false
	unitCards.add_child(card)
	update()

func update() -> void:
	
	for button in unitList.get_children():
		unitList.remove_child(button)
		button.queue_free()
	
	for unit in unitCards.get_children():
		var newButton: UnitListButton = UnitListButton.new()
		newButton.myUnit = unit
		newButton.text = unit.stats.title.split(" ")[0] + " " + unit.stats.variant
		newButton.custom_minimum_size.y = 64
		newButton.add_theme_font_override("font", load("res://Fonts/Orbitron/static/Orbitron-Black.ttf"))
		newButton.add_theme_font_size_override("font_size", 24)
		newButton.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		newButton.visible = true
		unitList.add_child(newButton)


func _on_roster_button_down() -> void:
	get_node("MainContainer/UnitSearch").visible = false
	get_node("MainContainer/UnitCardContainer").visible = true

func _on_search_button_down() -> void:
	get_node("MainContainer/UnitCardContainer").visible = false
	get_node("MainContainer/UnitSearch").visible = true

func _on_quit_button_down() -> void:
	get_tree().quit()
