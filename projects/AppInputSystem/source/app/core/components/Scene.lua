local Scene = {}

function Scene:new(o)
  local o = o or {}
  local info = debug.getinfo( 1, 'S' )
  local t = {}
  t.name = info.source  -- @Scene.lua
  t.layers = {}
  t.layersInfo = {}

  return setmetatable( t, { __index = self } )
end

function Scene:draw()
  for layName, _ in pairs( self.layers ) do
    if self.layersInfo[ layName ][0] then
      for i = 1, #self.layers[ layName ].gameObjects do
        self.layers[ layName ].gameObjects[i]:draw()
      end
    end
  end
end

function Scene:update( dt )
  for layName, _ in pairs( self.layers ) do
    if self.layersInfo[ layName ][1] then
      for i = 1, #self.layers[ layName ].gameObjects do
        self.layers[ layName ].gameObjects[i]:update( dt )
      end
    end
  end
end

function Scene:getName()
  return self.name
end

function Scene:addLayer( layName )
  self.layers[ layName ] = {}
  self.layers[ layName ].gameObjects = {}
  self:setLayerInfo( layName, true, true )
end

function Scene:setLayerInfo( layName, isDraw, isUpdate )
  if self.layers[ layName ] then
    self.layersInfo[ layName ] = { isDraw, isUpdate }
  end
end

function Scene:add( go, layName )
  local layerName = layName or "main"

  if not self.layers[ layerName ] then
    self:addLayer( layerName )
  end

  self.layers[ layerName ].gameObjects[ #self.layers[ layerName ].gameObjects + 1 ] = go
end

function Scene:remove( go, layName )
  if not self.layers[ layName ] then
    return
  end

  for i = 1, #self.layers[ layName ].gameObjects do
    if self.layers[ layName ].gameObjects[i] == go then
      table.remove( self.layers[ layName ].gameObjects, i )
      break
    end
  end
end

return Scene

--[[
NewScene = {}
--наследуемся
setmetatable( NewScene, { __index = Scene } )

newScene = NewScene:new()
]]
