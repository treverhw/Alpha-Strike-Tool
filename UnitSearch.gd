extends Control
class_name UnitSearch

@onready var UnitList : ItemList = get_node("VBoxContainer/UnitList")
@onready var start: String = "res://Units/"
@onready var timer: Timer = get_node("Timer")

var taskID = -1

var curr: String = ""

func _ready() -> void:
	pass

func _on_line_edit_text_changed(new_text: String) -> void:
	curr = new_text
	timer.start()

func _on_timer_timeout() -> void:
	WorkerThreadPool.wait_for_task_completion(taskID)
	UnitList.clear()
	if curr != "" and len(curr) >= 2:
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
	for path in files:
		if ".tres" in path or ".tres.remap" in path:
			var clean_path = path.replace(".remap", "")
			var unit: Resource = load(clean_path)
			if is_instance_valid(unit):
				addUnitToList(unit)
			else:
				print("ERROR: " + clean_path + " Contains no unit")

func addUnitToList(unit: Resource) -> void:
	var idx = UnitList.add_item(unit.title + " " + unit.variant)
	UnitList.set_item_metadata(idx, unit)

func _on_unit_list_item_activated(index: int) -> void:
	var res = UnitList.get_item_metadata(index)
	Global.Main.generateUnitCard(res)
