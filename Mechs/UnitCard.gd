extends Control
class_name UnitCard

@export var stats: UnitInfo
const armor = preload("res://ArmorPip.tscn")
const structure = preload("res://StructurePip.tscn")

func _ready():
	
	get_node("UnitImgContainer/Unit").texture = stats.unitIMG
	
	get_node("Labels/CALLSIGN").text = stats.callsign
	get_node("Labels/TITLE").text = stats.title
	get_node("Labels/PV").text = "PV: " + str(stats.pv)
	
	get_node("Labels/TP").text = stats.type
	get_node("Labels/SZ").text = str(stats.sz)
	get_node("Labels/TMM").text = str(stats.tmm)
	get_node("Labels/MV").text = str(stats.move)
	get_node("Labels/ROLE").text = stats.role
	get_node("Labels/SKILL").text = str(stats.skill)
	get_node("Labels/SHORT").text = str(stats.damageS)
	get_node("Labels/MEDIUM").text = str(stats.damageM)
	get_node("Labels/LONG").text = str(stats.damageL)
	get_node("Labels/OV").text = str(stats.damageL)
	get_node("Labels/SPECIAL").text = stats.printSpecial()
	
	createPips()

func createPips():
	
	for x in range(stats.armor):
		get_node("Armor").add_child(armor.instantiate())
	for x in range(stats.struct):
		get_node("Structure").add_child(structure.instantiate())
	
	if get_node("Armor").get_children().size() > 23:
		get_node("Armor").global_position.y += 2
	if get_node("Structure").get_children().size() > 23:
		get_node("Structure").global_position.y -= 10
