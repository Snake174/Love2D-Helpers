# -*- coding: UTF-8 -*-

from Exporter import *

class WindowsExporter( Exporter ):
  def __init__( self ):
    Exporter.__init__( self )

  def buildFile( self, srcDir ):
    zf = None

    if srcDir.endswith('x86'):
      zf = zipfile.ZipFile( self.sdkDir + '0.10.1-windows-x86.zip', 'r' )
    else:
      zf = zipfile.ZipFile( self.sdkDir + '0.10.1-windows-x64.zip', 'r' )

    zf.extractall( srcDir )
    zf.close()

    #self.makeIcon( self.addDS( self.toolsDir ) + 'icon.png', self.addDS( srcDir ) + 'icon.ico', 144 )

    os.chdir( srcDir )
    os.system('copy /b love.exe + game.love game.exe')
    os.remove('love.exe')
    os.remove('game.love')

    os.chdir( self.toolsDir )
    #os.system('RCEDIT64.exe /I ' + self.addDS( srcDir ) + 'game.exe ' + self.addDS( srcDir ) + 'icon.ico')
    #os.remove( self.addDS( srcDir ) + 'icon.ico' )
    os.system('upx.exe -qf --best --ultra-brute ' + self.addDS( srcDir ) + 'game.exe')

  def run( self ):
    projectSourceDir = self.projectsDir + self.currentProjectName + self.DS + 'source' + self.DS
    projectBuildDir = self.projectsDir + self.currentProjectName + self.DS + 'build' + self.DS

    x86 = projectBuildDir + 'windows' + self.DS + 'x86'
    x64 = projectBuildDir + 'windows' + self.DS + 'x64'

    try:
      shutil.rmtree( x86 )
      shutil.rmtree( x64 )
    except:
      pass

    os.makedirs( x86 )
    os.makedirs( x64 )

    self.makeLoveFile( projectSourceDir, x86, True )
    self.buildFile( x86 )

    self.makeLoveFile( projectSourceDir, x64, True )
    self.buildFile( x64 )

    print('Windows Exporter - OK')
