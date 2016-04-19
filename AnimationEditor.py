# -*- coding: UTF-8 -*-

import sys
from enum import Enum
from PyQt4.QtGui import *
'''
(
  QApplication, QWidget, QListView, QPushButton, QLineEdit, QLabel, QGridLayout, QToolButton, QFileDialog,
  QGraphicsView, QGraphicsScene, QPainter, QGraphicsSceneMouseEvent, QBrush, QColor, QPixmap, QPen, QMainWindow,
  QDockWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QSpinBox, QAbstractSpinBox, QStyleFactory, QStyle, QDialog,
  QStackedWidget, QPlainTextEdit, QFont, QFontMetrics, QStandardItem, QStandardItemModel, QAbstractItemView,
  QDoubleSpinBox
)
'''
from PyQt4.QtCore import * # Qt, QDir, QFileInfo, QRectF, QPointF, QLineF, QSize, pyqtSignal, pyqtSlot

class Mode( Enum ):
  NONE = 0
  ADD_ANIM = 1

class Roles( Enum ):
  FrameTime = Qt.UserRole,
  Rows = Qt.UserRole + 1,
  Cols = Qt.UserRole + 2

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

      for x in range( 0, int( self.img.width() + 1 ), self.fw ):
        self.grid.append( QLineF( float(x), 0.0, x, float( self.img.height() ) ) )

      for y in range( 0, int( self.img.height() + 1 ), self.fh ):
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

class AnimParamsDialog( QDialog ):
  def __init__( self, parent = None ):
    QDialog.__init__( self, parent )

    self.time = QDoubleSpinBox( self )
    self.time.setSingleStep( 0.1 )
    self.time.setValue( 0.1 )
    self.time.setMinimum( 0.01 )

    self.name = QLineEdit( self )

    self.ok = QPushButton( self.style().standardIcon( QStyle.SP_DialogApplyButton ), 'OK', self )
    self.ok.clicked.connect( self.accept )

    self.cancel = QPushButton( self.style().standardIcon( QStyle.SP_DialogCancelButton ), 'Cancel', self )
    self.cancel.clicked.connect( self.reject )

    self.hl = QHBoxLayout()
    self.hl.addWidget( self.cancel )
    self.hl.addWidget( self.ok )

    self.gl = QGridLayout( self )
    self.gl.addWidget( QLabel( 'Name', self ), 0, 0 )
    self.gl.addWidget( self.name, 0, 1 )
    self.gl.addWidget( QLabel( 'Time', self ), 1, 0 )
    self.gl.addWidget( self.time, 1, 1 )
    self.gl.addLayout( self.hl, 2, 0, 1, 2 )

    self.name.setFocus()
    self.setWindowTitle('Animation Settings')

  def getTime( self ):
    return self.time.value()

  def getName( self ):
    return self.name.text()

