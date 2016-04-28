# Love2D-Helpers

**Language:** [RU](README.md) / [EN](README-en.md)

## Description

**Love2D-Helpers** is a set of helper utilities for development on the [Love2D](http://love2d.org/) game engine.
Current supported version is **0.10.1**


## Folder structure

* *projects* - projects folder

The folder structure with the project needs to be next:

**projects/[project-name]/source** - project source files

**projects/[project-name]/build** - binary files will be placed here

**[project-name]** and all the path must be without spaces

* *SDK* - SDK folder

* *tools* - additional utilites


## Scripts

* *Builder.py*

Designed to create binary files for **Windows** and **Mac OS X**

Binary files will be placed to **projects/[project-name]/build** folder.

![Builder.py](/img/Builder.png)


* *AnimationEditor.py*

Intended for help when creating animations. You need to choose a texture atlas and specify the number of frames vertically and horizontally.
Animations are added by allocating the necessary staff. Then specify the name of an animation and the time between frames.
As a result, the script generates a code that you can insert into your project.

Screenshots

![AnimationEditor.py](/img/AnimationEditor_1.png)

![AnimationEditor.py](/img/AnimationEditor_2.png)

![AnimationEditor.py](/img/AnimationEditor_3.png)

![AnimationEditor.py](/img/AnimationEditor_4.png)


* *TexturePackCreator.py*

Designed to create texture atlas from separate images.

![TexturePackCreator.py](/img/TexturePackCreator.png)


The scripts are written in **Python 3** and **PyQt4**. You can download here [Anaconda](https://store.continuum.io/cshop/anaconda/) ([список библиотек](https://docs.continuum.io/anaconda/pkg-docs))

Also for editing projects in Lua you can use editors: [ZeroBrane Studio](https://studio.zerobrane.com/) and [Atom](https://atom.io/) with [love-ide](https://atom.io/packages/love-ide) plugin.
