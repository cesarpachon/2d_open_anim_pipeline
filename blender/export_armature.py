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

def _ea_export_curves(action, out):
    cv_sep = ""
    for curve in action.fcurves:
        bone = curve.data_path.split('"')[1]
        channel = curve.data_path.split(".")[2]
        
        #channel filtering
        #here we discard or rename some curves
        export = 0
        label = None
        #discard z position channel
        if channel == "location" and curve.array_index < 2:        
            export = 1
            if curve.array_index == 0:
                label = "pos.x"
            else: 
                label = "pos.y"
        
        if export:           
            out.write("%s{\n"%(cv_sep))
            cv_sep = ","
            _ea_write_str("bone", bone, out)
            out.write(",")
            _ea_write_str("channel", label, out)
            out.write(",")
            _ea_write_keyframes(curve, out)
            out.write("}\n")
        else:
            print("skipping channel %s with index %d"%(channel, curve.array_index))
    return

def _ea_write_keyframes(curve, out):
    sep = ""
    out.write('"keyframes":[\n')
    for frame in curve.keyframe_points:
        out.write(sep)
        sep = ","
        out.write(" [%s, %s]\n"%(frame.co[0], frame.co[1]))
    out.write(']\n')
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

#export an armature to a json file with the name of the 
#armature plus the suffix _armature.json
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

#exports an action to a json file with the name of the action
#and the suffix _animation.json
def export_action(name, path):
    action = bpy.data.actions[name]
    path = bpy.path.abspath(path) + name + "_animation.json"
    out = open(path, "w")
    print("exporting action %s as %s"%(name, path))
    out.write("{\n")
    _ea_write_str("name", name, out)
    out.write(",")
    _ea_write_num("frames", action.frame_range[1]-action.frame_range[0], out)
    out.write(",")
    out.write('"curves":[\n')
    _ea_export_curves(action, out)
    out.write(']\n')
    out.write("}\n")
    out.close()
    return

