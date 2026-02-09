extends Control
class_name UnitCard

@export var stats: UnitInfo
const armor = preload("res://ArmorPip.tscn")
const structure = preload("res://StructurePip.tscn")
	
const dir = "ScaleControl/"

func _ready():
	
	get_node(dir + "UnitImgContainer/Unit").texture = stats.unitIMG
	
	get_node(dir + "Labels/CALLSIGN").text = stats.callsign
	get_node(dir + "Labels/TITLE").text = stats.title
	get_node(dir + "Labels/PV").text = "PV: " + str(stats.pv)
	
	get_node(dir + "Labels/TP").text = stats.type
	get_node(dir + "Labels/SZ").text = str(stats.sz)
	get_node(dir + "Labels/TMM").text = str(stats.tmm)
	get_node(dir + "Labels/MV").text = str(stats.move)
	get_node(dir + "Labels/ROLE").text = stats.role
	get_node(dir + "Labels/SKILL").text = str(stats.skill)
	get_node(dir + "Labels/SHORT").text = str(stats.damageS)
	get_node(dir + "Labels/MEDIUM").text = str(stats.damageM)
	get_node(dir + "Labels/LONG").text = str(stats.damageL)
	get_node(dir + "Labels/OV").text = str(stats.damageL)
	get_node(dir + "Labels/SPECIAL").text = stats.printSpecial()
	
	createPips()

func createPips():
	
	var armorNode	= get_node(dir + "Armor")
	var structNode	= get_node(dir + "Structure")
	
	for x in range(stats.armor):
		armorNode.add_child(armor.instantiate())
	for x in range(stats.struct):
		structNode.add_child(structure.instantiate())
	
	if armorNode.get_children().size() > 23:
		armorNode.global_position.y += 2
	if structNode.get_children().size() > 23:
		structNode.global_position.y -= 10
