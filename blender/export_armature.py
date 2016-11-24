#
# exports the active armature and its actions in 
# separated json files
#
import os
import bpy
import json

_ea_name = None

def export_armature(name, path):
    global _ea_name 
    _ea_name = name
    path = bpy.path.abspath(path) + name + "_armature.json"
    out = open(path, "w")
    print("exporting armature %s as %s"%(_ea_name, path))
    armature = bpy.data.objects[name].data
    out.write("{\n")
    out.write('"name":"%s",\n'%(name))
    out.write('"bones":[\n')
    bones = armature.bones
    bone_sep = ""
    for bone in bones:
        print(bone)
        out.write("%s{\n"%(bone_sep))
        bone_sep = ","
        out.write('"name":"%s",\n'%(bone.name))
        if bone.parent:
            out.write('"parent":"%s",\n'%(bone.parent.name))
        else:
            out.write('"parent":null,\n')
        out.write('"pos":{"x": %s, "y": %s},\n'%(bone.head[0], bone.head[1]))
        out.write('"rot": %s,\n'%(bone.matrix.to_euler()[2]))
        out.write('"sprites":[\n')

        out.write(']\n')
        out.write("}\n")
    out.write("]\n")
    out.write("}\n")
    out.close()
    return
