"""
AxisItem


GraphLayout
matplotlib.pyplot.figure (figure = plt.figure())
pyqtgraph.graphicsItems.GraphicsLayout.GraphicsLayout (view.ci)

"""
import sys
import copy
from PyQt4 import QtGui

class GraphAxisBase(object):
    def __init__(self, axis_item):
        object.__setattr__(self, '__wrapped', axis_item)
    def plot(self,x,y,*args,**kwargs):
        pass
    def __getattr__(self, name):
        if name == '_GraphAxisBase__wrapped':
            return self.__getattribute__('__wrapped')
        elif hasattr(self.__wrapped, name):
            return getattr(self.__wrapped, name)
        else:
            return self.__getattribute__(name)
    def __setattr__(self, name, val):
        if hasattr(self.__wrapped, name):
            self.__wrapped.__setattr__(name, val)
        else:
            object.__setattr__(self, name, val)
    def origin(self):
        return self.__wrapped

class PyQtGraphAxis(GraphAxisBase):
    def __init__(self, *args):
        GraphAxisBase.__init__(self, *args)
        # set for default color
        self.__color_list = self.package.functions.Colors.keys()
        self.__color_index = 0
        # set for legend
        self.addLegend(offset=(0, 0))
        # set to emulate matplotlib
        self.package.graphicsItems.LegendItem.LegendItem.__call__ = self._legend
        self.legend.hide()
    @staticmethod
    def _legend(legend, *args, **kwargs):
        if legend.isVisible():
            legend.hide()
        else:
            legend.show()
        return legend
    @staticmethod
    def format_str_to_dict(format_str):
        style_dict = {}
        for s in format_str:
            if s == "-":
                style_dict["shape"] = "-"
            elif s in "bgrcmykw":
                style_dict["color"] = s
        return style_dict

    def matplotlib2pyqt(self, plt_dict):
        style_dict_pyqt = {'color':None, "width":2, "name":None}
        if plt_dict['color'] in self.__color_list:
            style_dict_pyqt['color'] = plt_dict['color']
        if style_dict_pyqt["color"] == None:
            style_dict_pyqt["color"] = self.__color_list[self.__color_index]
            self.__color_index += 1
        if not plt_dict['linewidth'] == None:
            style_dict_pyqt['width'] = plt_dict['linewidth']
        if not plt_dict['label'] == None:
            style_dict_pyqt['name'] = plt_dict['label']
        return style_dict_pyqt

    def plot(self, *args, **kwargs):
        style_dict = {"shape":"-","color":None, "linewidth":None, "label":None}
        style_dict.update(kwargs)
        if len(args) == 1:
            y = args[0]
            x = range(len(y))
        elif len(args) == 2:
            if type(args[1]) == str:
                y = args[0]
                x = range(len(y))
                style_dict.update(self.format_str_to_dict(args[1]))
            else:
                x = args[0]
                y = args[1]
        elif len(args) == 3:
            x = args[0]
            y = args[1]
            style_dict.update(self.format_str_to_dict(args[2]))
        style_dict_pyqt = self.matplotlib2pyqt(style_dict)
        qpen = self.package.mkPen(style_dict_pyqt['color'], width=style_dict_pyqt['width'])
        self.package.graphicsItems.PlotItem.PlotItem.plot(self.origin(), x, y, pen=qpen, name=style_dict_pyqt["name"])

    def set_title(self, label, *args, **kwargs):
        self.setTitle(label)

    def set_xlabel(self, *args, **kwargs):
        text = args[0]
        units = ""
        if kwargs.has_key("units"):
            units = kwargs["units"]
        self.setLabel("bottom", text=text, units=units)

    def set_ylabel(self, *args, **kwargs):
        text = args[0]
        units = ""
        if kwargs.has_key("units"):
            units = kwargs["units"]
        self.setLabel("left", text=text, units=units)

    def grid(self, b=None, which=u'major', axis=u'both', **kwargs):
        x, y = False, False
        if b == None:
            b = True
        if axis == 'both':
            x = True and b
            y = True and b
        elif axis == 'x':
            x = True and b
        elif axis == 'y':
            y = True and b
        self.showGrid(x=x, y=y)

class matplotlibGraphAxis(GraphAxisBase):
    def __init__(self, *args):
        GraphAxisBase.__init__(self, *args)

    def plot(self,x,y,*args,**kwargs):
        return self.origin().plot(x,y,*args,**kwargs)

def graph_axis_factory(item):
    import matplotlib
    import matplotlib.axes
    if issubclass(type(item), matplotlib.axes.Axes):
        wrapper = type("MatplotlibAxesWrapper", (matplotlibGraphAxis,), {"package":matplotlib})
    import pyqtgraph
    import pyqtgraph.graphicsItems
    if issubclass(type(item), pyqtgraph.graphicsItems.PlotItem.PlotItem):
        wrapper = type("pyqtgraphAxesWrapper", (PyQtGraphAxis,), {"package":pyqtgraph})
    return wrapper(item)

