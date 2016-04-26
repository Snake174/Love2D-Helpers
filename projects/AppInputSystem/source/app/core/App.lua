App = {
  OS      = love.system.getOS(),
  WIDTH   = love.graphics.getWidth(),
  HEIGHT  = love.graphics.getHeight(),
  SCALE   = 1,
  SCALE_T = 0,
  RUNNING = true
}

-- Система ввода
Input = {
  _keys     = {},
  _buttons  = {},
  _wheel    = 0,
  _mousePos = Vector( 0, 0 )
}

function App.run()
  local mouseX, mouseY = love.mouse.getPosition()
  Input._mousePos = Vector( mouseX, mouseY )

  if love.event then
    love.event.pump()

    local _keys = {}
    local _btns = {}

    for name, a, b, c, d, e, f in love.event.poll() do
      if name == "quit" then
        App.RUNNING = false
      elseif name == "keypressed" then
        Input._keys[a] = 1
        _keys[a] = true
      elseif name == "keyreleased" then
        Input._keys[a] = 0
        _keys[a] = true
      elseif name == "mousepressed" then
        Input._buttons[c] = 1
        _btns[c] = true
      elseif name == "mousereleased" then
        Input._buttons[c] = 0
        _btns[c] = true
      elseif name == "wheelmoved" then
        Input._wheel = b
      elseif name == "resize" then
        if App.HEIGHT > App.WIDTH then
          App.SCALE = b / App.HEIGHT
          App.SCALE_T = 1
        else
          App.SCALE = a / App.WIDTH
          App.SCALE_T = 0
        end
      end

      local iKeys = Input._keys

      for key, value in pairs( iKeys ) do
        if value == 0 and not _keys[ key ] then
          Input._keys[ key ] = -1
        elseif value == 1 and not _keys[ key ] then
          Input._keys[ key ] = 2
        end
	    end

      local iButtons = Input._buttons

      for key, value in pairs( iButtons ) do
        if value == 0 and not _btns[ key ] then
          Input._buttons[ key ] = -1
        elseif value == 1 and not _btns[ key ] then
          Input._buttons[ key ] = 2
        end
	    end

      love.handlers[ name ]( a, b, c, d, e, f )
    end
  end

  return App.RUNNING
end

function App.close()
  App.RUNNING = false
end

function App.toggleFullScreen()
  if love.window.getFullscreen() == false then
		love.window.setFullscreen( true, "exclusive" )
	else
    love.window.setMode(
      App.WIDTH,
      App.HEIGHT,
      {
        fullscreen = false,
        fullscreentype = "exclusive",
        resizable = false,
        vsync = true,
        centered = true
      }
    )
	end
end

-- >> INPUT
function Input.reset()
  Input._wheel = 0
end

function Input.pressed()
  for _, v in pairs( Input._keys ) do
    if v > 0 then
      return true
    end
  end

  return false
end

function Input.clicked()
  for _, v in pairs( Input._buttons ) do
    if v > 0 then
      return true
    end
  end

  return false
end

function Input.keyDown( key )
  return Input._keys[ key ] == 1
end

function Input.keyUp( key )
  return Input._keys[ key ] == 0
end

function Input.keyHeld( key )
  return Input._keys[ key ] == 2
end

function Input.mouseDown( button )
  return Input._buttons[ button ] == 1
end

function Input.mouseUp( button )
  return Input._buttons[ button ] == 0
end

function Input.mouseHeld( button )
  return Input._buttons[ button ] == 2
end

function Input.wheelUp()
  return Input._wheel == 1
end

function Input.wheelDown()
  return Input._wheel == -1
end

function Input.mousePos()
  return Input._mousePos
end
-- << INPUT

return App
