# -*- coding: UTF-8 -*-

import sys
import os
import shutil
import queue
from PyQt4.QtGui import (
  QApplication, QWidget, QComboBox, QPushButton, QLineEdit, QLabel, QGridLayout, QToolButton, QFileDialog, QStyleFactory
)
from PyQt4.QtCore import QDir, pyqtSignal, pyqtSlot
from ExportFactory import *

class Builder( QWidget ):
  def __init__( self ):
    QWidget.__init__( self )

    self.queue = queue.Queue()
    self.ef = ExportFactory()
    self.projects = QComboBox( self )

    dirs = next( os.walk( os.getcwd() + QDir.separator() + 'projects' ) )[1]

    for project in dirs:
      self.projects.addItem( project )

    self.icon = QLineEdit( self )

    self.tb = QToolButton( self )
    self.tb.setText('...')
    self.tb.clicked.connect( self.selectIcon )

    self.buildButton = QPushButton( 'Build', self )
    self.buildButton.clicked.connect( self.build )

    self.gl = QGridLayout( self )
    self.gl.addWidget( QLabel( 'Project', self ), 0, 0 )
    self.gl.addWidget( self.projects, 0, 1, 1, 2 )
    self.gl.addWidget( QLabel( 'Icon', self ), 1, 0 )
    self.gl.addWidget( self.icon, 1, 1 )
    self.gl.addWidget( self.tb, 1, 2 )
    self.gl.addWidget( self.buildButton, 2, 0, 1, 3 )

    self.setWindowTitle('Builder')
    self.setFixedSize( self.sizeHint().width(), self.sizeHint().height() )

  @pyqtSlot()
  def selectIcon( self ):
    fileName = QFileDialog.getOpenFileName( self, 'Application Icon', '', 'Image Files (*.png)' )

    if fileName != '':
      self.icon.setText( fileName )

      try:
        shutil.copy2( fileName, os.getcwd() + QDir.separator() + 'tools' + QDir.separator() + 'icon.png' )
      except:
        pass

  @pyqtSlot()
  def build( self ):
    self.buildButton.setEnabled( False )

    we = self.ef.getExporter('windows')
    we.setCurrentProjectName( self.projects.currentText() )
    me = self.ef.getExporter('macosx')
    me.setCurrentProjectName( self.projects.currentText() )
    ae = self.ef.getExporter('android')
    ae.setCurrentProjectName( self.projects.currentText() )

    self.queue.put( we )
    self.queue.put( me )
    self.queue.put( ae )
    self.queue.put( None )

    self.processQueue()

  @pyqtSlot()
  def threadFinished( self ):
    self.queue.task_done()
    self.processQueue()

  def processQueue( self ):
    e = self.queue.get()

    if e is None:
      self.buildButton.setEnabled( True )
    else:
      e.start()
      e.finished.connect( self.threadFinished )

if __name__ == '__main__':
  app = QApplication( sys.argv )
  QApplication.setStyle( QStyleFactory.create('plastique') )

  b = Builder()
  b.show()

  sys.exit( app.exec_() )
