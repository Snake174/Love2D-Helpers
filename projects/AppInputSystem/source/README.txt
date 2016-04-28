Базовая заготовка для создания игр.

Структура:
  app/     - папка с движком игры
  game/    - папка для ресурсов игры
  conf.lua - файл с настройками игры
  main.lua - главный файл игры



Доступные компоненты:
1) App - главный объект приложения

Константы:
string App.OS    - текущая ОС
int App.WIDTH    - ширина окна (настраивается в conf.lua)
int App.HEIGHT   - высота окна (настраивается в conf.lua)
bool App.RUNNING - запущено приложение или нет (в явном виде не используется)

Функции:
bool App.run()              - запуск игрового цикла
void App.close()            - выход
void App.toggleFullScreen() - переключение в полноэкранный режим и обратно

Примеры:

-- Init resources
...

while App.run() do
  if Input.keyDown("escape") then
    App.close()
  end

  if Input.keyDown("f") then
    App.toggleFullScreen()
  end
end

-- Free resources
...


2) Input - ввод с клавиатуры и мыши

Функции:
bool Input.pressed()           - была ли нажата какая-либо клавиша на клавиатуре
bool Input.clicked()           - была ли нажата какая-либо кнопка мыши
bool Input.keyDown( key )      - одиночное нажатие клавиши key на клавиатуре
bool Input.keyUp( key )        - клавиша key была отпущена
bool Input.keyHeld( key )      - клавиша key была нажата и удерживается
bool Input.mouseDown( button ) - одиночное нажатие кнопки button на мыши
bool Input.mouseUp( button )   - кнопка button была отпущена
bool Input.mouseHeld( button ) - кнопка button была нажата и удерживается
bool Input.wheelUp()           - колёсико мыши было прокручено вверх
bool Input.wheelDown()         - колёсико мыши было прокручено вниз
Vector Input.mousePos()        - координаты мыши

Примеры: смотри выше


2) Button - кнопка. Также может служить в роли хотспота.

Функции:
Button Button:new(o)    - создание новой кнопки
void Button:setAlpha(a) - установить реагирование на прозрачность (true/false)
void Button:click(f)    - установить функцию f в качестве коллбэка при клике
void Button:mouseIn(f)  - установить функцию f в качестве коллбэка наведении мыши
void Button:mouseOut(f) - установить функцию f в качестве коллбэка при уходе курсора мыши с кнопки

Примеры:

btn = Button:new( {
  pos = Vector( 0, 0 ),   - координаты кноки
  img = "",               - изображение
  imgH = "",              - изображение при наведении мыши
  alpha = true,           - реагировать на прозрачность
  onMouseIn = function()  - функция при наведении мыши
  end,
  onMouseOut = function() - функция при уходе курсора мыши с кнопки
  end,
  onClick = function()    - функция при клике
  end
} )


3) Animation - анимация

Функции:
Animation Animation:new(o)                - создание новой анимации
void Animation:add( name, cols, rows, t ) - добавить анимацию
void Animation:change( name )             - сменить анимацию на name
void Animation:flipV()                    - отразить по вертикали
void Animation:flipH()                    - отразить по горизонтали
void Animation:pause()                    - приостановить проигрывание
void Animation:resume()                   - возобновить проигрывание

Примеры:

anim = Animation:new( {
  pos = Vector( 0, 0 ),  - координаты
  img = "",              - текстурный атлас
  rows = 1,              - количество кадров по вертикали
  cols = 10              - количество кадров по горизонтали
} )

-- добавление анимации с названием "iddle". Изображения с 1 по 10 столбец в первой строке.
-- время между сменой кадров 0.1 секунда
anim:add( "iddle", "1-10", 1, 0.1 )
