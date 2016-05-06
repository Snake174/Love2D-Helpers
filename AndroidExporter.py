# -*- coding: UTF-8 -*-

from Exporter import *

class AndroidExporter( Exporter ):
  def __init__( self ):
    Exporter.__init__( self )

  def buildFile( self, srcDir ):
    pass

  def run( self ):
    projectSourceDir = self.projectsDir + self.currentProjectName + self.DS + 'source' + self.DS
    projectBuildDir = self.projectsDir + self.currentProjectName + self.DS + 'build' + self.DS + 'android' + self.DS

    versions = [ '2.3.3', '3.1', '4.0.3' ]

    for v in versions:
      projectBuildDirV = projectBuildDir + v

      try:
        shutil.rmtree( projectBuildDirV )
      except:
        pass

      os.makedirs( projectBuildDirV )

    print('Android Exporter - OK')
