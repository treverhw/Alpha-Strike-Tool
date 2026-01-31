extends Resource
class_name UnitInfo

@export var unitIMG : Texture2D

@export var callsign:	String
@export var title	:	String
@export var pv		:	int

@export var type	:	String
@export var sz		:	int
@export var tmm		:	int
@export var move	:	int
@export var role	:	String
@export var skill	:	int

@export var damageS	:	int
@export var damageM	:	int	
@export var damageL	:	int

@export var ov		:	int
@export var armor	:	int
@export var struct	:	int
@export var special	:	Array[String] = []

func printSpecial() -> String:
	var ret : String = "SPECIAL: "
	for ability in special:
		ret += ability
		if ability != special.back():
			ret += ", "
	return ret
