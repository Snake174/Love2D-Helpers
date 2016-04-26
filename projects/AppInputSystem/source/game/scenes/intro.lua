local Scene = require "app.core.components.Scene"

local intro = Class {
  __includes = Scene,

  init = function( self, o )
    Scene.init( self, o )
 
    self.btnStart = Button:new( {
      pos = Vector( 200, 200 ),
      img = self.RC.img.start_n,
      imgH = self.RC.img.start_nn,
      alpha = true
    } )

    self.btnHelp = Button:new( {
      pos = Vector( 200, 350 ),
      img = self.RC.img.pom_n,
      imgH = self.RC.img.pom_nn,
      alpha = false,
      onClick = function()
        SceneManager.change( SceneManager.scenes.scene0 )
      end
    } )

    self:add( self.btnStart )
    self:add( self.btnHelp )
  end
}

return intro
