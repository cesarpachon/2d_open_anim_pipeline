#
# exports the active armature and its actions in 
# separated json files
#
import os
import bpy
import json

_ea_name = None

def _ea_write_str(key, val, out):
    out.write('"%s":"%s"\n'%(key, val))
    return

def _ea_write_num(key, val, out):
    out.write('"%s":%s\n'%(key, val))
    return

def _ea_write_vector2(key, val, out):
    out.write('"%s":{"x":%s, "y":%s}\n'%(key, val[0], val[1]))
    return

def _ea_export_sprites(obj, bone, out):
    sp_sep = ""
    for child in obj.children:
        if child.parent_bone == bone.name:
            out.write("%s{\n"%(sp_sep))
            sp_sep = ","
            _ea_write_str("name", child.name, out)
            out.write(",")
            _ea_write_vector2("pos", child.location, out)
            out.write(",")
            _ea_write_num("rot", child.rotation_euler[2], out)
            out.write("}\n")
    return

def export_armature(name, path):
    global _ea_name 
    _ea_name = name
    path = bpy.path.abspath(path) + name + "_armature.json"
    out = open(path, "w")
    print("exporting armature %s as %s"%(_ea_name, path))
    obj = bpy.data.objects[name]
    armature = obj.data
    out.write("{\n")
    out.write('"name":"%s",\n'%(name))
    out.write('"bones":[\n')
    bones = armature.bones
    bone_sep = ""
    for bone in bones:
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
        _ea_export_sprites(obj, bone, out)
        out.write(']\n')
        out.write("}\n")
    out.write("]\n")
    out.write("}\n")
    out.close()
    return
