local InfoBox = {}

function InfoBox:create( pos )
	local t = {}

	t.pos = pos
	t.infos = {}
  t.size = Vector( 0, 0 )
  t.center = Vector( 0, 0 )
  t.scale = Vector( 1, 1 )
  t.size = Vector( 0, 0 )
  t.ang = 0
  t.callbacks = {}

  t.nextImage = nil
  t.nextHoverImage = nil
  t.prevImage = nil
  t.prevHoverImage = nil
  t.okImage = nil
  t.okHoverImage = nil

  t.curNext = nil
  t.curPrev = nil
  t.curOk = nil

  t.drawNext = false
  t.drawPrev = false
  t.drawOk = false

  t.obj = {}
  t.obj.px = pos.x
  t.obj.py = pos.y
  t.obj.alpha = 255

  t.salpha = 255
  t.psx = pos.x
  t.psy = pos.y
  t.slideSpeed = 0
  t.slideEase = "linear"
  t.inProcess = false
  t.process = ""
  t.index = 1
  t.curInfo = ""

  t.cow, t.coh = 0, 0
  t.cnw, t.cnh = 0, 0
  t.cpw, t.cph = 0, 0

  return setmetatable( t, { __index = self } )
end

function InfoBox:draw()
	love.graphics.draw( self.infos[ self.curInfo ].img[ self.index ],
		                  self.pos.x,
											self.pos.y,
											math.rad( self.ang ),
											self.scale.x,
											self.scale.y,
											self.size.x * self.center.x,
											self.size.y * self.center.y
                    )

  if self.drawOk then
    love.graphics.draw( self.curOk,
		                    (self.pos.x + self.size.x * self.scale.x) - self.cow * self.scale.x - 5,
  	  									(self.pos.y + self.size.y * self.scale.y) - self.coh * self.scale.y - 5,
	    									0,
			   								self.scale.x,
				    						self.scale.y,
						    				self.size.x * self.center.x,
								    		self.size.y * self.center.y
                      )
  end

  if self.drawNext then
    love.graphics.draw( self.curNext,
		                    (self.pos.x + self.size.x * self.scale.x) - self.cnw * self.scale.x - self.cow * self.scale.x - 10,
  		  								(self.pos.y + self.size.y * self.scale.y) - self.cnh * self.scale.y - 5,
	  		  							0,
		   		  						self.scale.x,
			    	  					self.scale.y,
					      				self.size.x * self.center.x,
							      		self.size.y * self.center.y
                      )
  end

  if self.drawPrev then
    love.graphics.draw( self.curPrev,
		                    (self.pos.x + self.size.x * self.scale.x) - self.cpw * self.scale.x - self.cnw * self.scale.x - self.cow * self.scale.x - 15,
  		  								(self.pos.y + self.size.y * self.scale.y) - self.cph * self.scale.y - 5,
	  		  							0,
		   		  						self.scale.x,
			    	  					self.scale.y,
					      				self.size.x * self.center.x,
							      		self.size.y * self.center.y
                      )
  end
end

function InfoBox:update( dt )
  if self.inProcess then
    if self.process == "slide" then
      Flux.to( self.obj, self.slideSpeed, { px = self.psx, py = self.psy } )
        :ease( self.slideEase )
        :onupdate( function() self.pos = Vector( self.obj.px, self.obj.py ) end )
        :oncomplete( function()
                       if self.inProcess then
                         if self.callbacks["onEnd"] then
                           self.callbacks["onEnd"]()
                         end

                         self.inProcess = false
                         self.process = ""
                       end
                     end
                    )
    end
  end

  self:updateIndex()

  self:updateOk()
  self:updateNext()
  self:updatePrev()
end

function InfoBox:updateIndex()
  if #self.infos[ self.curInfo ].img > 1 then
    self.drawNext = true
  end

  if self.index == #self.infos[ self.curInfo ].img then
    self.drawNext = false
    self.drawOk = true
  end

  if self.index < #self.infos[ self.curInfo ].img then
    self.drawOk = false
  end

  if self.index == 1 then
    self.drawPrev = false
  end

  if self.index > 1 and #self.infos[ self.curInfo ].img > 1 then
    self.drawPrev = true
  end
end

