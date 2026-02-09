import requests
import json
import os
import re
import time
import string

# Configuration
QUERY_URL = "http://masterunitlist.info/Unit/QuickList?"
OUTPUT_DIR = "./Units"
IMG_DIR = "Sprites/Units/"
img_name = ""
alphabet = list(string.ascii_uppercase)

#Limited run, innersphere era 257
technologies = [1, 2]
era_ids = [257, 10, 13, 247, 14, 15, 254]

def cleanNameParts(unit):

    nameParts = str(unit["Name"]).split()

    counter = 0
    for part in nameParts:
        while "\"" in nameParts[counter]:
            nameParts[counter] = re.sub("\"", "(", nameParts[counter], count = 1)
            nameParts[counter] = re.sub("\"", ")", nameParts[counter], count = 1)
        while '"' in nameParts[counter]:
            nameParts[counter] = re.sub('"', "(", nameParts[counter], count = 1)
            nameParts[counter] = re.sub('"', ")", nameParts[counter], count = 1)
        while "/" in nameParts[counter]:
            nameParts[counter] = re.sub("/", " ", nameParts[counter], count = 1)

        counter += 1


    name = ""
    callsign = ""

    if unit["Technology"]["Name"] == "Clan":
        callsign = nameParts.pop()
        for part in nameParts:
            if name == "":
                name += part
            else: name += (" " + part)
    else:
        for part in nameParts:
            if "-" in part:
                callsign = part
            else: 
                if name == "":
                    name += part
                else: name += (" " + part)
    
    return callsign, name

def calculate_tmm(move_str):
    try:
        move_val = int(re.search(r'\d+', str(move_str)).group())
        if move_val <= 4: return "0"
        if move_val <= 8: return "1"
        if move_val <= 12: return "2"
        if move_val <= 18: return "3"
        if move_val <= 34: return "4"
        return "5"
    except (AttributeError, ValueError):
        return "0"

def generate_tres(unit):
    
    callsign, name = cleanNameParts(unit)
    
    name = name.upper()
    pv = str(unit["BFPointValue"])
    type = ""
    if unit["BFType"]:          type = unit["BFType"] 
    else:                       type = "None"
    size = str(unit["BFSize"])
    move = str(unit["BFMove"])
    move = move.replace('"', "")
    tmm =  calculate_tmm(unit["BFMove"])
    role = unit["Role"]["Name"]
    skill = "4"
    damageS = str(unit["BFDamageShort"])
    damageM = str(unit["BFDamageMedium"])
    damageL = str(unit["BFDamageLong"])
    ov = str(unit["BFOverheat"])
    armor = str(unit["BFArmor"])
    structure = str(unit["BFStructure"])
    special = ""
    specialList = unit
    if unit["BFAbilities"] and unit["BFAbilities"] != "None":
        specialList = unit["BFAbilities"].split(",")
        for ability in specialList:
            special += f'"{ability}"'
            if ability != specialList[len(specialList)-1]:
                special += ", "
    else:                       special = '""'


    #download the png
    img_name = unit["ImageUrl"].split("/").pop()
    if "\r\n" in img_name:
        img_name = img_name.replace("\r\n", "")
    folder = f"{img_name.split("-")[0].upper()}"

    #Image path "Sprites/Units/{img_name}"
    img_path = os.path.join(IMG_DIR, f"{img_name}")
    if not os.path.exists(img_path):
        img_data = requests.get(unit["ImageUrl"]).content
        with open(img_path, 'wb') as f:
            f.write(img_data)
            print(f"Image Downloaded: {img_path}")
            f.close()

    tres = f"""[gd_resource type="Resource" script_class="UnitInfo" load_steps=3 format=3]

[ext_resource type="Script" path="res://UnitInfo.gd" id="1_cs3jr"]
[ext_resource type="Texture2D" path="res://{img_path}" id="2_ynkeb"]

[resource]
script = ExtResource("1_cs3jr")
unitIMG = ExtResource("2_ynkeb")
callsign = "{callsign}"
title = "{name}"
pv = {pv}
type = "{type}"
sz = {size}
tmm = {tmm}
move = {move}
role = "{role}"
skill = {skill}
damageS = {damageS}
damageM = {damageM}
damageL = {damageL}
ov = {ov}
armor = {armor}
struct = {structure}
special = Array[String]([{special}])
metadata/_custom_type_script = "uid://dj1da82xsjhtw"
"""
    
    file_name = name + " " + callsign
    return file_name, tres, img_path


