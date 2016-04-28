# -*- coding: UTF-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Scene( QGraphicsScene ):
  def __init__( self, parent = None ):
    QGraphicsScene.__init__( self, parent )

    self.mainWindow = None

    self.cols = 1
    self.rows = 1
    self.fw = 32
    self.fh = 32
    self.grid = []

    self.setSceneRect( 0, 0, self.fw * self.cols, self.fh * self.rows )
    self.setGrid()
    self.update()

  def drawAtlas( self, painter ):
    if self.mainWindow != None:
      for y in range( 0, self.rows ):
        for x in range( 0, self.cols ):
          index = (y * self.rows) + x

          if index < self.mainWindow.imageListModel.rowCount():
            fileName = self.mainWindow.imageListModel.data( self.mainWindow.imageListModel.index( index, 0 ), Qt.UserRole )
            img = QImage( fileName )

            w = self.fw
            h = self.fh
            ox = 0
            oy = 0

            # TODO: косяк с изменением размера фрейма и последнее изображение 2 раза выводится
            if img.width() > img.height():
              h = img.height() * (self.fw / img.width())
              oy = (self.fh - h) / 2
            else:
              w = img.width() * (self.fh / img.height())
              ox = (self.fw - w) / 2

            painter.drawImage( QRect( x * self.fw + ox, y * self.fh + oy, w, h ), img, QRect( 0, 0, img.width(), img.height() ) )

  def getAtlas( self, fileName ):
    iAtlas = QImage( QSize( self.fw * self.cols, self.fh * self.rows ), QImage.Format_ARGB32 )
    iAtlas.fill( Qt.transparent )

    pAtlas = QPainter( iAtlas )
    pAtlas.setRenderHints( QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform )
    self.drawAtlas( pAtlas )
    pAtlas.end()

    wAtlas = QImageWriter()
    wAtlas.setFileName( fileName )
    wAtlas.write( iAtlas )

  def drawBackground( self, painter, rect ):
    self.drawAtlas( painter )

  def drawForeground( self, painter, rect ):
    painter.save()
    painter.setPen( QPen( QBrush( QColor( 255, 0, 0 ) ), 2 ) )
    painter.drawLines( self.grid )
    painter.restore()

  def setMainWindow( self, w ):
    self.mainWindow = w

  def setColsRows( self, cols, rows ):
    self.cols = cols
    self.rows = rows
    self.setSceneRect( 0, 0, self.fw * self.cols, self.fh * self.rows )
    self.setGrid()
    self.update()

  def setFrameSize( self, width, height ):
    self.fw = width
    self.fh = height
    self.setSceneRect( 0, 0, self.fw * self.cols, self.fh * self.rows )
    self.setGrid()
    self.update()

  def setGrid( self ):
    self.grid = []

    for x in range( 0, int( self.fw * self.cols + 1 ), self.fw ):
      self.grid.append( QLineF( float(x), 0.0, x, float( self.fh * self.rows ) ) )

    for y in range( 0, int( self.fh * self.rows + 1 ), self.fh ):
      self.grid.append( QLineF( 0.0, float(y), float( self.fw * self.cols ), float(y) ) )

class ImageView( QGraphicsView ):
  def __init__( self, parent = None ):
    QGraphicsView.__init__( self, parent )

    self.mainWindow = None

    self.scene = Scene( self )
    self.setScene( self.scene )

    self.setMouseTracking( False )
    self.setRenderHints( QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform )
    self.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded );
    self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded );
    self.setAlignment( Qt.AlignCenter );
    self.setViewportUpdateMode( QGraphicsView.FullViewportUpdate )
    self.setCacheMode( QGraphicsView.CacheNone )
    self.setFocusPolicy( Qt.NoFocus )

  def setMainWindow( self, w ):
    self.scene.setMainWindow(w)

  def setColsRows( self, cols, rows ):
    self.scene.setColsRows( cols, rows )

  def setFrameSize( self, width, height ):
    self.scene.setFrameSize( width, height )

  def updateScene( self ):
    self.scene.update()

  def getAtlas( self, fileName ):
    self.scene.getAtlas( fileName )

