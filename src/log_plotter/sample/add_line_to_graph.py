from pyqtgraph.Qt import QtGui
import numpy as np
import pyqtgraph as pg

class InfiniteLineWithBreak(pg.GraphicsObject):
    def __init__(self, changeX, levelsY, pen=None):
        pg.GraphicsObject.__init__(self)

        self.changeX = changeX
        self.levelsY = levelsY

        self.maxRange = [None, None]
        self.moving = False
        self.movable = False
        self.mouseHovering = False

        pen = (200, 200, 100)
        self.setPen(pen)
        self.setHoverPen(color=(255,0,0), width=self.pen.width())
        self.currentPen = self.pen


    def setBounds(self, bounds):
        self.maxRange = bounds
        self.setValue(self.value())

    def setPen(self, *args, **kwargs):
        self.pen = pg.fn.mkPen(*args, **kwargs)
        if not self.mouseHovering:
            self.currentPen = self.pen
            self.update()

    def setHoverPen(self, *args, **kwargs):
        self.hoverPen = pg.fn.mkPen(*args, **kwargs)
        if self.mouseHovering:
            self.currentPen = self.hoverPen
            self.update()

    def boundingRect(self):
        br = self.viewRect()
        return br.normalized()

    def paint(self, p, *args):
        br = self.boundingRect()
        p.setPen(self.currentPen)
        # three lines (left border to change point, change point vertical, change point to right)
        p.drawLine(pg.Point(br.left(), self.levelsY[0]), pg.Point(self.changeX, self.levelsY[0]))
        p.drawLine(pg.Point(self.changeX, self.levelsY[0]), pg.Point(self.changeX, self.levelsY[1]))
        p.drawLine(pg.Point(self.changeX, self.levelsY[1]), pg.Point(br.right(), self.levelsY[1]))

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == 0:
            return None   ## x axis should never be auto-scaled
        else:
            return (0,0)

    def setMouseHover(self, hover):
        pass

app = QtGui.QApplication([])
w = pg.GraphicsWindow()
w.resize(1000, 600)
v = w.addPlot(y=np.random.normal(size=100))
v.addItem(InfiniteLineWithBreak(changeX=50, levelsY=(-1, 1)))
app.exec_()
