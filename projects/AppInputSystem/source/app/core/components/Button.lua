local Button = {}

function Button:new(o)
  local t = {}
  t.callbacks = {}
  t.pos = Vector( 0, 0 )
  t.size = Vector( 0, 0 )
  t.img = nil
  t.imgH = nil
  t.data = {}
  t.isHover = false
  t.triggerFlag = false

  if o.pos ~= nil then
    t.pos = o.pos
  end

  if o.size ~= nil then
    t.size = o.size
  end

  if o.img ~= nil then
    t.img = love.graphics.newImage( o.img )
    local data = t.img:getData()
    data:mapPixel(
      function( x, y, r, g, b, a )
        if a == 255 then
          t.data[ tostring(x) .. "-" .. tostring(y) ] = true
        end

        return r, g, b, a
      end
    )
    data = nil
  end

  if o.imgH ~= nil then
    t.imgH = love.graphics.newImage( o.imgH )
  end

  return setmetatable( t, { __index = self } )
end

function Button:draw()
  local img = self.img

  if self.isHover then
    img = self.imgH
  end

  love.graphics.draw(
    img,
    self.pos.x,
    self.pos.y,
    0,
    1,
    1
  )
end

function Button:update( dt )
  local mx, my = Input.mousePos().x - self.pos.x, Input.mousePos().y - self.pos.y

  if self.data[ tostring( mx ) .. "-" .. tostring( my ) ] then
    self.isHover = true
  else
    self.isHover = false
  end

  if self.isHover and not self.triggerFlag then
    self.triggerFlag = true

    if self.callbacks["mousein"] then
      (self.callbacks["mousein"])()
    end
  end
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
