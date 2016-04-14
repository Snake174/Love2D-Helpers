App = {}

App.OS      = love.system.getOS()
App.WIDTH   = love.graphics.getWidth()
App.HEIGHT  = love.graphics.getHeight()
App.RUNNING = true

-- Система ввода
Input           = {}
Input._keys     = {}
Input._buttons  = {}
Input._wheel    = 0
Input._mousePos = Vector( 0, 0 )

function App.run()
  local mouseX, mouseY  = love.mouse.getPosition()
  Input._mousePos = Vector( mouseX, mouseY )

  if love.event then
    love.event.pump()

    local _keys = {}
    local _btns = {}

    for e, a, b, c, d in love.event.poll() do
      if e == "quit" then
        App.RUNNING = false
      elseif e == "keypressed" then
        Input._keys[a] = 1
        _keys[ #_keys + 1 ] = a
      elseif e == "keyreleased" then
        Input._keys[a] = 0
        _keys[ #_keys + 1 ] = a
      elseif e == "mousepressed" then
        Input._buttons[c] = 1
        _btns[ #_btns + 1 ] = c
        Input.str = a .. " : " .. b .. " : " .. c
      elseif e == "mousereleased" then
        Input._buttons[c] = 0
        _btns[ #_btns + 1 ] = c
      elseif e == "wheelmoved" then
        Input._wheel = b
      end

      for key, value in pairs( Input._keys ) do
        if value == 0 then
          local keyFound = false

          for i = 1, #_keys do
            if _keys[i] == key then
              keyFound = true
              break
            end
          end

          if not keyFound then
            Input._keys[ key ] = -1
          end
        elseif value == 1 then
          local keyFound = false

          for i = 1, #_keys do
            if _keys[i] == key then
              keyFound = true
              break
            end
          end

          if not keyFound then
            Input._keys[ key ] = 2
          end
        end
	    end

      for key, value in pairs( Input._buttons ) do
        if value == 0 then
          local keyFound = false

          for i = 1, #_btns do
            if _btns[i] == key then
              keyFound = true
              break
            end
          end

          if not keyFound then
            Input._buttons[ key ] = -1
          end
        elseif value == 1 then
          local keyFound = false

          for i = 1, #_btns do
            if _btns[i] == key then
              keyFound = true
              break
            end
          end

          if not keyFound then
            Input._buttons[ key ] = 2
          end
        end
	    end

      love.handlers[e]( a, b, c, d )
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
