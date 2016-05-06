# -*- coding: UTF-8 -*-

from Exporter import *

INFO_PLIST = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>BuildMachineOSBuild</key>
  <string>13D65</string>
  <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleDocumentTypes</key>
    <array>
      <dict>
        <key>CFBundleTypeIconFile</key>
        <string>game.icns</string>
        <key>CFBundleTypeName</key>
        <string>###GAME_TITLE###</string>
        <key>CFBundleTypeRole</key>
        <string>Viewer</string>
        <key>LSHandlerRank</key>
        <string>Owner</string>
        <key>LSItemContentTypes</key>
        <array>
          <string>org.love2d.love-game</string>
		</array>
	  </dict>
	  <dict>
		<key>CFBundleTypeName</key>
		<string>Folder</string>
		<key>CFBundleTypeOSTypes</key>
		<array>
		  <string>fold</string>
		</array>
		<key>CFBundleTypeRole</key>
		<string>Viewer</string>
		<key>LSHandlerRank</key>
		<string>None</string>
	  </dict>
	</array>
	<key>CFBundleExecutable</key>
	<string>love</string>
	<key>CFBundleIconFile</key>
	<string>game.icns</string>
	<key>CFBundleIdentifier</key>
	<string>snake174.github.io</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>game.love</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>0.10.1</string>
	<key>CFBundleSignature</key>
	<string>LoVe</string>
	<key>DTCompiler</key>
	<string>com.apple.compilers.llvm.clang.1_0</string>
	<key>DTPlatformBuild</key>
	<string>5B1008</string>
	<key>DTPlatformVersion</key>
	<string>GM</string>
	<key>DTSDKBuild</key>
	<string>13C64</string>
	<key>DTSDKName</key>
	<string>macosx10.9</string>
	<key>DTXcode</key>
	<string>0511</string>
	<key>DTXcodeBuild</key>
	<string>5B1008</string>
	<key>LSApplicationCategoryType</key>
	<string>public.app-category.games</string>
	<key>NSHumanReadableCopyright</key>
	<string>Burlachenko Maxim & Serebryannikov Evgeniy</string>
	<key>NSPrincipalClass</key>
	<string>NSApplication</string>
</dict>
</plist>
'''

class MacExporter( Exporter ):
  def __init__( self ):
    Exporter.__init__( self )

  def buildFile( self, srcDir ):
    zf = zipfile.ZipFile( self.sdkDir + '0.10.1-macosx-x64.zip', 'r' )
    zf.extractall( srcDir )
    zf.close()

    os.chdir( srcDir )
    shutil.move( 'love.app', 'game.app' )

    with open( 'game.app' + self.DS + 'Contents' + self.DS + 'Info.plist', 'w' ) as f:
      f.writelines( INFO_PLIST.replace( '###GAME_TITLE###', self.currentProjectName ) )

    self.makeIcon(
      self.addDS( self.toolsDir ) + 'icon.png',
      'game.app' + self.DS + 'Contents' + self.DS + 'Resources' + self.DS + 'game.icns',
      144
    )

    shutil.move( 'game.love', 'game.app'  + self.DS + 'Contents' + self.DS + 'Resources' )

  def run( self ):
    projectSourceDir = self.projectsDir + self.currentProjectName + self.DS + 'source' + self.DS
    projectBuildDir = self.projectsDir + self.currentProjectName + self.DS + 'build' + self.DS + 'macosx' + self.DS

    try:
      shutil.rmtree( projectBuildDir )
    except:
      pass

    os.makedirs( projectBuildDir )

    self.makeLoveFile( projectSourceDir, projectBuildDir )
    self.buildFile( projectBuildDir )

    print('Mac OS X Exporter - OK')
