# -*- coding: UTF-8 -*-

import sys
from enum import Enum
from PyQt4.QtGui import (
  QApplication, QWidget, QListWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QToolButton, QFileDialog,
  QGraphicsView, QGraphicsScene, QPainter, QGraphicsSceneMouseEvent, QBrush, QColor, QPixmap, QPen, QMainWindow,
  QDockWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QSpinBox, QAbstractSpinBox, QStyleFactory, QStyle, QDialog
)
from PyQt4.QtCore import Qt, QDir, QRectF, QPointF, QLineF, QSize, pyqtSignal, pyqtSlot

class Mode( Enum ):
  NONE = 0
  ADD_ANIM = 1

class Scene( QGraphicsScene ):
  sReset = pyqtSignal()
  animDone = pyqtSignal([list])

  def __init__( self, parent = None ):
    QGraphicsScene.__init__( self, parent )

    self.mode = Mode.NONE

    self.curPos = QPointF()
    self.clickPos = QPointF()
    self.mousePressed = False

    self.setItemIndexMethod( QGraphicsScene.NoIndex )

    self.reset()

  def drawBackground( self, painter, rect ):
    if self.img is not None:
      painter.drawPixmap( QPointF( 0, 0 ), self.img )

  def drawForeground( self, painter, rect ):
    painter.save()
    painter.setPen( QPen( QBrush( QColor( 255, 0, 0 ) ), 3 ) )
    painter.drawLines( self.grid )
    painter.restore()

    if self.mousePressed and self.mode == Mode.ADD_ANIM:
      x = min( self.clickPos.x(), self.curPos.x() )
      y = min( self.clickPos.y(), self.curPos.y() )
      w = abs( self.curPos.x() - self.clickPos.x() )
      h = abs( self.curPos.y() - self.clickPos.y() )

      painter.fillRect( x, y, w, h, QBrush( QColor( 0, 255, 0, 70 ), Qt.SolidPattern ) )

  def mouseMoveEvent( self, e ):
    self.curPos = e.scenePos()
    self.update()
    QGraphicsScene.mouseMoveEvent( self, e )

  def mousePressEvent( self, e ):
    if e.button() == Qt.LeftButton:
      self.mousePressed = True
      self.clickPos = e.scenePos()

    self.update()
    QGraphicsScene.mousePressEvent( self, e )

  def mouseReleaseEvent( self, e ):
    self.mousePressed = False

    if self.mode == Mode.ADD_ANIM:
      x1 = int( self.clickPos.x() / self.fw ) + 1
      y1 = int( self.clickPos.y() / self.fh ) + 1
      x2 = int( e.scenePos().x() / self.fw ) + 1
      y2 = int( e.scenePos().y() / self.fh ) + 1

      self.animDone.emit( [ x1, y1, x2, y2 ] )

    self.update()
    QGraphicsScene.mouseReleaseEvent( self, e )

  def setImage( self, img ):
    if img is None:
      self.reset()
    else:
      self.img = QPixmap( img )
      self.setSceneRect( 0, 0, self.img.width(), self.img.height() )

    self.update()

  def setColsRows( self, cols, rows ):
    if self.img is not None:
      self.cols = cols
      self.rows = rows
      self.grid = []

      self.fw = int( self.img.width() / self.cols )
      self.fh = int( self.img.height() / self.rows )

      for x in range( 0, int( self.img.width() ), self.fw ):
        self.grid.append( QLineF( float(x), 0.0, x, float( self.img.height() ) ) )

      for y in range( 0, int( self.img.height() ), self.fh ):
        self.grid.append( QLineF( 0.0, float(y), float( self.img.width() ), float(y) ) )

      self.update()

  def setMode( self, mode ):
    self.mode = mode

  def reset( self ):
    self.img = None
    self.cols = 1
    self.rows = 1
    self.fw = 1
    self.fh = 1
    self.grid = []
    self.setSceneRect( 0, 0, 640, 480 )
    self.sReset.emit()

class AnimationEditor( QGraphicsView ):
  animDone = pyqtSignal([list])

  def __init__( self, parent = None ):
    QGraphicsView.__init__( self, parent )

    self.scene = Scene( self )
    self.setScene( self.scene )
    self.scene.animDone.connect( self.animDone )

    self.setMouseTracking( True )
    self.setRenderHint( QPainter.Antialiasing )
    self.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded );
    self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded );
    self.setAlignment( Qt.AlignCenter );
    self.setViewportUpdateMode( QGraphicsView.BoundingRectViewportUpdate )
    self.setCacheMode( QGraphicsView.CacheBackground )
    self.setFocusPolicy( Qt.StrongFocus )

  def setImage( self, img ):
    self.scene.setImage( img )

  def setColsRows( self, cols, rows ):
    self.scene.setColsRows( cols, rows )

  def setMode( self, mode ):
    self.scene.setMode( mode )

