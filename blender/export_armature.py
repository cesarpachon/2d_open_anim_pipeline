#
# exports the active armature and its actions in 
# separated json files
#
import os
import bpy
import json

_ea_name = None
cv_sep = ""

def _ea_write_str(key, val, out):
    out.write('"%s":"%s"\n'%(key, val))
    return

def _ea_write_num(key, val, out):
    out.write('"%s":%s\n'%(key, val))
    return

def _ea_write_vector2(key, val, out):
    out.write('"%s":{"x":%s, "y":%s}\n'%(key, val[0], val[1]))
    return

#
# if here, it means that action.name has the main armature action
# name as prefix = [action].[sprite_name]. this is a convention..
# the curves of sprite actions are just mixed with those of 
# the armature. instead of the "bone" key, we use "sprite" key
# in the json to differentiate.
#
def _ea_export_sprite_curves(action, out):
    global cv_sep
    for curve in action.fcurves:
        tokens = action.name.split(".")
        if len(tokens)!=2:
            print("we expect a [action].[sprite] name of the sprite action, as convention..")
            return
        channel = curve.data_path
        sprite = tokens[1]
        print("exporting sprite curve sprite:%s channel:%s"%(sprite, channel))
        export = 0
        if channel == "hide":
            export = 1
        if export == 0:
            print("skipping unknown channel")
            return
        out.write("%s{\n"%(cv_sep))
        cv_sep = ","
        _ea_write_str("sprite", sprite, out)
        out.write(",")
        _ea_write_str("channel", channel, out)
        out.write(",")
        _ea_write_keyframes(curve, out)
        out.write("}\n")
    return

def _ea_export_curves(action, out):
    global cv_sep
    for curve in action.fcurves:
        print(curve.data_path)
        tokens = curve.data_path.split('"')
        if len(tokens)>1:
            bone = tokens[1]
            channel = curve.data_path.split(".")[2]
        else:
            print("skipping unknown curve: %s in action %s"%(curve.data_path, action.name))
            continue
        
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

        if channel == "rotation_euler" and curve.array_index == 2:
            export = 1
            label = "rot"
        
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
            if channel == "rotation_quaternion":
                print("this version does not support quaternion channels. please animate using euler rotations")

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
        out.write('"pos":{"x": %s, "y": %s},\n'%(bone.head_local[0], bone.head_local[1]))
        out.write('"rot": %s,\n'%(bone.matrix_local.to_euler()[2]))
        out.write('"sprites":[\n')
        _ea_export_sprites(obj, bone, out)
        out.write(']\n')
        out.write("}\n")
    out.write("]\n")
    out.write("}\n")
    out.close()
    return


#the previous line will export the action associated to the armature
#but actions associated to the sprites, like visibility channel,
#can't be accessed that way. 
#we are relying in a Convention Over Configuration rule here:
#let's prefix the actions in the sprites with the name of this action.
#i.e: if "move" is the armature's action, then "move.helix_0" will be understood
#as part of this group. 
def _ea_export_sprite_actions(name, out):
    for action in bpy.data.actions:
        if action.name != name and action.name.startswith(name):
            print("adding sprite action %s"%(action.name))
            _ea_export_sprite_curves(action, out)
        else:
            print("skipping sprite action %s"%(action.name))
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
    _ea_export_sprite_actions(name, out)
    out.write(']\n')
    out.write("}\n")
    out.close()
    return