class MainWindow( QMainWindow ):
  def __init__( self, parent = None ):
    QMainWindow.__init__( self, parent )

    self.animParams = AnimParamsDialog( self )

    self.animName = ''
    self.itemSize = QSize()
    self.itemSize.setHeight( QFontMetrics( QApplication.font() ).height() + 4 )

    self.stack = QStackedWidget( self )

    self.view = AnimationEditor( self.stack )
    self.view.animDone.connect( self.animDone )

    self.code = QWidget( self.stack )

    self.codeText = QPlainTextEdit( self.code )
    self.codeText.setFont( QFont( 'Lucida Console', 12 ) )

    self.backToImage = QPushButton( 'Back', self.code )
    self.backToImage.clicked.connect( self.goBack )

    self.vlCode = QVBoxLayout( self.code )
    self.vlCode.addWidget( self.codeText )
    self.vlCode.addWidget( self.backToImage )

    self.stack.addWidget( self.view )
    self.stack.addWidget( self.code )
    self.stack.setCurrentIndex(0)

    self.toolsWidget = QWidget( self )
    self.vlToolsWidget = QVBoxLayout( self.toolsWidget )


    # Image Atlas
    self.gbAtlas = QGroupBox( 'Atlas', self.toolsWidget )

    self.atlasImage = QLineEdit( self.gbAtlas )
    self.atlasImage.setReadOnly( True )

    self.openImageButton = QToolButton( self.gbAtlas )
    self.openImageButton.setText('...')
    self.openImageButton.clicked.connect( self.openAtlasImage )

    self.cols = QSpinBox( self.gbAtlas )
    #self.cols.setButtonSymbols( QAbstractSpinBox.NoButtons )
    self.cols.setSingleStep(1)
    self.cols.setValue(1)
    self.cols.setMinimum(1)
    self.cols.valueChanged.connect( self.setColsRows )

    self.rows = QSpinBox( self.gbAtlas )
    #self.rows.setButtonSymbols( QAbstractSpinBox.NoButtons )
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

    self.animList = QListView( self.gbAnims )
    self.animList.setEditTriggers( QAbstractItemView.NoEditTriggers )
    self.animList.setSelectionMode( QAbstractItemView.SingleSelection )

    self.animListModel = QStandardItemModel( self.animList )

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


    # Tools window
    self.tools = QDockWidget( 'Tools', self )
    self.tools.setWidget( self.toolsWidget )
    self.tools.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )

    self.setCentralWidget( self.stack )
    self.addDockWidget( Qt.RightDockWidgetArea, self.tools )
    self.setWindowTitle('Animation Editor')

  @pyqtSlot()
  def openAtlasImage( self ):
    fileName = QFileDialog.getOpenFileName( self, 'Atlas Image', '', 'Image Files (*.png; *.jpg; *.jpeg; *.bmp)' )

    if fileName != '':
      self.atlasImage.setText( QFileInfo( fileName ).fileName() )
      self.animName = QFileInfo( fileName ).baseName()
      self.view.setImage( fileName )
      self.cols.setValue(1)
      self.rows.setValue(1)
      self.animListModel.removeRows( 0, self.animListModel.rowCount() )

  @pyqtSlot(int)
  def setColsRows( self, v ):
    self.view.setColsRows( self.cols.value(), self.rows.value() )

  @pyqtSlot()
  def generateCode( self ):
    self.codeText.clear()

    self.codeText.appendPlainText('-- init function')
    self.codeText.appendPlainText('self.' + self.animName + ' = Animation:new( {')
    self.codeText.appendPlainText('  pos  = Vector( 0, 0 ),')
    self.codeText.appendPlainText('  img  = "' + self.atlasImage.text() + '",')
    self.codeText.appendPlainText('  rows = ' + str( self.rows.value() ) + ',')
    self.codeText.appendPlainText('  cols = ' + str( self.cols.value() ))
    self.codeText.appendPlainText('} )')

    for i in range( 0, self.animListModel.rowCount() ):
      name = self.animListModel.data( self.animListModel.index( i, 0 ), Qt.DisplayRole )
      rows = self.animListModel.data( self.animListModel.index( i, 0 ), Qt.UserRole + 1 )
      cols = self.animListModel.data( self.animListModel.index( i, 0 ), Qt.UserRole + 2 )
      frameTime = self.animListModel.data( self.animListModel.index( i, 0 ), Qt.UserRole )
      self.codeText.appendPlainText(
        'self.'
        + self.animName
        + ':add( "'
        + name
        + '", '
        + str( cols )
        + ', '
        + str( rows )
        + ', '
        + str( round( frameTime, 2 ) ) + ' )'
      )

    self.codeText.appendPlainText('')
    self.codeText.appendPlainText('-- draw function')
    self.codeText.appendPlainText('self.' + self.animName + ':draw()')
    self.codeText.appendPlainText('')
    self.codeText.appendPlainText('-- update function')
    self.codeText.appendPlainText('self.' + self.animName + ':update( dt )')
    self.codeText.appendPlainText('')
    self.codeText.appendPlainText('-- other functions')

    for i in range( 0, self.animListModel.rowCount() ):
      name = self.animListModel.data( self.animListModel.index( i, 0 ), Qt.DisplayRole )
      self.codeText.appendPlainText('self.' + self.animName + ':change("' + name + '")')

    self.codeText.appendPlainText('self.' + self.animName + ':flipV()')
    self.codeText.appendPlainText('self.' + self.animName + ':flipH()')
    self.codeText.appendPlainText('self.' + self.animName + ':pause()')
    self.codeText.appendPlainText('self.' + self.animName + ':resume()')
    self.codeText.appendPlainText('')

    self.stack.setCurrentIndex(1)

  @pyqtSlot()
  def addAnim( self ):
    self.view.setCursor( Qt.CrossCursor )
    self.view.setMode( Mode.ADD_ANIM )

  @pyqtSlot()
  def delAnim( self ):
    indexes = self.animList.selectedIndexes()

    if indexes == []:
      return

    reply = QMessageBox.question( self, 'Animation Editor', 'Delete animation?', QMessageBox.Yes | QMessageBox.No )

    if reply == QMessageBox.Yes:
      self.animListModel.removeRows( indexes[0].row(), 1 )

  @pyqtSlot(list)
  def animDone( self, poses ):
    self.view.setCursor( Qt.ArrowCursor )
    self.view.setMode( Mode.NONE )

    if self.animParams.exec() == QDialog.Accepted:
      cols = 1
      rows = 1

      if poses[0] == poses[2]:
        cols = poses[0]
      else:
        cols = '"' + str( poses[0] ) + '-' + str( poses[2] ) + '"'

      if poses[1] == poses[3]:
        rows = poses[1]
      else:
        rows = '"' + str( poses[1] ) + '-' + str( poses[3] ) + '"'

      item = QStandardItem()
      item.setData( self.animParams.getName(), Qt.DisplayRole )
      item.setData( self.style().standardIcon( QStyle.SP_MediaPlay ), Qt.DecorationRole )
      item.setData( self.itemSize, Qt.SizeHintRole )
      item.setData( self.animParams.getTime(), Qt.UserRole )
      item.setData( rows, Qt.UserRole + 1 )
      item.setData( cols, Qt.UserRole + 2 )
      self.animListModel.invisibleRootItem().appendRow( item )
      self.animList.setModel( self.animListModel )

  @pyqtSlot()
  def goBack( self ):
    self.stack.setCurrentIndex(0)

if __name__ == '__main__':
  app = QApplication( sys.argv )
  QApplication.setStyle( QStyleFactory.create('plastique') )

  ae = MainWindow()
  ae.show()

  sys.exit( app.exec_() )
