import bpy
import os
import subprocess

#usage:
#1. define the path to the 2d_open_anim_pipeline/blender/import_gimp_layers_from_json.py:
path =  bpy.path.abspath("//import_gimp_layers_from_json.py")
exec(compile(open(path).read(), path, 'exec')) 

#2. define the path to your gimp's json file:
path = bpy.path.abspath("//../gimp/submarine.json")

#3. use the import method:
import_gimp_layers(path)
