#
# given a json file with GIMP layer information, 
# it will create quads that will match the GIMP image
#
import os
import bpy
import json

_igl_path = ""

def _igl_load_texture(name):
    global _igl_path
    imgpath = _igl_path + name + ".png"
    print("texture path: %s"%(imgpath))
    try:
        img = bpy.data.images.load(imgpath)
    except:
        raise NameError("Cannot load image %s" % imgpath)
    return

def import_gimp_layers(json_path):
    global _igl_path
    print("json path: %s"%(json_path))
    _igl_path = json_path.replace(bpy.path.basename(json_path), "")
    print("base path: %s"%(_igl_path))
    with open(json_path) as data_file:    
        data = json.load(data_file)
        json_img = data["img"]
        print("image: %s w:%s h:%s"%(json_img["name"], json_img["width"],  json_img["height"]))
        _igl_load_texture(json_img["name"])
        json_layers = data["layers"]
        for layer in json_layers:
            name = layer["name"]
            x = layer["x"]
            y = layer["y"]
            w = layer["width"]
            h = layer["height"]
            print("layer: %s x:%s y:%s w:%s h:%s "%(name, x, y, w, h))
        
    return

