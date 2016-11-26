import bpy
import os
import subprocess

#usage:
#1. copy this script in your model's blend file.
#2. define the path to the 2d_open_anim_pipeline/blender/export_armature.py:
path =  bpy.path.abspath("//export_armature.py")
exec(compile(open(path).read(), path, 'exec')) 

#3. use the export_armature and export_action methods that you need..
export_armature("submarine", "//")
export_action("move", "//")
