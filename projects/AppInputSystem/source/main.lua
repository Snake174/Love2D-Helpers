require "app"

function love.load()
  -- изображение
  mac = love.graphics.newImage("data/mac.png")

  -- размер изображения
  size = Vector( mac:getWidth(), mac:getHeight() )

  -- координаты
  pos = Vector( 320, 240 )

  -- текущий угол поворота
  angle = 0

  inftab06 = InfoBox:create( Vector( 0, -107 ) )

  inftab06:addInfo( "dialog1", "data/ttsl_005_sc0080_d01.png")
  inftab06:addInfo( "dialog2", "data/ttsl_005_sc0080_d02.png")

  inftab06:setOkImage( "data/ok02.png", "data/ok02_hover.png" )
  inftab06:setNextImage( "data/next02.png", "data/next02_hover.png" )
  inftab06:setPrevImage( "data/prev02.png", "data/prev02_hover.png" )

  inftab06:onOkClick(
    "dialog1",
    function()
      inftab06:slide( 0, -107, 2.0, "backout" )
    end
  )

	inftab06:onOkClick(
    "dialog2",
    function()
      inftab06:slide( 0, -107, 2.0, "backout" )
    end
  )

  inftab06:slide( 0, 0, 2.0, "backout" )

  btn = Button:new( {
    pos = Vector( 200, 400 ),
    img = "data/osmotr_ok.png",
    imgH = "data/osmotr_ok_hover.png"
  } )
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

  while App.run() do
    love.timer.step()
    local dt = love.timer.getDelta()
    Timer.update( dt )
    Flux.update( dt )

    -- update
    if Input.keyDown("escape") then
      App.close()
    end

    if Input.keyDown("f") then
      App.toggleFullScreen()
    end

    local mousePos = Input.mousePos()
	  local dir = pos - mousePos

    angle = -math.atan2( dir.x, dir.y ) / (math.pi / 180)

    inftab06:update( dt )

    btn:update( dt )

    love.graphics.clear()
    love.graphics.origin()

    -- draw
    love.graphics.draw( mac,
			                  pos.x,
												pos.y,
												math.rad( angle ),
												1,
												1,
												size.x / 2,
												size.y / 2
                      )

    btn:draw()

    if Input.keyHeld("p") then
      love.graphics.print( "P is holded", 100, 100 )
    end

    Input.reset()

    inftab06:draw()

    love.graphics.present()

    love.timer.sleep( 0.001 )
	end
end
