#
# exports the active armature and its actions in 
# separated json files
#

import os
import bpy
import json

_ea_name = None

def export_armature(name):
    global _ea_name 
    _ea_name = name
    print("exporting armature %s"%(_ea_name))
    return