class GraphLayoutBase(QtGui.QDialog):
    def __init__(self, layoutList):
        QtGui.QDialog.__init__(self)
        self.plotItemOrig = []
        self.__layout = []

        # override following methods
        self.setLayout(layoutList)
        self.connect_all_x_axes()

    def __getitem__(self, key):
        return self.__layout[key]

    def __setitem__(self, key, value):
        self.__layout[key] = value

    def __len__(self):
        return len(self.__layout)

    def __iter__(self):
        l = reduce(lambda x,y: x+y, self.__layout)
        return l.__iter__()

    def setLayout(self,layoutList):
        """
        setLayout(layoutList)
        example:
        1. setLayout([2])
        |fig|fig|
        2. setLayout([2,1,2])
        |fig|fig|
        |fig|
        |fig|fig|
        """
        print "please overwrite this method"
        layout = QtGui.QVBoxLayout()
        button = QtGui.QPushButton('Plot')
        layout.addWidget(button)
        QtGui.QDialog.setLayout(self, layout)

    def _set_layout_list(self, l):
        """
        l is 2d list of axes.
        please use in setLayout()
        self._set_layout_list([[ax00, ax01],[ax10, ax11, ax,12], ...])
        """
        self.__layout = l

    def connect_all_x_axes(self, parent, child):
        pass

    def removeItem(self,i,j):
        pass

    def addItem(self,i,j):
        pass


class PyQtGraphLayout(GraphLayoutBase):
    def __init__(self, *args):
        import pyqtgraph
        self.pyqtgraph = pyqtgraph
        self.view = self.pyqtgraph.GraphicsLayoutWidget()
        self.view.setBackground('w')
        self.view.setWindowTitle("sample")
        GraphLayoutBase.__init__(self, *args)

    def setLayout(self, layout_list):
        layout = QtGui.QVBoxLayout()
        for row in layout_list:
            for col in range(row):
                self.view.addPlot()
            self.view.nextRow()
        layout.addWidget(self.view)
        QtGui.QDialog.setLayout(self, layout)
        # meke self like a list
        item_dict = self.view.ci.rows
        tmp_layout = []
        for i in range(len(item_dict)):
            tmp_layout.append([])
            for j in range(len(item_dict[i])):
                wrapped_ax = graph_axis_factory(item_dict[i][j])
                tmp_layout[i].append(wrapped_ax)
        self._set_layout_list(tmp_layout)

    def connect_all_x_axes(self):
        parent = self[0][0]
        for i, child in enumerate(self):
            if not child is parent:
                child.setXLink(parent)
            else:
                parent.enableAutoRange()

class matplotlibGraphLayout(GraphLayoutBase):
    def __init__(self, *args):
        import matplotlib.pyplot as plt
        self.plt = plt
        GraphLayoutBase.__init__(self, *args)

    def setLayout(self, layout_list):
        try:
            from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
        except ImportError:
            from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
        # make instances
        layout = copy.copy(layout_list)
        if 0 in layout:
            layout.remove(0)
        max_row_num = len(layout_list)
        max_col_num = max(layout_list)
        self.axes = []
        for i in range(max_row_num):
            self.axes.append([])
        self.fig = self.plt.figure()
        for i, col_num in enumerate(layout_list):
            for j in range(col_num):
                ax = self.fig.add_subplot( max_row_num, max_col_num, max_col_num * i + j + 1 )
                wrapped_ax = graph_axis_factory(ax)
                self.axes[i].append(wrapped_ax)
        self._set_layout_list(self.axes)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.fig.set_facecolor((1,1,1,1))
        # generate layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        QtGui.QDialog.setLayout(self, layout)
        self.fig.tight_layout(pad=0.1, w_pad=0.5, h_pad=1.0)

    def connect_all_x_axes(self):
        parent = self[0][0]
        grouper = parent.get_shared_x_axes()
        for child in self:
            if child != parent:
                grouper.join(parent.origin(), child.origin())
            child.set_adjustable('datalim')

def test_layout():
    import sys
    app = QtGui.QApplication(sys.argv)

    print "please select graph interface. (0/1)"
    print "0: pyqtgraph"
    print "1: matplotlib"
    mode = int(sys.stdin.readline()[0])
    if mode == 0:
        graph_layout = PyQtGraphLayout([3,2])
    elif mode == 1:
        # graph_layout = matplotlibGraphLayout([6, 6, 5, 5, 5, 2, 5, 5, 5, 5, 6, 6])
        graph_layout = matplotlibGraphLayout([3,2])
    else:
        print "no mode."
        return False

    for ax in graph_layout:
        # wrap = graph_axis_factory(ax)
        ax.plot([0,1,2,3],[0,3,1,2], '-', linewidth=2, label = "line1")
        ax.plot([0,1,2,3],[0,1,2,3], '-', linewidth=2, label = "line2")
        ax.plot([0,1,2,3],[0,2,3,1], linewidth=2, label = "line3")
        ax.legend(loc=4)
        ax.set_title("title")
        ax.set_xlabel("x [ml]")
        ax.set_ylabel("y[ml]")
        ax.grid(True, axis = 'both')
    graph_layout.connect_all_x_axes()

    graph_layout.showMaximized()
    # main_window = QtGui.QMainWindow()
    # main_window.setCentralWidget(graph_layout)
    # main_window.show()
    app.exec_()

    # import IPython
    # IPython.embed()
