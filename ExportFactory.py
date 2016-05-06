# -*- coding: UTF-8 -*-

from PyQt4.QtCore import QObject
from WindowsExporter import *
from MacExporter import *
from AndroidExporter import *

class ExportFactory( QObject ):
  def __init__( self, parent = None ):
    QObject.__init__( self, parent )

  def getExporter( self, name ):
    if name == 'windows':
      return WindowsExporter()
    elif name == 'macosx':
      return MacExporter()
  elif name == 'android':
      return AndroidExporter()
