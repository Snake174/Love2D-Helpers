# -*- coding: UTF-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWindow( QMainWindow ):
  def __init__( self, parent = None ):
    QMainWindow.__init__( self, parent )

    self.tools = QDockWidget( 'Tools', self )
    self.tools.setWidget( self.getToolsWidget( self ) )
    self.tools.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )

    self.addDockWidget( Qt.RightDockWidgetArea, self.tools )
    self.setWindowTitle('Texture Pack Creator')

  def getToolsWidget( self, parent ):
    self.toolsWidget = QWidget( parent )
    self.vlToolsWidget = QVBoxLayout( self.toolsWidget )

if __name__ == '__main__':
  app = QApplication( sys.argv )
  QApplication.setStyle( QStyleFactory.create('plastique') )

  w = MainWindow()
  w.show()

  sys.exit( app.exec_() )
