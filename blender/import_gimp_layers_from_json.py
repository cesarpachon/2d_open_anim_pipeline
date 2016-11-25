#
# given a json file with GIMP layer information, 
# it will create quads that will match the GIMP image
#
import os
import bpy
import json

_igl_path = None
_igl_name = None
_igl_image = None

def _igl_load_texture(name):
    global _igl_path, _igl_name, _igl_image
    imgpath = _igl_path + name + ".png"
    print("texture path: %s"%(imgpath))
    try:
        _igl_image = bpy.data.images.load(imgpath)
    except:
        raise NameError("Cannot load image %s" % imgpath)
    # Create material
    #_igl_material = bpy.data.materials.new(_igl_name+'_material') # Add texture slot for color texture
    # Create image texture from image
    #cTex = bpy.data.textures.new(_igl_name +'_texture', type = 'IMAGE')
    #cTex.image = img
    #mtex = _igl_material.texture_slots.add()
    #mtex.texture = cTex
    #mtex.texture_coords = 'UV'
    #mtex.use_map_color_diffuse = True 
    #mtex.use_map_color_emission = True 
    #mtex.emission_color_factor = 0.5
    #mtex.use_map_density = True 
    #mtex.mapping = 'FLAT'
    return

def _igl_createTextureLayer(name, me, x, y, w, h, imgw, imgh):
    global _igl_image
    uvtex = me.uv_textures.new()
    uvtex.name = name
    uv_layer = me.uv_layers[0]
    uvtex.data[0].image = _igl_image 
    uvtex.data[1].image = _igl_image 
    #ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)
    u0 = x/imgw
    v0 = (y)/imgh
    u1 = (x+w)/imgw
    v1 = (y-h)/imgh
    print("x %s y %s w %s h %s imgw %s imgh %s"%(x, y, w, h, imgw, imgh))
    print("u0 %s u1 %s v0 %s v1 %s"%(u0, u1, v0, v1))
    uv_layer.data[0].uv = (u0, v1)
    uv_layer.data[1].uv = (u0, v0)
    uv_layer.data[2].uv = (u1, v0)
    uv_layer.data[3].uv = (u1, v0)
    uv_layer.data[4].uv = (u1, v1)
    uv_layer.data[5].uv = (u0, v1)
    return uvtex
 
def _igl_add_sprite(name, x, y, w, h, imgw, imgh):
    global _igl_material
    cx = (x + w)/2
    cy = (y + h)/2
    w2 = w/2
    h2 = h/2
    # Create mesh and object
    me = bpy.data.meshes.new(name+'_mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = (cx, cy, 0)
    # Link object to scene
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    scn.update()

    # List of verts and faces
    verts = [
        (-w2, -h2, 0), 
        (-w2, +h2, 0), 
        (+w2, +h2, 0), 
        (+w2, -h2, 0)
    ]
    faces = [(0,1,2), (2,3,0)]
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, [], faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
 
    # First texture layer: Main UV texture
    uvMain = _igl_createTextureLayer("UVMain", me, x, y, w, h, imgw, imgh)
 
    # Set Main Layer active
    me.uv_textures["UVMain"].active = True
    me.uv_textures["UVMain"].active_render = True
    return

def import_gimp_layers(json_path):
    global _igl_path, _igl_name
    print("json path: %s"%(json_path))
    _igl_name = bpy.path.basename(json_path)
    _igl_path = json_path.replace(_igl_name, "")
    print("base path: %s"%(_igl_path))
    with open(json_path) as data_file:    
        data = json.load(data_file)
        json_img = data["img"]
        print("image: %s w:%s h:%s"%(json_img["name"], json_img["width"],  json_img["height"]))
        imgw = json_img["width"]
        imgh = json_img["height"]
        _igl_load_texture(json_img["name"])
        json_layers = data["layers"]
        for layer in json_layers:
            name = layer["name"]
            x = layer["x"]
            y = layer["y"]
            w = layer["width"]
            h = layer["height"]
            print("layer: %s x:%s y:%s w:%s h:%s "%(name, x, y, w, h))
            _igl_add_sprite(name, x, y, w, h, imgw, imgh)
    return

