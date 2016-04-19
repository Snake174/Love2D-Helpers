local Button = {}

function Button:new(o)
  local o = o or {}
  local t = {}
  t.callbacks = {}
  t.pos = Vector( 0, 0 )
  t.size = Vector( 0, 0 )
  t.img = nil
  t.imgH = nil
  t.data = {}
  t.isHover = false
  t.isAlpha = false
  t.triggerInOut = false
  t.triggerClick = false

  if o.pos then
    t.pos = o.pos
  end

  if o.alpha then
    t.isAlpha = o.alpha
  end

  if o.img then
    t.img = love.graphics.newImage( o.img )
    t.size = Vector( t.img:getWidth(), t.img:getHeight() )
    local data = t.img:getData()
    data:mapPixel(
      function( x, y, r, g, b, a )
        if a > 0 then
          t.data[ tostring(x) .. "-" .. tostring(y) ] = true
        end

        return r, g, b, a
      end
    )
    data = nil
  end

  if o.imgH then
    t.imgH = love.graphics.newImage( o.imgH )
  end

  if o.onClick then
    t.callbacks["click"] = o.onClick
  end

  if o.onMouseIn then
    t.callbacks["mousein"] = o.onMouseIn
  end

  if o.onMouseOut then
    t.callbacks["mouseout"] = o.onMouseOut
  end

  return setmetatable( t, { __index = self } )
end

function Button:draw()
  local img = self.img

  if self.isHover then
    img = self.imgH
  end

  if img then
    love.graphics.draw( img, self.pos.x, self.pos.y )
  end
end

function Button:update( dt )
  local mx, my = Input.mousePos().x - self.pos.x, Input.mousePos().y - self.pos.y

  if self.isAlpha then
    if self.data[ tostring( mx ) .. "-" .. tostring( my ) ] then
      self.isHover = true
    else
      self.isHover = false
    end
  else
    if mx > 0 and mx < self.size.x and my > 0 and my < self.size.y then
      self.isHover = true
    else
      self.isHover = false
    end
  end

  if self.isHover and not self.triggerInOut then
    self.triggerInOut = true

    if self.callbacks["mousein"] then
      (self.callbacks["mousein"])()
    end
  elseif not self.isHover and self.triggerInOut then
    self.triggerInOut = false

    if self.callbacks["mouseout"] then
      (self.callbacks["mouseout"])()
    end
  end

  if self.isHover and not self.triggerClick and Input.mouseDown(1) then
    self.triggerClick = true

    if self.callbacks["click"] then
      (self.callbacks["click"])()
    end
  end

  if Input.mouseUp(1) then
    self.triggerClick = false
  end
end

function Button:setAlpha(a)
  self.isAlpha = a
end

function Button:click(f)
  self.callbacks["click"] = f
end

function Button:mouseIn(f)
  self.callbacks["mousein"] = f
end

function Button:mouseOut(f)
  self.callbacks["mouseout"] = f
end

return Button