def generateScene(tres_path, img_path):


    first = f"""[gd_scene format=3]

[ext_resource type="Script" uid="uid://ckrs8cwf2baj3" path="res://Units/UnitCard.gd" id="1_8e0a1"]
[ext_resource type="Resource" path="res://{tres_path}" id="2_wavwk"]
[ext_resource type="Texture2D" uid="uid://bqjudwhrflhyt" path="res://Sprites/ASUnitCard.png" id="3_tqojt"]
[ext_resource type="Texture2D" path="res://{img_path}" id="4_kvswk"]
[ext_resource type="Texture2D" uid="uid://dupw7bm6c73ix" path="res://Sprites/ASUnitCard_Backdrop.png" id="5_whmh8"]
[ext_resource type="PackedScene" uid="uid://brcchflca8cel" path="res://CritPips.tscn" id="6_ctsk4"]
[ext_resource type="PackedScene" uid="uid://dljmcp2cwcfhl" path="res://ArmorPip.tscn" id="7_tg1ke"]
[ext_resource type="FontFile" uid="uid://b1vnm5eojsjn" path="res://Fonts/Orbitron/static/Orbitron-Regular.ttf" id="8_67y70"]
[ext_resource type="FontFile" uid="uid://dr1ehbyf7j7h" path="res://Fonts/Orbitron/static/Orbitron-Black.ttf" id="9_boxg6"]
[ext_resource type="FontFile" uid="uid://crhnk2w1fvpo" path="res://Fonts/Roboto_Condensed/static/RobotoCondensed-ExtraBold.ttf" id="10_d8mch"]
[ext_resource type="Texture2D" uid="uid://ev6hk5g21b0r" path="res://Sprites/heat_scale.png" id="11_0amtm"]
[ext_resource type="Script" uid="uid://b1ajh0ju0k2hb" path="res://HeatScale.gd" id="12_bgya8"]

[sub_resource type="AtlasTexture" id="AtlasTexture_m710d"]
atlas = ExtResource("11_0amtm")
region = Rect2(0, 0, 222, 47)

[sub_resource type="AtlasTexture" id="AtlasTexture_3cf8h"]
atlas = ExtResource("11_0amtm")
region = Rect2(222, 0, 222, 47)

[sub_resource type="AtlasTexture" id="AtlasTexture_1tsts"]
atlas = ExtResource("11_0amtm")
region = Rect2(444, 0, 222, 47)

[sub_resource type="AtlasTexture" id="AtlasTexture_f6t4s"]
atlas = ExtResource("11_0amtm")
region = Rect2(666, 0, 222, 47)

[sub_resource type="AtlasTexture" id="AtlasTexture_ur6nf"]
atlas = ExtResource("11_0amtm")
region = Rect2(888, 0, 222, 47)
"""
    middle = """
[sub_resource type="SpriteFrames" id="SpriteFrames_kabr8"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": SubResource("AtlasTexture_m710d")
}, {
"duration": 1.0,
"texture": SubResource("AtlasTexture_3cf8h")
}, {
"duration": 1.0,
"texture": SubResource("AtlasTexture_1tsts")
}, {
"duration": 1.0,
"texture": SubResource("AtlasTexture_f6t4s")
}, {
"duration": 1.0,
"texture": SubResource("AtlasTexture_ur6nf")
}],
"loop": true,
"name": &"default",
"speed": 5.0
}]

"""

    end = f"""
[node name="{tres_path.split().pop()[:-5]}" type="Control"]
custom_minimum_size = Vector2(1050, 750)
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
size_flags_horizontal = 3
size_flags_vertical = 3
script = ExtResource("1_8e0a1")
stats = ExtResource("2_wavwk")
metadata/_custom_type_script = "uid://ckrs8cwf2baj3"

[node name="ScaleControl" type="Control" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
grow_horizontal = 2
grow_vertical = 2
pivot_offset = Vector2(525, 375)

[node name="Card" type="TextureRect" parent="ScaleControl"]
z_index = 1
layout_mode = 0
texture = ExtResource("3_tqojt")
expand_mode = 1
stretch_mode = 3

[node name="UnitImgContainer" type="HBoxContainer" parent="ScaleControl"]
z_index = 2
custom_minimum_size = Vector2(312, 333)
layout_mode = 0
offset_left = 134.0
offset_top = -271.0
offset_right = 446.0
offset_bottom = 62.0
alignment = 1

[node name="Unit" type="TextureRect" parent="ScaleControl/UnitImgContainer"]
layout_mode = 2
size_flags_horizontal = 3
texture = ExtResource("4_kvswk")
expand_mode = 1
stretch_mode = 5

[node name="Background" type="TextureRect" parent="ScaleControl"]
z_index = -1
layout_mode = 0
offset_left = 94.0
offset_top = -346.0
offset_right = 498.0
offset_bottom = 94.0
texture = ExtResource("5_whmh8")
expand_mode = 1
stretch_mode = 3

[node name="Armor" type="HFlowContainer" parent="ScaleControl"]
z_index = 3
layout_mode = 0
offset_left = -450.0
offset_top = 78.03
offset_right = 728.03015
offset_bottom = 153.7876
scale = Vector2(0.4, 0.4)

[node name="Structure" type="HFlowContainer" parent="ScaleControl"]
z_index = 3
layout_mode = 0
offset_left = -450.0
offset_top = 111.36401
offset_right = 720.45435
offset_bottom = 183.33386
scale = Vector2(0.4, 0.4)

[node name="Crits" type="VBoxContainer" parent="ScaleControl"]
z_index = 3
layout_mode = 0
offset_left = 205.0
offset_top = 126.00003
offset_right = 521.66675
offset_bottom = 466.00003
scale = Vector2(0.3, 0.3)
theme_override_constants/separation = 28

[node name="CritPip" parent="ScaleControl/Crits" instance=ExtResource("6_ctsk4")]
layout_mode = 2

[node name="HBoxContainer" type="HBoxContainer" parent="ScaleControl/Crits"]
layout_mode = 2
theme_override_constants/separation = 20

[node name="ArmorPip" parent="ScaleControl/Crits/HBoxContainer" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip2" parent="ScaleControl/Crits/HBoxContainer" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip3" parent="ScaleControl/Crits/HBoxContainer" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip4" parent="ScaleControl/Crits/HBoxContainer" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="HBoxContainer2" type="HBoxContainer" parent="ScaleControl/Crits"]
layout_mode = 2
theme_override_constants/separation = 20

[node name="ArmorPip2" parent="ScaleControl/Crits/HBoxContainer2" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip3" parent="ScaleControl/Crits/HBoxContainer2" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip4" parent="ScaleControl/Crits/HBoxContainer2" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip5" parent="ScaleControl/Crits/HBoxContainer2" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="HBoxContainer3" type="HBoxContainer" parent="ScaleControl/Crits"]
layout_mode = 2
theme_override_constants/separation = 20

[node name="ArmorPip2" parent="ScaleControl/Crits/HBoxContainer3" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip3" parent="ScaleControl/Crits/HBoxContainer3" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip4" parent="ScaleControl/Crits/HBoxContainer3" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="ArmorPip5" parent="ScaleControl/Crits/HBoxContainer3" instance=ExtResource("7_tg1ke")]
layout_mode = 2

[node name="Labels" type="Control" parent="ScaleControl"]
z_index = 2
anchors_preset = 0
offset_left = -526.0
offset_top = -370.0
offset_right = -486.0
offset_bottom = -330.0

[node name="CALLSIGN" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 55.0
offset_top = 32.0
offset_right = 259.0
offset_bottom = 93.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("8_67y70")
theme_override_font_sizes/font_size = 48
text = "callsign"

[node name="TITLE" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 55.0
offset_top = 82.0
offset_right = 195.0
offset_bottom = 163.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("9_boxg6")
theme_override_font_sizes/font_size = 64
text = "title"

[node name="PV" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 862.0
offset_top = 22.0
offset_right = 989.0
offset_bottom = 70.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 44
text = "PV: 000"

[node name="TP" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 98.015
offset_top = 162.0
offset_right = 138.01515
offset_bottom = 210.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "tp"

[node name="SZ" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 233.0
offset_top = 162.0
offset_right = 273.0
offset_bottom = 210.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "sz"

[node name="TMM" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 370.0
offset_top = 162.0
offset_right = 442.0
offset_bottom = 210.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "tmm"

[node name="MV" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 504.0
offset_top = 162.0
offset_right = 552.0
offset_bottom = 210.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "mv"

[node name="ROLE" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 130.0
offset_top = 200.0
offset_right = 192.0
offset_bottom = 248.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "role"

[node name="SKILL" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 505.0
offset_top = 200.0
offset_right = 573.0
offset_bottom = 248.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "skill"

[node name="SHORT" type="Label" parent="ScaleControl/Labels"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = 91.0
offset_top = 286.0
offset_right = 176.0
offset_bottom = 334.0
grow_horizontal = 2
grow_vertical = 2
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "short"
horizontal_alignment = 1

[node name="MEDIUM" type="Label" parent="ScaleControl/Labels"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = 255.0
offset_top = 286.0
offset_right = 383.0
offset_bottom = 334.0
grow_horizontal = 2
grow_vertical = 2
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "medium"
horizontal_alignment = 1

[node name="LONG" type="Label" parent="ScaleControl/Labels"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = 480.0
offset_top = 286.0
offset_right = 550.0
offset_bottom = 334.0
grow_horizontal = 2
grow_vertical = 2
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "long"
horizontal_alignment = 1

[node name="OV" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 103.0
offset_top = 369.0
offset_right = 143.0
offset_bottom = 417.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("10_d8mch")
theme_override_font_sizes/font_size = 40
text = "ov"

[node name="SPECIAL" type="Label" parent="ScaleControl/Labels"]
layout_mode = 0
offset_left = 53.0
offset_top = 544.0
offset_right = 123.0
offset_bottom = 568.0
theme_override_colors/font_color = Color(0, 0, 0, 1)
theme_override_fonts/font = ExtResource("8_67y70")
theme_override_font_sizes/font_size = 18
text = "special"

[node name="HeatScale" type="AnimatedSprite2D" parent="ScaleControl"]
z_index = 1
position = Vector2(-17, 24)
sprite_frames = SubResource("SpriteFrames_kabr8")
script = ExtResource("12_bgya8")

[node name="first" type="Button" parent="ScaleControl/HeatScale"]
z_index = -1
offset_left = -106.0
offset_top = -21.0
offset_right = -50.0
offset_bottom = 22.0
text = "1"

[node name="second" type="Button" parent="ScaleControl/HeatScale"]
z_index = -1
offset_left = -50.0
offset_top = -21.0
offset_right = 1.0
offset_bottom = 22.0
text = "2"

[node name="third" type="Button" parent="ScaleControl/HeatScale"]
z_index = -1
offset_left = 1.0
offset_top = -21.0
offset_right = 53.0
offset_bottom = 22.0
text = "3"

[node name="shutdown" type="Button" parent="ScaleControl/HeatScale"]
z_index = -1
offset_left = 53.0
offset_top = -21.0
offset_right = 108.0
offset_bottom = 22.0
text = "S"

[connection signal="button_down" from="ScaleControl/HeatScale/first" to="ScaleControl/HeatScale" method="_on_first_button_down"]
[connection signal="button_down" from="ScaleControl/HeatScale/second" to="ScaleControl/HeatScale" method="_on_second_button_down"]
[connection signal="button_down" from="ScaleControl/HeatScale/third" to="ScaleControl/HeatScale" method="_on_third_button_down"]
[connection signal="button_down" from="ScaleControl/HeatScale/shutdown" to="ScaleControl/HeatScale" method="_on_shutdown_button_down"]
"""
    return first + middle + end
    

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Fetching data from Master Unit List...")

    for tech in technologies:
        for era in era_ids:
                try:
                    json_name = f"JSON_Data/Types_18_Technologies_{tech}_AvailableEras_{era}"
                    
                    #Download the JSON if it doesn't exist, otherwise load it from the file
                    if not os.path.exists(f"{json_name}.json"):

                        print("Requesting JSON")
                        response = requests.get(f"{QUERY_URL}Types=18&Technologies={tech}&AvailableEras={era}")
                        print("Request Retrieved")
                        response.raise_for_status()
                        with open(f"{json_name}.json", "w", encoding='utf-8') as file:
                            file.write(response.text)

                    else: print("File already exists!")

                    #Load the JSON data from the file
                    with open(f"{json_name}.json", "r", encoding='utf-8') as jf:
                        data = json.load(jf)
                    unitList = data["Units"]

                    #create the tres
                    for unit in unitList:
                        time.sleep(.1)
                        if unit["BFPointValue"] != 0:
                            print(f"Processing: {unit['Name']} | {unit['Type']['Name']} | {unit['Technology']['Name']} era {unit['EraId']} from {unit['DateIntroduced']}")
                            
                            #Generate the resource file
                            file_name, tres, img_path = generate_tres(unit)
                            tres_path = f"{file_name.split()[0]}/{file_name}.tres"
                            print(tres_path)
                            os.makedirs(os.path.join(OUTPUT_DIR, f"{file_name.split()[0]}"), exist_ok=True)
                            file_path = os.path.join(OUTPUT_DIR, tres_path)

                            #Write the resource file
                            #print(f"Resource Attempt: {file_path}")
                            with open(file_path, "w") as f:
                                f.write(tres)
                            #print(f"Resource Created: {file_path}")

                            #Generate the Scene file
                            tscn = generateScene(f"Units/{tres_path}", img_path)
                            tscn_path = f"{file_name.split()[0]}/{file_name}.tscn"
                            file_path = os.path.join(OUTPUT_DIR, tscn_path)

                            #Write the Scene file
                            #print(f"Scene Attempt: {file_path}")
                            with open(file_path, "w") as f:
                                f.write(tscn)
                            #print(f"Scene Created: {file_path}")
                
                        
                except requests.exceptions.RequestException as e:
                    print(f"Network error: {e}")
                except json.JSONDecodeError:
                    print("Error: The server did not return valid JSON.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()