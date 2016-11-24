#
# given a json file with GIMP layer information, 
# it will create quads that will match the GIMP image
#

import bpy
import json

def import_gimp_layers(json_path):
    print(json_path)
    with open(json_path) as data_file:    
        data = json.load(data_file)
        json_img = data["img"]
        print("image: %s w:%s h:%s"%(json_img["name"], json_img["width"],  json_img["height"]))
        
    return

