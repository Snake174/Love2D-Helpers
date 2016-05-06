# -*- coding: UTF-8 -*-

import os
import zipfile
import shutil
from PyQt4.QtCore import QThread, QDir, QSize, QRect, Qt
from PyQt4.QtGui import QPainter, QImage, QImageWriter

class Exporter( QThread ):
  def __init__( self ):
    QThread.__init__( self )
    self.DS = QDir.separator()
    self.CWD = os.getcwd()
    self.toolsDir = self.addDS( self.CWD ) + 'tools' + self.DS
    self.sdkDir = self.addDS( self.CWD ) + 'SDK' + self.DS
    self.projectsDir = self.addDS( self.CWD ) + 'projects' + self.DS
    self.currentProjectName = ''

    if ' ' in self.toolsDir:
      self.toolsDir = '"' + self.toolsDir + '"'

    if ' ' in self.sdkDir:
      self.sdkDir = '"' + self.sdkDir + '"'

    if ' ' in self.projectsDir:
      self.projectsDir = '"' + self.projectsDir + '"'

  def __del__( self ):
    self.wait()

  def normalizeName( self, value, deletechars ):
    for c in deletechars:
      value = value.replace( c, '' )

    return value;

  def setCurrentProjectName( self, name ):
    self.currentProjectName = self.normalizeName( name, '\\/:*?"\'<>|' )

    if ' ' in self.currentProjectName:
      self.currentProjectName = '"' + self.currentProjectName + '"'

  def addDS( self, srcDir ):
    if srcDir.endswith( self.DS ):
      return srcDir

    return srcDir + self.DS

  def removeBlankLines( self, src ):
    clean_lines = []

    with open( src, 'r' ) as f:
      lines = f.readlines()
      clean_lines = [l.strip() for l in lines if l.strip()]

    with open( src, 'w' ) as f:
      f.writelines( '\n'.join( clean_lines ) )

  def removeSpaces( self, srcDir, isObfuscated ):
    os.chdir( self.toolsDir )

    for dirName, subDirs, files in os.walk( srcDir ):
      for fileName in files:
        absName = os.path.abspath( os.path.join( dirName, fileName ) )

        if absName.lower().endswith('.lua'):
          newName = absName + "___"
          shutil.copy2( absName, newName )
          os.remove( absName )
          os.system( 'lua.exe LuaSrcDiet.lua ' + newName + ' -o ' + absName + ' --quiet --opt-comments --opt-whitespace --opt-emptylines' )
          os.remove( newName )
          self.removeBlankLines( absName )

          if isObfuscated == True:
            os.system( 'luajit.exe -b ' + absName + ' ' + absName )

  def makeLoveFile( self, srcDir, dstDir = '', isObfuscated = False ):
    if srcDir.endswith( self.DS ):
      srcDir = srcDir[:-1]

    newDirName = srcDir + '___'
    shutil.copytree( srcDir, newDirName )
    self.removeSpaces( newDirName, isObfuscated )

    if dstDir == '':
      dstDir = self.addDS( self.CWD )

    loveFile = self.addDS( dstDir ) + 'game.love'
    zf = zipfile.ZipFile( loveFile, 'w', zipfile.ZIP_DEFLATED )
    absSrc = os.path.abspath( newDirName )

    for dirName, subDirs, files in os.walk( newDirName ):
      for fileName in files:
        absName = os.path.abspath( os.path.join( dirName, fileName ) )
        arcName = absName[len( absSrc ) + 1:]
        zf.write( absName, arcName )

    zf.close()

    shutil.rmtree( newDirName )

  def makeIcon( self, src, dst, size ):
    tmpImage = QImage( src )

    iIcon = QImage( QSize( size, size ), QImage.Format_ARGB32 )
    iIcon.fill( Qt.transparent )

    pIcon = QPainter( iIcon )
    pIcon.setRenderHints( QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform )
    pIcon.drawImage( QRect( 0, 0, size, size ), tmpImage, QRect( 0, 0, tmpImage.width(), tmpImage.height() ) )
    pIcon.end()

    wIcon = QImageWriter()
    wIcon.setFileName( dst )
    wIcon.write( iIcon )

  def buildFile( self, srcDir ):
    pass

  def run( self ):
    pass