class MainWindow( QMainWindow ):
  def __init__( self, parent = None ):
    QMainWindow.__init__( self, parent )

    self.view = AnimationEditor( self )
    self.view.animDone.connect( self.animDone )

    self.toolsWidget = QWidget( self )
    self.vlToolsWidget = QVBoxLayout( self.toolsWidget )


    # Image Atlas
    self.gbAtlas = QGroupBox( 'Atlas', self.toolsWidget )

    self.atlasImage = QLineEdit( self.gbAtlas )
    self.openImageButton = QToolButton( self.gbAtlas )
    self.openImageButton.setText('...')
    self.openImageButton.clicked.connect( self.openAtlasImage )

    self.cols = QSpinBox( self.gbAtlas )
    self.cols.setButtonSymbols( QAbstractSpinBox.NoButtons )
    self.cols.setSingleStep(1)
    self.cols.setValue(1)
    self.cols.setMinimum(1)
    self.cols.valueChanged.connect( self.setColsRows )

    self.rows = QSpinBox( self.gbAtlas )
    self.rows.setButtonSymbols( QAbstractSpinBox.NoButtons )
    self.rows.setSingleStep(1)
    self.rows.setValue(1)
    self.rows.setMinimum(1)
    self.rows.valueChanged.connect( self.setColsRows )

    self.glAtlas = QGridLayout( self.gbAtlas )
    self.glAtlas.addWidget( QLabel( 'Image', self.gbAtlas ), 0, 0 )
    self.glAtlas.addWidget( self.atlasImage, 0, 1 )
    self.glAtlas.addWidget( self.openImageButton, 0, 2 )
    self.glAtlas.addWidget( QLabel( 'Columns', self.gbAtlas ), 1, 0 )
    self.glAtlas.addWidget( self.cols, 1, 1, 1, 2 )
    self.glAtlas.addWidget( QLabel( 'Rows', self.gbAtlas ), 2, 0 )
    self.glAtlas.addWidget( self.rows, 2, 1, 1, 2 )


    # Animations
    self.gbAnims = QGroupBox( 'Animations', self.toolsWidget )

    self.animList = QListWidget( self.gbAnims )

    self.addAnimButton = QToolButton( self.gbAnims )
    self.addAnimButton.setIconSize( QSize( 16, 16 ) )
    self.addAnimButton.setIcon( self.style().standardIcon( QStyle.SP_FileIcon ) )
    self.addAnimButton.setToolTip('Add Animation')
    self.addAnimButton.clicked.connect( self.addAnim )

    self.delAnimButton = QToolButton( self.gbAnims )
    self.delAnimButton.setIconSize( QSize( 16, 16 ) )
    self.delAnimButton.setIcon( self.style().standardIcon( QStyle.SP_BrowserStop ) )
    self.delAnimButton.setToolTip('Remove Animation')
    self.delAnimButton.clicked.connect( self.delAnim )

    self.hlButtons = QVBoxLayout()
    self.hlButtons.addWidget( self.addAnimButton )
    self.hlButtons.addWidget( self.delAnimButton )
    self.hlButtons.setAlignment( Qt.AlignTop )

    self.hlAnims = QHBoxLayout( self.gbAnims )
    self.hlAnims.addLayout( self.hlButtons )
    self.hlAnims.addWidget( self.animList )


    # Generate Code Button
    self.genButton = QPushButton( 'Generate', self.toolsWidget )
    self.genButton.clicked.connect( self.generateCode )


    self.vlToolsWidget.addWidget( self.gbAtlas )
    self.vlToolsWidget.addWidget( self.gbAnims )
    self.vlToolsWidget.addWidget( self.genButton )
    self.vlToolsWidget.setAlignment( Qt.AlignTop )

    self.tools = QDockWidget( 'Tools', self )
    self.tools.setWidget( self.toolsWidget )
    self.tools.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )

    self.setCentralWidget( self.view )
    self.addDockWidget( Qt.RightDockWidgetArea, self.tools )
    self.setWindowTitle('Animation Editor')

  @pyqtSlot()
  def openAtlasImage( self ):
    fileName = QFileDialog.getOpenFileName( self, 'Atlas Image', '', 'Image Files (*.png; *.jpg; *.jpeg; *.bmp)' )

    if fileName != '':
      self.atlasImage.setText( fileName )
      self.view.setImage( fileName )
      self.cols.setValue(1)
      self.rows.setValue(1)

  @pyqtSlot(int)
  def setColsRows( self, v ):
    self.view.setColsRows( self.cols.value(), self.rows.value() )

  @pyqtSlot()
  def generateCode( self ):
    print('GENERATE')

  @pyqtSlot()
  def addAnim( self ):
    self.view.setCursor( Qt.CrossCursor )
    self.view.setMode( Mode.ADD_ANIM )

  @pyqtSlot()
  def delAnim( self ):
    pass

  @pyqtSlot(list)
  def animDone( self, poses ):
    self.view.setCursor( Qt.ArrowCursor )
    self.view.setMode( Mode.NONE )

if __name__ == '__main__':
  app = QApplication( sys.argv )
  QApplication.setStyle( QStyleFactory.create('plastique') )

  ae = MainWindow()
  ae.show()

  sys.exit( app.exec_() )
