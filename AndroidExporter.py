# -*- coding: UTF-8 -*-

from Exporter import *
import multiprocessing

class AndroidExporter( Exporter ):
  def __init__( self ):
    Exporter.__init__( self )

  def buildFile( self, srcDir ):
    os.chdir( self.makePath( [ self.sdkDir, 'android-ndk-r9d' ] ) )
    os.environ['JAVA_HOME'] = self.makePath( [ self.sdkDir, 'jdk-8u73' ] )
    os.environ['ANT_HOME'] = self.makePath( [ self.sdkDir, 'apache-ant-1.9.7' ] )
    os.environ['ANDROID_NDK'] = self.makePath( [ self.sdkDir, 'android-ndk-r9d' ] )
    os.environ['ANDROID_SDK'] = self.makePath( [ self.sdkDir, 'android-sdk-windows' ] )
    os.environ['ANDROID_HOME'] = self.makePath( [ self.sdkDir, 'android-sdk-windows' ] )
    os.environ['ANDROID_SWT'] = self.makePath( [ self.sdkDir, 'android-sdk-windows', 'tools', 'lib', 'x86' ] )
    os.environ['PATH'] = ';'.join( [ os.environ.get( 'PATH', '' ), '%JAVA_HOME%', '%ANDROID_SDK%\tools', '%ANDROID_NDK%', '%ANT_HOME%\bin' ] )
    os.system( self.makePath( [ self.sdkDir, 'android-ndk-r9d', 'ndk-build.cmd' ] ) + ' --jobs ' + str( multiprocessing.cpu_count() + 1 ) + ' -C ' + srcDir )
    os.chdir( srcDir )
    os.system( self.makePath( [ self.sdkDir, 'apache-ant-1.9.7', 'bin', 'ant' ] ) + ' release' )

  def run( self ):
    projectSourceDir = self.makePath( [ self.projectsDir, self.currentProjectName, 'source' ] )
    projectBuildDir = self.makePath( [ self.projectsDir, self.currentProjectName, 'build', 'androidb' ] )
    projectReleaseDir = self.makePath( [ self.projectsDir, self.currentProjectName, 'build', 'android' ] )

    try:
      shutil.rmtree( projectBuildDir )
      shutil.rmtree( projectReleaseDir )
    except:
      pass

    os.makedirs( projectBuildDir )
    os.makedirs( projectReleaseDir )

    zf = zipfile.ZipFile( self.sdkDir + '0.10.1-android.zip', 'r' )
    zf.extractall( projectBuildDir )
    zf.close()

    sizes = { 
      'drawable-mdpi': 48, 
      'drawable-hdpi': 72, 
      'drawable-xhdpi': 96, 
      'drawable-xxhdpi': 144, 
      'drawable-xxxhdpi': 192 
    }

    for f, s in sizes.items():
      self.makeIcon( self.makePath( [ self.toolsDir, 'icon.png' ] ), self.makePath( [ projectBuildDir, 'res', f, 'love.png' ] ), s )

    self.makeLoveFile( projectSourceDir, self.makePath( [ projectBuildDir, 'assets' ] ), True )
    self.buildFile( projectBuildDir )

    try:
      shutil.move( 
        self.makePath( [ projectBuildDir, 'bin', 'love-android-release-unsigned.apk' ] ), 
        self.makePath( [ projectReleaseDir, 'game.apk' ] ) 
      )
      shutil.rmtree( projectBuildDir )
    except:
      pass

    print('Android Exporter - OK')
