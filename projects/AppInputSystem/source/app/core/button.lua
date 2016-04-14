
-- button library

button ={}

function button:create(x,y,image,imagehover)
local t = {}
t.isHover = false
t.x = x
t.y = y
t.image = love.graphics.newImage(image)
t.imagehover = love.graphics.newImage(imagehover)
return setmetatable(t,{__index = self})
end

function button:update(dt)

     local data = self.image:getData()
     self.isHover = false
      --function love.mousepressed(mx, my)
   local mx = love.mouse.getX(); local my = love.mouse.getY()
        if ((mx - self.x) > 0) and ((mx - self.x) <= data:getWidth() - 1) and ((my - self.y) > 0) and ((my - self.y) <= data:getHeight() - 1) then
     self.isHover = true
   --  end

end

   self.isHover = false
   local data = self.image:getData()

     -- local mx, my = love.mouse.getPosition()
   if ((mx - self.x) > 0) and ((mx - self.x) <= data:getWidth() - 1) and ((my - self.y) > 0) and ((my - self.y) <= data:getHeight() - 1) then
      local r, g, b, a = data:getPixel(mx - self.x - 1, my - self.y - 1)
   --loadstring(button.action)()
    click:play()  
   self.isHover = not (a == 0) -- если (a == 0) - прозрачность учитывается
   end
    
end

function button:draw()

   if self.isHover then
      love.graphics.draw(self.imagehover,self.x,self.y) -- кнопка старт- меняется бекграунд кнопки, если над ней курсор
   else
      love.graphics.draw(self.image,self.x,self.y) -- кнопка старт - нормальный бекграунд кнопки, если над ней нет курсора
   end

end

function button:mpress(x,y)
    if self.isHover then
  self.isHover = false
  return true
    end
return false
end