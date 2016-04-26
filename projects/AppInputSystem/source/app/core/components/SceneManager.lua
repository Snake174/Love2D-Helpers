local setmetatable, require = setmetatable, require

local function getRequireFile( fileName, basePath, validFormats )
  local filePath

  for _, ext in ipairs( validFormats ) do
    filePath = basePath .. fileName .. ext

    if love.filesystem.isFile( filePath ) then
      return string.gsub( basePath .. fileName, "/", "." )
    end
  end

  return nil
end

local function getFilePath( fileName, basePath, validFormats )
  local filePath

  for _, ext in ipairs( validFormats ) do
    filePath = basePath .. fileName .. ext

    if love.filesystem.isFile( filePath ) then
      return filePath
    end
  end
end

local function getFolderTree( baseFolder )
  local tree = { __folder = baseFolder }

  for i, v in ipairs( love.filesystem.getDirectoryItems( baseFolder ) ) do
    if love.filesystem.isDirectory( baseFolder .. v ) then
      tree[v] = getFolderTree( baseFolder .. v .. "/" )
    end
  end

  return tree
end

local baseImgMetatable = {
  __index = function( t, k )
    t[k] = getFilePath( k, t.__folder, { ".png", ".jpg", ".bmp" } )
    return t[k]
  end
}

local baseSndMetatable = {
  __index = function( t, k )
    t[k] = love.audio.newSource( getFilePath( k, t.__folder, { ".ogg", ".wav", ".mp3" } ), "stream" )
    return t[k]
  end,
  __call = function( self, k )
    return self[k]
  end
}

local function setImgMeta(t)
  return setmetatable( t, baseImgMetatable )
end

local function recurseSetImgMeta( base )
  for _, v in pairs( base ) do
    if type(v) == "table" then
      v = recurseSetImgMeta(v)
    end
  end

  return setImgMeta( base )
end

local function setSndMeta(t)
  return setmetatable( t, baseSndMetatable )
end

local function recurseSetSndMeta( base )
  for _, v in pairs( base ) do
    if type(v) == "table" then
      v = recurseSetSndMeta(v)
    end
  end

  return setSndMeta( base )
end

local baseMetatable = {
  __index = function( self, k )
    self[k] = require( getRequireFile( k, "game/scenes/", { ".lua" } ) )
    self[k].RC = {
      img = recurseSetImgMeta( getFolderTree( "game/scenes/" .. tostring(k) .. "/images/" ) ),
      snd = recurseSetSndMeta( getFolderTree( "game/scenes/" .. tostring(k) .. "/sound/" ) )
    }
    return self[k]
  end,
  __call = function( self, k )
    return self[k]
  end
}

local SceneManager = {
  scenes = setmetatable( {}, baseMetatable ),
  curScene = nil,
  nextScene = nil,
  duration = 1,
  effect = "fade",
  inProcess = false
}

function SceneManager.draw()
  if SceneManager.inProcess then
    if SceneManager.nextScene and SceneManager.nextScene:getPreview() then
      love.graphics.draw( SceneManager.nextScene:getPreview(), 0, 0 )
    end
  else
    if SceneManager.curScene then
      SceneManager.curScene:draw()
    end
  end
end

function SceneManager.update( dt )
  if SceneManager.inProcess then
    SceneManager.curScene = SceneManager.nextScene
    SceneManager.nextScene = nil
    SceneManager.inProcess = false
  elseif SceneManager.curScene and not SceneManager.inProcess then
    SceneManager.curScene:update( dt )
  end
end

function SceneManager.change( to, duration, effect )
  --[[SceneManager.nextScene = to
  SceneManager.duration = duration
  SceneManager.effect = effect

  if SceneManager.nextScene.init then
    SceneManager.nextScene:init()
    SceneManager.nextScene.init = nil
  end

  SceneManager.inProcess = true]]

  if to.init then
    to:init()
    to.init = nil
  end

  SceneManager.curScene = to
end

return SceneManager
