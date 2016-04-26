local pairs = pairs

local Scene = Class {
  init = function( self, o )
    local o = o or {}
    self.layers = {}
    self.layersInfo = {}
    self.preview = nil

    if o.preview then
      self.preview = love.graphics.newImage( o.preview )
    end
  end,

  draw = function( self )
    for layName, _ in pairs( self.layers ) do
      if self.layersInfo[ layName ].draw then
        for i = 1, #self.layers[ layName ].gameObjects do
          self.layers[ layName ].gameObjects[i]:draw()
        end
      end
    end
  end,

  update = function( self, dt )
    for layName, _ in pairs( self.layers ) do
      if self.layersInfo[ layName ].update then
        for i = 1, #self.layers[ layName ].gameObjects do
          self.layers[ layName ].gameObjects[i]:update( dt )
        end
      end
    end
  end,

  enter = function( self )
  end,

  leave = function( self )
  end,

  getPreview = function( self )
    return self.preview
  end,

  addLayer = function( self, layName )
    self.layers[ layName ] = {}
    self.layers[ layName ].gameObjects = {}
    self:setLayerInfo( layName, true, true )
  end,

--[[
Информация о слое

layName - название слоя
isDraw - нужно ли отображать все объекты на слое
isUpdate - нужно ли обновлять все объекты на слое
]]
  setLayerInfo = function( self, layName, isDraw, isUpdate )
    if self.layers[ layName ] then
      self.layersInfo[ layName ] = {
	      draw = isDraw,
		    update = isUpdate
	    }
    end
  end,

--[[
Добавление объекта на слой

go - объект
layName - название слоя (по умолчанию "main")

Пример:
local btn = Button:new( { ... } )
self:add( btn ) -- будет добавлен объект btn на слой с названием "main"
self:add( btn, "gui" ) -- будет добавлен объект btn на слой с названием "gui"
]]
  add = function( self, go, layName )
    local layerName = layName or "main"

    if not self.layers[ layerName ] then
      self:addLayer( layerName )
    end

    self.layers[ layerName ].gameObjects[ #self.layers[ layerName ].gameObjects + 1 ] = go
  end,

--[[
Удаление объекта со слоя
]]
  remove = function( self, go, layName )
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
}

return Scene