function InfoBox:checkButtons( btnNum )
  local x, y = Input.mousePos().x, Input.mousePos().y

  if btnNum == 1 then
    local xx = (self.pos.x + self.size.x * self.scale.x) - self.cow * self.scale.x - 5
    local yy = (self.pos.y + self.size.y * self.scale.y) - self.coh * self.scale.y - 5

    if ((x > (xx - self.cow * self.scale.x * self.center.x)) and (x < xx + (self.cow * self.scale.x - self.cow * self.scale.x * self.center.x)))
      and ((y > (yy - self.coh * self.scale.y * self.center.y)) and (y < yy + (self.coh * self.scale.y - self.coh * self.scale.y * self.center.y))) then
      return true
    end
  elseif btnNum == 2 then
    local xx = (self.pos.x + self.size.x * self.scale.x) - self.cnw * self.scale.x - self.cow * self.scale.x - 10
    local yy = (self.pos.y + self.size.y * self.scale.y) - self.cnh * self.scale.y - 5

    if ((x > (xx - self.cnw * self.scale.x * self.center.x)) and (x < xx + (self.cnw * self.scale.x - self.cnw * self.scale.x * self.center.x)))
      and ((y > (yy - self.cnh * self.scale.y * self.center.y)) and (y < yy + (self.cnh * self.scale.y - self.cnh * self.scale.y * self.center.y))) then
      return true
    end
  elseif btnNum == 3 then
    local xx = (self.pos.x + self.size.x * self.scale.x) - self.cpw * self.scale.x - self.cnw * self.scale.x - self.cow * self.scale.x - 15
  	local yy = (self.pos.y + self.size.y * self.scale.y) - self.cph * self.scale.y - 5

    if ((x > (xx - self.cpw * self.scale.x * self.center.x)) and (x < xx + (self.cpw * self.scale.x - self.cpw * self.scale.x * self.center.x)))
      and ((y > (yy - self.cph * self.scale.y * self.center.y)) and (y < yy + (self.cph * self.scale.y - self.cph * self.scale.y * self.center.y))) then
      return true
    end
  end

  return false
end

function InfoBox:updateOk()
  if self:checkButtons(1) then
    self.curOk = self.okHoverImage

    if Input.mouseDown(1) then
      if self.callbacks[ self.curInfo ].onOkClick then
        (self.callbacks[ self.curInfo ].onOkClick)()
      end
    end
  else
    self.curOk = self.okImage
  end
end

function InfoBox:updateNext()
  if self:checkButtons(2) then
    self.curNext = self.nextHoverImage

    if Input.mouseDown(1) then
      if self.index < #self.infos[ self.curInfo ].img then
        self.index = self.index + 1
        self.size = Vector( self.infos[ self.curInfo ].img[ self.index ]:getWidth(), self.infos[ self.curInfo ].img[ self.index ]:getHeight() )
      end
    end
  else
    self.curNext = self.nextImage
  end
end

function InfoBox:updatePrev()
  if self:checkButtons(3) then
    self.curPrev = self.prevHoverImage

    if Input.mouseDown(1) then
      if self.index > 1 then
        self.index = self.index - 1
        self.size = Vector( self.infos[ self.curInfo ].img[ self.index ]:getWidth(), self.infos[ self.curInfo ].img[ self.index ]:getHeight() )
      end
    end
  else
    self.curPrev = self.prevImage
  end
end

function InfoBox:addInfo( info, img )
  if not self.infos[ info ] then
    self.infos[ info ] = {}
    self.infos[ info ].img = {}
  end

  local ind = #self.infos[ info ].img + 1
  self.infos[ info ].img[ ind ] = love.graphics.newImage( img )
  self.size = Vector( self.infos[ info ].img[ ind ]:getWidth(), self.infos[ info ].img[ ind ]:getHeight() )

  self.curInfo = info
  self.index = 1
end

function InfoBox:switch( info )
  if not self.infos[ info ] then
    return
  end

  self.curInfo = info
  self.index = 1
end

function InfoBox:getCurrentInfo()
  return self.curInfo
end

function InfoBox:setNextImage( img, imgh )
  self.nextImage = love.graphics.newImage( img )
  self.nextHoverImage = love.graphics.newImage( imgh )
  self.cnw, self.cnh = self.nextImage:getWidth(), self.nextImage:getHeight()
end

function InfoBox:setPrevImage( img, imgh )
  self.prevImage = love.graphics.newImage( img )
  self.prevHoverImage = love.graphics.newImage( imgh )
  self.cpw, self.cph = self.prevImage:getWidth(), self.prevImage:getHeight()
end

function InfoBox:setOkImage( img, imgh )
  self.okImage = love.graphics.newImage( img )
  self.okHoverImage = love.graphics.newImage( imgh )
  self.cow, self.coh = self.okImage:getWidth(), self.okImage:getHeight()
end

function InfoBox:slide( x, y, speed, ease )
  if self.inProcess then
    return
  end

  self.process = "slide"
  self.psx = x
  self.psy = y
  self.slideSpeed = speed

  if ease then
    self.slideEase = ease
  end

  self.inProcess = true

  if self.callbacks["onStart"] then
    self.callbacks["onStart"]()
  end
end

function InfoBox:setPos( pos )
  self.pos = pos
  self.obj.px = pos.x
  self.obj.py = pos.y
end

function InfoBox:onOkClick( info, func )
  if not self.callbacks[ info ] then
    self.callbacks[ info ] = {}
    self.callbacks[ info ].onOkClick = nil
  end

  self.callbacks[ info ].onOkClick = func
end

function InfoBox:onStart( func )
  self.callbacks["onStart"] = func
end

function InfoBox:onEnd( func )
  self.callbacks["onEnd"] = func
end

return InfoBox
