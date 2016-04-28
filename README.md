# Love2D-Helpers

**Language:** [RU](README.md) / [EN](README-en.md)

## Описание

**Love2D-Helpers** представляет собой набор вспомогательных утилит для разработки на игровом движке [Love2D](http://love2d.org/)
Текущая поддерживаемая версия **0.10.1**


## Структура папок

* *projects* - папка с проектами

Структура папки с проектом должна быть следующей:

**projects/[имя-проекта]/source** - исходные файлы проекта

**projects/[имя-проекта]/build** - сюда будут помещаться бинарные файлы

**[имя-проекта]** и все пути должны быть без пробелов

* *SDK* - папка с SDK

* *tools* - вспомогательные утилиты


## Скрипты

* *Builder.py*

Предназначен для создания бинарных файлов для **Windows** и **Mac OS X**

Бинарные файлы помещаются в папку **projects/[имя-проекта]/build**

![Builder.py](/img/Builder.png)


* *AnimationEditor.py*

Предназначен для помощи при создании анимаций. Нужно выбрать текстурный атлас и указать количество кадров по вертикали и горизонтали.
Анимации добавляются путём выделения необходимых кадров. Затем указывается название анимации и время между кадрами.
В результате скрипт генерирует код, который можно будет вставить в свой проект.

Скриншоты

![AnimationEditor.py](/img/AnimationEditor_1.png)

![AnimationEditor.py](/img/AnimationEditor_2.png)

![AnimationEditor.py](/img/AnimationEditor_3.png)

![AnimationEditor.py](/img/AnimationEditor_4.png)


* *TexturePackCreator.py*

Предназначен для создания текстурного атласа из отдельных изображений.

![TexturePackCreator.py](/img/TexturePackCreator.png)


Скрипты написаны на **Python 3** и **PyQt4**. Установщик можно взять здесь [Anaconda](https://store.continuum.io/cshop/anaconda/) ([список библиотек](https://docs.continuum.io/anaconda/pkg-docs))

Также для редактирования проектов на Lua можно использовать редакторы: [ZeroBrane Studio](https://studio.zerobrane.com/) и [Atom](https://atom.io/) с плагином [love-ide](https://atom.io/packages/love-ide)
