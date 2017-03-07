import numpy
import unittest.main
from unittest import TestCase
import log_plotter.target as target
from target import *

class TestTarget(TestCase):
    def test_target(self):
        targets = TargetDict()
        targets["hoge/fuga","st_q"] = 1
        targets["hoge/piyo","st_q"] = 2
        targets["hoge/piyo","abc_q"] = 3
        targets["hoge/fuga","abc_q"] = 4
        self.assertEqual(targets['st_q'], 1)
        self.assertEqual(targets['abc_q'], 4)
        self.assertEqual(targets["hoge/fuga","st_q"], 1)
        self.assertEqual(targets["hoge/piyo","st_q"], 2)
        self.assertEqual(targets["hoge/piyo","abc_q"], 3)
        self.assertEqual(targets["hoge/fuga","abc_q"], 4)

    def test_target2(self):
        targets = TargetDict()
        data = DataDict(path=["path/to/log1","path/to/log2"])
        self.assertEqual(data.paths, ["path/to/log1","path/to/log2"])
        index = 0
        x = data.get_x_data[targets.st_q, index]
        y = data.get_y_data[targets.st_q, index]

        tmp_data = data.filter(path="path/to/log") # how to identify path/to/log?


    def test_plot_sample(self):
        from log_plotter import *
        path1= "path/to/log1"
        path2= "path/to/log2"
        targets = TargetDict()
        data = DataDict(path=[path1, path2])
        data(path=[path1, path2])
        view = log_plotter.View()
        view.addGroup(legends=[data(path1, target.st_q)[0:3],
                               data(path1, target.abc_q)[0:3]]
                      xLabel="time",
                      yLabel="joint angle [deg]")
        view.addGroup(legends=[data(path1, target.watt)[0:3]])
        view.addGroup(legends=[data(path1, target_func.inverse(target.watt))[0:3]]) # inverse watt graph

if __name__ == '__main__':
    unittest.main(verbosity=2)
