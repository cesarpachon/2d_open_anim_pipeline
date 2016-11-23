# 2d_open_anim_pipeline
experiments on exporting 2d animations from gimp/blender into cocos2d javascript

The goal is to learn how to  implement a complete pipeline based on opensource tools, that allows the following workflow: 

GIMP side: 
- create a master Gimp file with the sprites as layers.
- export the whole image to be used as atlas.
- export metadata as JSON with the layer list and positions within the atlas.

BLENDER side: 
- import the metadata and create textured quads using the atlas. 
- allow to animate that quads using blender tools.
- export the animated sprites as another json file.

COCOS2D-JS side:
-load the atlas png and atlas json definition, load the json animation
- implement a basic runtime to execute the animation inside the engine.


##current status: 
The Gimp folder contains the export_layers_as_json.py file. it is a gimp plug-in written in python that generates a json with the list of layers and its positions.

currently working on the blender script to import the layer info. 

