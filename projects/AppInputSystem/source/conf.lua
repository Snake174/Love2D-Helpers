function love.conf(c)
  c.version               = "0.10.1"
  c.title                 = "App"
  c.window.width          = 800
  c.window.height         = 600
  c.window.resizable      = true
  c.window.fullscreen     = false
  c.window.fullscreentype = "exclusive"
  c.window.vsync          = true
  c.window.fsaa           = 4
  c.modules.audio         = true
  c.modules.event         = true
  c.modules.graphics      = true
  c.modules.image         = true
  c.modules.joystick      = false
  c.modules.keyboard      = true
  c.modules.math          = true
  c.modules.mouse         = true
  c.modules.physics       = false
  c.modules.sound         = true
  c.modules.system        = true
  c.modules.timer         = true
  c.modules.window        = true
end