class MainWindow( QMainWindow ):
  imageListModel = None

  def __init__( self, parent = None ):
    QMainWindow.__init__( self, parent )

    self.view = ImageView( self )
    self.view.setMainWindow( self )

    self.itemSize = QSize()
    self.itemSize.setHeight( QFontMetrics( QApplication.font() ).height() + 4 )

    self.tools = QDockWidget( 'Tools', self )
    self.tools.setWidget( self.getToolsWidget( self ) )
    self.tools.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )

    self.setCentralWidget( self.view )
    self.addDockWidget( Qt.RightDockWidgetArea, self.tools )
    self.setMinimumSize( 640, 480 )
    self.setWindowTitle('Texture Pack Creator')

  def getToolsWidget( self, parent ):
    self.toolsWidget = QWidget( parent )
    self.vlToolsWidget = QVBoxLayout( self.toolsWidget )

    # Grid Widget
    self.gbGrid = QGroupBox( 'Grid', self.toolsWidget )

    self.cols = QSpinBox( self.gbGrid )
    self.cols.setSingleStep(1)
    self.cols.setValue(1)
    self.cols.setMinimum(1)
    self.cols.setMaximum(99999)
    self.cols.valueChanged.connect( self.setColsRows )

    self.rows = QSpinBox( self.gbGrid )
    self.rows.setSingleStep(1)
    self.rows.setValue(1)
    self.rows.setMinimum(1)
    self.rows.setMaximum(99999)
    self.rows.valueChanged.connect( self.setColsRows )

    self.glGrid = QGridLayout( self.gbGrid )
    self.glGrid.addWidget( QLabel( 'Columns', self.gbGrid ), 0, 0 )
    self.glGrid.addWidget( self.cols, 0, 1 )
    self.glGrid.addWidget( QLabel( 'Rows', self.gbGrid ), 1, 0 )
    self.glGrid.addWidget( self.rows, 1, 1 )
    self.glGrid.setAlignment( Qt.AlignTop )
    # Grid Widget /

    # Frame Size Widget
    self.gbFrameSize = QGroupBox( 'Frame Size', self.toolsWidget )

    self.fsWidth = QSpinBox( self.gbFrameSize )
    self.fsWidth.setSingleStep(1)
    self.fsWidth.setValue( 32 )
    self.fsWidth.setMinimum(1)
    self.fsWidth.setMaximum(99999)
    self.fsWidth.valueChanged.connect( self.setFrameSize )

    self.fsHeight = QSpinBox( self.gbFrameSize )
    self.fsHeight.setSingleStep(1)
    self.fsHeight.setValue( 32 )
    self.fsHeight.setMinimum(1)
    self.fsHeight.setMaximum(99999)
    self.fsHeight.valueChanged.connect( self.setFrameSize )

    self.glFrameSize = QGridLayout( self.gbFrameSize )
    self.glFrameSize.addWidget( QLabel( 'Width', self.gbFrameSize ), 0, 0 )
    self.glFrameSize.addWidget( self.fsWidth, 0, 1 )
    self.glFrameSize.addWidget( QLabel( 'Height', self.gbFrameSize ), 1, 0 )
    self.glFrameSize.addWidget( self.fsHeight, 1, 1 )
    self.glFrameSize.setAlignment( Qt.AlignTop )
    # Frame Size Widget /


    # Images Widget
    self.gbImages = QGroupBox( 'Images', self.toolsWidget )

    self.imageList = QListView( self.gbImages )
    self.imageList.setEditTriggers( QAbstractItemView.NoEditTriggers )
    self.imageList.setSelectionMode( QAbstractItemView.SingleSelection )

    self.imageListModel = QStandardItemModel( self.imageList )

    self.addButton = QToolButton( self.gbImages )
    self.addButton.setIconSize( QSize( 16, 16 ) )
    self.addButton.setIcon( self.style().standardIcon( QStyle.SP_FileIcon ) )
    self.addButton.setToolTip('Add Image')
    self.addButton.clicked.connect( self.addImage )

    self.delButton = QToolButton( self.gbImages )
    self.delButton.setIconSize( QSize( 16, 16 ) )
    self.delButton.setIcon( self.style().standardIcon( QStyle.SP_BrowserStop ) )
    self.delButton.setToolTip('Remove Image')
    self.delButton.clicked.connect( self.delImage )

    self.upButton = QToolButton( self.gbImages )
    self.upButton.setIconSize( QSize( 16, 16 ) )
    self.upButton.setIcon( self.style().standardIcon( QStyle.SP_ArrowUp ) )
    self.upButton.setToolTip('Move Up')
    self.upButton.clicked.connect( self.upImage )

    self.downButton = QToolButton( self.gbImages )
    self.downButton.setIconSize( QSize( 16, 16 ) )
    self.downButton.setIcon( self.style().standardIcon( QStyle.SP_ArrowDown ) )
    self.downButton.setToolTip('Move Down')
    self.downButton.clicked.connect( self.downImage )

    self.hlButtons = QVBoxLayout()
    self.hlButtons.addWidget( self.addButton )
    self.hlButtons.addWidget( self.delButton )
    self.hlButtons.addSpacing( 10 )
    self.hlButtons.addWidget( self.upButton )
    self.hlButtons.addWidget( self.downButton )
    self.hlButtons.setAlignment( Qt.AlignTop )

    self.hlImages = QHBoxLayout( self.gbImages )
    self.hlImages.addLayout( self.hlButtons )
    self.hlImages.addWidget( self.imageList )
    # Images Widget /


    # Generate Button
    self.genButton = QPushButton( 'Generate', self.toolsWidget )
    self.genButton.clicked.connect( self.generate )
    # Generate Button /


    self.vlToolsWidget.addWidget( self.gbGrid )
    self.vlToolsWidget.addWidget( self.gbFrameSize )
    self.vlToolsWidget.addWidget( self.gbImages )
    self.vlToolsWidget.addWidget( self.genButton )
    self.vlToolsWidget.setAlignment( Qt.AlignTop )

    return self.toolsWidget

  @pyqtSlot(int)
  def setColsRows( self, v ):
    self.view.setColsRows( self.cols.value(), self.rows.value() )

  @pyqtSlot(int)
  def setFrameSize( self, v ):
    self.view.setFrameSize( self.fsWidth.value(), self.fsHeight.value() )

  @pyqtSlot()
  def addImage( self ):
    fileName = QFileDialog.getOpenFileName( self, 'Image', '', 'Image Files (*.png; *.jpg; *.jpeg; *.bmp)' )

    if fileName != '':
      item = QStandardItem()
      item.setData( QFileInfo( fileName ).fileName(), Qt.DisplayRole )
      item.setData( self.style().standardIcon( QStyle.SP_MediaPlay ), Qt.DecorationRole )
      item.setData( self.itemSize, Qt.SizeHintRole )
      item.setData( fileName, Qt.UserRole )

      self.imageListModel.invisibleRootItem().appendRow( item )
      self.imageList.setModel( self.imageListModel )

      self.view.updateScene()

  @pyqtSlot()
  def delImage( self ):
    indexes = self.imageList.selectedIndexes()

    if indexes == []:
      return

    reply = QMessageBox.question( self, 'Texture Pack Creator', 'Delete image?', QMessageBox.Yes | QMessageBox.No )

    if reply == QMessageBox.Yes:
      self.imageListModel.removeRows( indexes[0].row(), 1 )
      self.view.updateScene()

  @pyqtSlot()
  def upImage( self ):
    pass

  @pyqtSlot()
  def downImage( self ):
    pass

  @pyqtSlot()
  def generate( self ):
    fileName = QFileDialog.getSaveFileName( self, 'Texture Atlas', '', 'Image Files (*.png; *.jpg; *.jpeg; *.bmp)' )

    if fileName != '':
      self.view.getAtlas( fileName )

if __name__ == '__main__':
  app = QApplication( sys.argv )
  QApplication.setStyle( QStyleFactory.create('plastique') )

  w = MainWindow()
  w.show()

  sys.exit( app.exec_() )
