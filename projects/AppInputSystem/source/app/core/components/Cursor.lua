Cursor = {
  isSystem = true,
  cursors = {},
  cursor = nil,
  hotXY = Vector( 0, 0 )
}

function Cursor.useSystem(v)
  Cursor.isSystem = v
  love.mouse.setVisible(v)

  if v then
    love.mouse.setCursor()
  end
end

function Cursor.add( name, cursor )
  Cursor.cursors[ name ] = cursor
  Cursor.cursor = cursor
  -- cursor = love.mouse.newCursor( filename, hotx, hoty )
  -- love.mouse.setCursor( cursor )
end

function Cursor.change( name )
  if Cursor.cursors[ name ] then
    Cursor.cursor = Cursor.cursors[ name ]
  end
end

function Cursor.draw()
  if not Cursor.isSystem and Cursor.cursor then
    Cursor.cursor:draw()
  end
end

function Cursor.update( dt )
  if not Cursor.isSystem and Cursor.cursor then
    Cursor.cursor:update( dt )
    Cursor.cursor.pos = Input.mousePos() - Cursor.hotXY
  end
end

return Cursor
