extends Control
class_name UnitCard

@export var stats: UnitInfo
const armor = preload("res://ArmorPip.tscn")
const structure = preload("res://StructurePip.tscn")

const dir = "ScaleControl/"

const maxVariant: int = 724
const maxTitle: int = 586

func _init(res: Resource = null) -> void:
	stats = res

func _ready():
	
	get_node(dir + "UnitImgContainer/Unit").texture = stats.unitIMG
	
	get_node(dir + "Labels/VARIANT").text = stats.variant
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

func resizeText(increase: float, label: Label, x: int) -> void:
	print("resizing")
	label.add_theme_font_size_override("font_size", floor(x/2))
	print("resizing Done")


func _on_title_item_rect_changed() -> void:
	var title: Label = get_node("ScaleControl/Labels/TITLE")
	if title.size.y > 100:
		print("Title Changed")
		resizeText(title.size.x/maxTitle, title, 64)


func _on_variant_item_rect_changed() -> void:
	var variant: Label = get_node("ScaleControl/Labels/VARIANT")
	if variant.size.y > 100:
		print("Variant Changed")
		resizeText(variant.size.x/maxVariant, variant, 48)
