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
	
	var armorNode	= get_node("Armor")
	var structNode	= get_node("Structure")
	
	for x in range(stats.armor):
		armorNode.add_child(armor.instantiate())
	for x in range(stats.struct):
		structNode.add_child(structure.instantiate())
	
	if armorNode.get_children().size() > 23:
		armorNode.global_position.y += 2
	if structNode.get_children().size() > 23:
		structNode.global_position.y -= 10
