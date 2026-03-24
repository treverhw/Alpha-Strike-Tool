extends Control
class_name UnitSearch

@onready var UnitList : ItemList = get_node("VBoxContainer/UnitList")
@onready var start: String = "res://Units/"
@onready var timer: Timer = get_node("Timer")
@onready var typeHbox: HBoxContainer = get_node("VBoxContainer/optionBoxes")
@onready var classHbox: HBoxContainer = get_node("VBoxContainer/mechOptions")

var currentOptions: Array = []

var taskID = -1

var curr: String = ""

func _ready() -> void:
	pass

func _on_line_edit_text_changed(new_text: String) -> void:
	curr = new_text
	timer.start()
	currentOptions = []
	for option : CheckBox in typeHbox.get_children():
		if option.button_pressed:
			currentOptions.append(option.name)
	var counter = 4
	for option : CheckBox in classHbox.get_children():
		if option.button_pressed:
			currentOptions.append(counter)
		counter -= 1

func _on_timer_timeout() -> void:
	WorkerThreadPool.wait_for_task_completion(taskID)
	UnitList.clear()
	if curr != "":
		taskID = WorkerThreadPool.add_task(threadedSearch.bind(start,curr))

func threadedSearch(path: String, text: String) -> void:
	var files: Array[String] = []
	loadUnits(path, text, files)
	
	call_deferred("populateList", files)

func loadUnits(path: String, text: String, files: Array[String]) -> void:
	#print("Loading Units at " + path)
	var dir: DirAccess = DirAccess.open(path)
	if dir:
		dir.list_dir_begin()
		var file = dir.get_next()
		while file != "":
			var fullPath = path + file
			if dir.current_is_dir() and text.to_lower() in file.to_lower():
				loadUnits(path + file + "/", text, files)
			else:
				files.append(fullPath)
			file = dir.get_next()
	else: print("Error: Could not open path")

func populateList(files: Array[String]) -> void:
	print("Populating")
	print(currentOptions)

	for path in files:
		if ".tres" in path or ".tres.remap" in path:
			
			var clean_path = path.replace(".remap", "")
			var unit: Resource = load(clean_path)
			print(currentOptions)
			if is_instance_valid(unit):
				if unit.type in currentOptions and ("BM" not in currentOptions or unit.sz in currentOptions):
					addUnitToList(unit)
			else:
				print("ERROR: " + clean_path + " Contains no unit")

func addUnitToList(unit: Resource) -> void:
	var idx = UnitList.add_item(unit.title + " " + unit.variant)
	UnitList.set_item_metadata(idx, unit)

func _on_unit_list_item_activated(index: int) -> void:
	var res = UnitList.get_item_metadata(index)
	Global.Main.generateUnitCard(res)

func _on_line_edit_text_submitted(new_text: String) -> void:
	_on_line_edit_text_changed(new_text)

##Annoying tie together

func _on_bm_pressed() -> void:
	var mechOptions = get_node("VBoxContainer/mechOptions")
	mechOptions.visible = !mechOptions.visible
	if mechOptions.visible == true:
		for size in mechOptions.get_children():
			size.set_pressed_no_signal(true)
	else:
		for size in mechOptions.get_children():
			size.set_pressed_no_signal(false)
	_on_line_edit_text_changed(curr)

func _on_cv_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_ba_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_ci_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_af_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_assault_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_heavy_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_medium_pressed() -> void:
	_on_line_edit_text_changed(curr)

func _on_light_pressed() -> void:
	_on_line_edit_text_changed(curr)
