local Anim = require "app.core.anim8.anim8"
local Animation = {}

function Animation:new(o)
  local o = o or {}
  local t = {}
  t.pos = Vector( 0, 0 )
  t.img = nil
  t.grid = nil
  t.anims = {}
  t.anim = nil

  if o.pos then
    t.pos = o.pos
  end

  if o.img then
    t.img = love.graphics.newImage( o.img )
    local w, h = t.img:getWidth(), t.img:getHeight()
    local rows, cols = 1

    if o.rows then
      rows = o.rows
    end

    if o.cols then
      cols = o.cols
    end

    t.grid = Anim.newGrid( w / cols, h / rows, w, h )
  end

  return setmetatable( t, { __index = self } )
end

function Animation:draw()
  if self.anim then
    self.anim:draw( self.img, self.pos.x,	self.pos.y )
  end
end

function Animation:update( dt )
  if self.anim then
    self.anim:update( dt )
  end
end

function Animation:add( name, frames, row, t )
  if self.grid then
    self.anims[ name ] = Anim.newAnimation( self.grid( frames, row ), t )
  end
end

function Animation:change( name )
  if self.anims[ name ] then
    self.anim = self.anims[ name ]
  end
end

function Animation:flipV()
  if self.anim then
    self.anim:flipV()
  end
end

function Animation:flipH()
  if self.anim then
    self.anim:flipH()
  end
end

function Animation:pause()
  if self.anim then
    self.anim:pause()
  end
end

function Animation:resume()
  if self.anim then
    self.anim:resume()
  end
end

return Animation
