require "app"

function love.load()
  Cursor.useSystem( true )
  SceneManager.change( SceneManager.scenes.intro )
end

function love.run()
	if love.math then
    love.math.setRandomSeed( os.time() )
  end

	if love.event then
    love.event.pump()
  end

	if love.load then
		love.load( arg )
	end

  if not (love.window and love.graphics and love.window.isCreated() and love.timer) then
    return
  end

  love.keyboard.setKeyRepeat( false )

  while App.run() do
    love.timer.step()
    local dt = love.timer.getDelta()

    SceneManager.update( dt )
    Cursor.update( dt )
    Timer.update( dt )
    Flux.update( dt )

    if Input.keyDown("escape") then
      App.close()
    end

    if Input.keyDown("f") then
      App.toggleFullScreen()
    end

    love.graphics.clear()
    love.graphics.origin()

    SceneManager.draw()
    Cursor.draw()

    love.graphics.present()
    Input.reset()
    love.timer.sleep( 0.001 )
	end
end
