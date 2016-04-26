local Scene = require "app.core.components.Scene"

local scene1 = Class {
  __includes = Scene,

  init = function( self, o )
    Scene.init( self, o )
    
    self.anim = Animation:new( {
      pos = Vector( 200, 200 ),
      img = self.RC.img.coin_sprite_animation,
      rows = 1,
      cols = 10
    } )
    self.anim:add( "iddle", "1-10", 1, 0.1 )
    
    self:add( self.anim )
  end
}

return scene1
