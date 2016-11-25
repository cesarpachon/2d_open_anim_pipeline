"use strict";
/**
 * 2D Open Animation Pipeline - cocos2d javascript runtime
 * @author: cesarpachon@gmail.com 
 */
var oap2D = (function(cc){
  var oap2D = {
    animation_cache: {}
  };

  /**
   * @param armature_json_path: path to a oap2D armature json
   * it will be loaded using the cc.loader.
   * the texture referenced by the file is also expected to be reachable
   * through the Cocos2D loader.
   */ 
  oap2D.loadArmature = function(armature_json_path, atlas_json_path, res_path){
     var armature_json = cc.loader.getRes(armature_json_path);
     var atlas_json = cc.loader.getRes(atlas_json_path);
     console.log(armature_json);
     console.log(atlas_json);
     var armature = this._initArmature(armature_json);
     this._initSprites(armature, armature_json, atlas_json, res_path);
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
    armature.addChild(armature.bones.root);
    return armature; 
  };

  /**
   * create sprites and attach them to the bones
   */ 
  oap2D._initSprites = function(armature, armature_json, atlas_json, res_path){
    var _self = this;
    // a registry of sprites for quick lookup
    armature.sprites = {};
    armature_json.bones.forEach(function(jbone){
      jbone.sprites.forEach(function(jsprite){
        var csprite = _self._initSprite(jsprite, atlas_json, res_path);
        armature.bones[jbone.name].addChild(csprite);
        armature.sprites[jsprite.name] = csprite;
      });
    });
  };

  /**
   * creates a cc.Sprite using the json information
   */ 
  oap2D._initSprite = function(jsprite, atlas_json, res_path){
    var path = res_path + atlas_json.img.name + ".png";
    var layer = atlas_json.layers.find(function(layer){
      return layer.name === jsprite.name; 
    });
    var y = atlas_json.img.height - layer.y;
    var rect = new cc.Rect(layer.x, y, layer.width, layer.height);
    var sprite = cc.Sprite.createWithTexture(path, rect);
    sprite.setPosition(jsprite.pos);
    sprite.setRotation(jsprite.rot);
    return sprite;
  };

  /**
   * load the animation in a module cache
   * @param alias: optional. if found, will be used as key
   * to register the anim in the cache. if not present,
   * the attribute "name" of the animation will be used. 
   * main intention is to avoid clashing names. 
   */ 
  oap2D.loadAnimation= function(animation_json_path, alias){
     var animation_json = cc.loader.getRes(animation_json_path);
     var name = alias?alias:animation_json.name; 
     this.animation_cache[name] = animation_json;
    console.log(animation_json);
  };


  /**
   * returns and cocos action to play the given animation from
   * the oap2D cache. 
   */ 
  oap2D.playAnimation= function(armature, animation_name){
    var action;  
    var anim = this.animation_cache[animation_name];
     if(!anim) throw "oap2D: animation not found in cache";
     var actions = [];
     anim.curves.forEach(function(curve){
      var target;
      if(curve.bone){
        target = armature.bones[curve.bone];
        console.log("target bone " + curve.bone + " channel:"+curve.channel + " " +target);
      }else if(curve.sprite){
        target = armature.sprite[curve.sprite];
        console.log("target sprite " + curve.sprite  + " channel:"+curve.channel+ " " +target);
      }
      if(curve.channel === "pos.x"){
         
      }else if(curve.channel === "pos.y"){
        
      }else if(curve.channel === "rot"){
        action = new oap2D.ActionAnimCurve(target, curve, anim.frames, 5);
        //actions.push(action);
      }else if(curve.channel === "hide"){
        
      }
     });
     return action; 
     //return new cc.Spawn(actions);
  };

  /**
   * we want to override the update mechanism of the original action
   * to apply to any property, not only position
   */ 
  oap2D.ActionAnimCurve = cc.CardinalSplineTo.extend({
    curve: null,

    /*
     * @param frames_len: total number of frames of the action this curve belongs to. 
     *  will be used as the 100% to compute total duration.
     * @fps: used to transform the frame value of keyframes into a absolute time value.
     * */
    ctor: function (target, curve, frames_len, fps/*duration, points, tension*/) {
         cc.CardinalSplineTo.prototype.ctor.call(this);
         this.curve = curve;
         this.oap2d_target = target;
         var duration = frames_len /  fps; 
         var points = [];
         curve.keyframes.forEach(function(keyframe){
          points.push({
            y: keyframe[1],
            x: (keyframe[0]/frames_len) * duration
          });
         });
         var last = points[points.length-1];
         points.push({
           x: duration,
           y: last.y
         });
         console.log(curve.keyframes);
         console.log(points);
         console.log("duration:"+duration);
         this.initWithDuration(duration, points, 0);
     },

    /*
     * this is the key part! override setPosition to affect 
     * the curve's channel.. 
     * */
     updatePosition:function (newPos) {
         //instead of..
         //this.target.setPosition(newPos);
         
         //let's do: 
         if(this.curve.channel === "rot"){
          this.oap2d_target.setRotation(newPos.y); 
         }

         this._previousPosition = newPos;
     },
  });

  return oap2D;
})(cc);
