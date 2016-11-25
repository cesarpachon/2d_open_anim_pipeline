"use strict";
/**
 * 2D Open Animation Pipeline - cocos2d javascript runtime
 * @author: cesarpachon@gmail.com 
 */
var oap2D = (function(cc){
  var oap2D = {};

  /**
   * @param armature_json_path: path to a oap2D armature json
   * it will be loaded using the cc.loader.
   * the texture referenced by the file is also expected to be reachable
   * through the Cocos2D loader.
   */ 
  oap2D.loadArmature = function(armature_json_path, atlas_json_path){
     var armature_json = cc.loader.getRes(armature_json_path);
     var atlas_json = cc.loader.getRes(atlas_json_path);
     console.log(armature_json);
     console.log(atlas_json);
     var armature = this._initArmature(armature_json);
     this._initSprites(armature, armature_json, atlas_json);
     return armature; 
  };

  /**
   * create a hierarchy of cc.Nodes as bones
   * @return root cc.Node
   */ 
  oap2D._initArmature= function(armature_json){
    var armature = new cc.Node();
    armature.bones = {};
    //init unlinked bones
    armature_json.bones.forEach(function(bone){
      var node = new cc.Node();
      node.name = bone.name;
      node.setPosition(bone.pos);
      node.setRotation(bone.rot);
      armature.bones[node.name] = node; 
    });
    //link bones
    armature_json.bones.forEach(function(bone){
      if(!bone.parent) return;
      var parent = armature.bones[bone.parent];
      parent.addChild(armature.bones[bone.name]); 
    });
    return armature; 
  };

  /**
   * create sprites and attach them to the bones
   */ 
  oap2D._initSprites = function(armature, armature_json, atlas_json){
    armature_json.bones.forEach(function(bone){
      bone.sprites.forEach(function(sprite){
        console.log(sprite);
      });
    });
  };

  return oap2D;
})(cc);
