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

def _igl_createTextureLayer(name, me):
    global _igl_image
    uvtex = me.uv_textures.new()
    uvtex.name = name
    uv_layer = me.uv_layers[0]
    print(uvtex.data[0])
    print(dir(uvtex.data[0]))
    uvtex.data[0].image = _igl_image 
    uvtex.data[1].image = _igl_image 
    #ob.data.uv_layers.active.data[loop_index].uv = (0.5, 0.5)
    uv_layer.data[0].uv = (0, 1)
    uv_layer.data[1].uv = (0, 0)
    uv_layer.data[2].uv = (1, 0)
    uv_layer.data[3].uv = (1, 0)
    uv_layer.data[4].uv = (1, 1)
    uv_layer.data[5].uv = (0, 1)
    return uvtex
 
def _igl_add_sprite(name, x, y, w, h):
    global _igl_material
    cx = (x + w)/2
    cy = (y + h)/2
    w2 = w/2
    h2 = h/2
    # Create mesh and object
    me = bpy.data.meshes.new(name+'_mesh')
    ob = bpy.data.objects.new(name+'_sprite', me)
    ob.location = (cx, cy, 0)
    # Link object to scene
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    scn.update()

    # List of verts and faces
    verts = [
        (cx-w2, cy+h2, 0), 
        (cx-w2, cy-h2, 0), 
        (cx+w2, cy-h2, 0), 
        (cx+w2, cy+h2, 0)
    ]
    faces = [(0,1,2), (2,3,0)]
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, [], faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
 
    # First texture layer: Main UV texture
    texFaces = [
        [(0,1), (0,0), (1,0)],
        [(1,0), (1,1), (0,1)]
    ]
    uvMain = _igl_createTextureLayer("UVMain", me)
 
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
        _igl_load_texture(json_img["name"])
        json_layers = data["layers"]
        for layer in json_layers:
            name = layer["name"]
            x = layer["x"]
            y = layer["y"]
            w = layer["width"]
            h = layer["height"]
            print("layer: %s x:%s y:%s w:%s h:%s "%(name, x, y, w, h))
            _igl_add_sprite(name, x, y, w, h)
    return

