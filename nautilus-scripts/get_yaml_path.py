#!/usr/bin/env python
# -*-coding: utf-8-*-
import sys
import os
import functools
from PyQt4 import QtGui
from PyQt4 import QtCore

class PathSelector (QtGui.QGroupBox):
   def __init__(self, parent, group_name, button_name, default_path=None):
      '''
      :param widget parent: parent widget
      :param str group_name: name of this item displayed on left up
      :param str button_name: name displayed on button
      :param str default_path: default path to file
      '''
      self.parent = parent
      default_path = str(default_path)
      QtGui.QVBoxLayout.__init__(self, group_name)
      # make layouts
      vbox = QtGui.QVBoxLayout()
      hbox = QtGui.QHBoxLayout()
      # label and button
      self.label = QtGui.QLabel(default_path)
      self.button = QtGui.QPushButton(parent)
      self.button.setText(button_name)
      # set parents
      hbox.addWidget(self.button)
      hbox.addWidget(self.label)
      vbox.addLayout(hbox)
      self.setLayout(vbox)

      # self.button.clicked.connect(functools.partial(self.select_path, self))
      self.button.clicked.connect(self.select_path)
   def select_path(self):
      d = QtGui.QFileDialog(self.parent)
      path = self.label.text()
      pathname = d.getOpenFileName(directory=os.path.dirname(str(path)))
      if not pathname == "":
         self.label.setText(pathname)

   def get_path(self):
      return str(self.label.text())

def get_script_path():
   import os
   import sys
   if sys.argv[0].split('/')[0] == '':
      return os.path.dirname(sys.argv[0])
   else:
      return os.path.realpath(os.path.dirname('{}/{}'.format(os.getcwd(), sys.argv[0]))) # /path/to/log-plotter

class MainDialog(object):
   def __init__(self):
      self.app = QtGui.QApplication(sys.argv)
      plot_yaml_history, layout_yaml_history = self.read_path_history()
      self.window = QtGui.QWidget()
      vbox = QtGui.QVBoxLayout()

      script_root_dir = self.script_root_dir
      plot_yaml = PathSelector(self.window, 'plot.yaml', 'select', plot_yaml_history)
      layout_yaml = PathSelector(self.window, 'layout.yaml', 'select', layout_yaml_history)
      self.plot_yaml = plot_yaml
      self.layout_yaml = layout_yaml
      vbox.addWidget(plot_yaml)
      vbox.addWidget(layout_yaml)

      button = QtGui.QPushButton(self.window)
      button.setText('OK')
      vbox.addWidget(button)
      button.clicked.connect(self.quit_app)

      self.window.setLayout(vbox)
      self.window.setWindowTitle("PyQt Dialog demo")
      for btn in [plot_yaml.button, layout_yaml.button]:
         btn.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
      self.window.show()

      sys.exit(self.app.exec_())

   def quit_app(self):
      plot_yaml_path = self.plot_yaml.get_path()
      layout_yaml_path = self.layout_yaml.get_path()
      self.write_path_history(plot_yaml_path, layout_yaml_path)
      sys.stdout.write('{} {}'.format(plot_yaml_path, layout_yaml_path))
      QtCore.QCoreApplication.instance().quit()

   def read_path_history(self):
      script_root_dir = get_script_path()
      self.script_root_dir = script_root_dir
      historyfile = '{}/.log_plotter'.format(script_root_dir)
      try:
         with open(historyfile, 'r') as f:
            paths = f.readline()
         plot_yaml_path, layout_yaml_path = paths.split(' ')
         plot_isYaml = os.path.basename(plot_yaml_path).split('.')[-1] == 'yaml'
         layout_isYaml = os.path.basename(layout_yaml_path).split('.')[-1] == 'yaml'
      except (ValueError, IOError):
         plot_isYaml =False
         layout_isYaml = False
      if not plot_isYaml:
         plot_yaml_path = '{}/../{}'.format(script_root_dir, 'config/robot/jaxon/test.yaml')
      if not layout_isYaml:
         layout_yaml_path = '{}/../{}'.format(script_root_dir, 'config/robot/jaxon/test-layout.yaml')
      return (plot_yaml_path, layout_yaml_path)

   def write_path_history(self, plot_yaml_path, layout_yaml_path):
      script_root_dir = self.script_root_dir
      historyfile = '{}/.log_plotter'.format(script_root_dir)
      with open(historyfile, 'w') as f:
         f.writelines('{} {}'.format(plot_yaml_path, layout_yaml_path))

if __name__ == '__main__':
   m = MainDialog()
