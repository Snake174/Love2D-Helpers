require "app"

function love.load()
  Cursor.useSystem( false )
  --cursor = love.mouse.newCursor( "data/blank.png", 8, 8 )
  --love.mouse.setCursor( cursor )

  cr = Animation:new( {
    pos = Vector( 400, 400 ),
    img = "data/cursors.png",
    rows = 6,
    cols = 8
  } )
  cr:add( "pointer", "1-8", 2, 0.1 )

  Cursor.add( "pointer", cr )

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
      inftab06:slide( 0, -107, 1.0, "backout" )
    end
  )

	inftab06:onOkClick(
    "dialog2",
    function()
      inftab06:slide( 0, -107, 1.0, "backout" )
    end
  )

  inftab06:slide( 0, 0, 1.0, "backout" )

  str = "Button test"
  i = 0

  btn = Button:new( {
    pos = Vector( 200, 400 ),
    img = "data/osmotr_ok.png",
    imgH = "data/osmotr_ok_hover.png",
    alpha = false
  } )

  btn:mouseIn(
    function()
      str = "MOUSE IN"
    end
  )

  btn:mouseOut(
    function()
      str = "MOUSE OUT"
    end
  )

  btn:click(
    function()
      i = i + 1
      str = "CLICKED " .. tostring(i)
    end
  )

  anim = Animation:new( {
    pos = Vector( 400, 400 ),
    img = "data/coin-sprite-animation-sprite-sheet.png",
    rows = 1,
    cols = 10
  } )
  anim:add( "iddle", "1-10", 1, 0.1 )

  hero = Animation:new( {
    pos = Vector( 500, 400 ),
    img = "data/T_Vlad_Sword_Walking_48x48.png",
    rows = 8,
    cols = 8
  } )
  hero:add( "right", "1-8", 1, 0.1 )
  hero:add( "up", "1-8", 2, 0.1 )
  hero:add( "up-right", "1-8", 3, 0.1 )
  hero:add( "up-left", "1-8", 4, 0.1 )
  hero:add( "down", "1-8", 5, 0.1 )
  hero:add( "down-right", "1-8", 6, 0.1 )
  hero:add( "down-left", "1-8", 7, 0.1 )
  hero:add( "left", "1-8", 8, 0.1 )
  heroWalk = false
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
    Cursor.update( dt )
    Timer.update( dt )
    Flux.update( dt )

    -- update
    if Input.keyDown("escape") then
      App.close()
    end

    if Input.keyDown("f") then
      App.toggleFullScreen()
    end

    if Input.keyHeld("w") then
      if Input.keyHeld("a") then
        hero:change("up-left")
      elseif Input.keyHeld("d") then
        hero:change("up-right")
      else
        hero:change("up")
      end

      heroWalk = true
    end

    local mousePos = Input.mousePos()
	  local dir = pos - mousePos

    angle = -math.atan2( dir.x, dir.y ) / (math.pi / 180)

    inftab06:update( dt )

    btn:update( dt )
    anim:update( dt )
    hero:update( dt )

    if heroWalk then
      hero:resume()
    else
      hero:pause()
    end

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
    anim:draw()
    hero:draw()

    love.graphics.print( str, 200, 370 )

    inftab06:draw()

    Cursor.draw()
    love.graphics.present()
    Input.reset()
    love.timer.sleep( 0.001 )
	end
end
