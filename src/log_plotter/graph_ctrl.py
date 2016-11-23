import sys
import numpy
import functools
from pyqtgraph import QtGui

class CurveOffset(QtGui.QHBoxLayout):
   def __init__(self, name, curve):
      QtGui.QHBoxLayout.__init__(self)
      self.addWidget(QtGui.QLabel(name))
      self.curve = curve
      self.sp = QtGui.QDoubleSpinBox()
      self.addWidget(self.sp)
      self.sp.valueChanged.connect(functools.partial(self.setOffset, 1))
      self.sp.setMinimum(-1000)
      self.sp.setMaximum(1000)
      self.sp.setSingleStep(0.01)
      self.sp.setDecimals(3)

      data = curve.getData()
      x = data[0].copy()
      y = data[1].copy()
      self.originData = (x,y)
      self.offsets = [0, 0]

      self.sp.setMinimum(-1000)
      self.sp.setMaximum(1000)
      step = float((max(y)-min(y))/100)
      self.sp.setSingleStep(10**numpy.round(numpy.log10(step), 0) if step > 0 else 0)
      step_dec = - numpy.log10(step) if step > 0 else 0
      self.sp.setDecimals(max(step_dec, 0))

   def setOffset(self, axis_index):
      '''
      axis_index: x=0, y=1
      '''
      self.offsets[axis_index] = self.sp.value()
      self.curve.setData(self.originData[0]+self.offsets[0], self.originData[1]+self.offsets[1])

class GraphOffset(QtGui.QWidget):
   def __init__(self):
      QtGui.QWidget.__init__(self)
      self.layout = QtGui.QVBoxLayout()
      self.graph_offsets = []

   def add_curve(self, curve):
      name = curve.name()
      graph_offset = CurveOffset(name, curve)
      self.graph_offsets.append(graph_offset)
      self.layout.addLayout(graph_offset)

   def update(self):
      self.setLayout(self.layout)
