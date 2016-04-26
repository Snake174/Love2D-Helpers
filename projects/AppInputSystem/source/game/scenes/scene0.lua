local Scene = require "app.core.components.Scene"

local scene0 = Class {
  __includes = Scene,

  init = function( self, o )
    Scene.init( self, o )

    self.inftab06 = InfoBox:create( Vector( 0, -107 ) )

    self.inftab06:addInfo( "dialog1", self.RC.img.ttsl_005_sc0080_d01 )
    self.inftab06:addInfo( "dialog2", self.RC.img.ttsl_005_sc0080_d02 )

    self.inftab06:setOkImage( self.RC.img.ok02, self.RC.img.ok02_hover )
    self.inftab06:setNextImage( self.RC.img.next02, self.RC.img.next02_hover )
    self.inftab06:setPrevImage( self.RC.img.prev02, self.RC.img.prev02_hover )

    self.inftab06:onOkClick(
      "dialog1",
      function()
        self.inftab06:slide( 0, -107, 1.0, "backout" )
      end
    )

  	self.inftab06:onOkClick(
      "dialog2",
      function()
        self.inftab06:slide( 0, -107, 1.0, "backout" )
      end
    )

    self.inftab06:slide( 0, 0, 1.0, "backout" )

    self:add( self.inftab06 )
  end
}

return scene0
