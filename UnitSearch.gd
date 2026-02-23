extends Control
class_name UnitSearch

@onready var UnitList : ItemList = get_node("VBoxContainer/UnitList")
@onready var start: String = "res://Units/"

var UnitDB: Dictionary = {}

func _ready() -> void:
	pass

func _on_line_edit_text_changed(new_text: String) -> void:
	#print("Edited")
	UnitList.clear()
	UnitDB.clear()
	new_text = new_text.to_upper()
	if new_text != "":
		loadUnits(start, new_text)

func loadUnits(path: String, text: String) -> void:
	#print("Loading Units at " + path)
	var dir: DirAccess = DirAccess.open(path)
	var curr: DirAccess
	if dir:
		dir.list_dir_begin()
		var file = dir.get_next()
		while file != "" and len(text) >= 2:
			print(text + " | " + file + " -> " + str(file.begins_with(text)))
			if dir.current_is_dir() and file.to_lower().begins_with(text.to_lower()):
				loadUnits(path + file + "/", text)
			else:
				addUnitToList(path + file)
			file = dir.get_next()
	else: print("Error: Could not open path")

func addUnitToList(file: String) -> void:
	if ".tres" in file:
		var unit: Resource = load(file)
		var idx = UnitList.add_item(unit.title + " " + unit.variant)
		UnitList.set_item_metadata(idx, unit)
		print(unit.variant + " Added at index " + str(idx))
