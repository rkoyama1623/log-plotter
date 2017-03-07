import numpy
import unittest.main
from unittest import TestCase
import log_plotter.target as target
from target import TargetInterface

class DummyTarget(TargetInterface):
    depends = {'a', 'b'}
    def get_x_data(self, index):
        return range(index, index+3)
    def get_y_data(self, index):
        return range(index+3, index, -1)


class TestTarget(TestCase):
    def test_target_familiy_dict(self):
        '''
        test for TargetInterface
        '''
        dd = target.TargetFamilyDict()
        dd.add_target(DummyTarget)
        self.assertEqual(dd['DummyTarget'].name, 'DummyTarget', 'check ')
        self.assertTrue('a' in dd['DummyTarget'].depends)
        self.assertEqual(dd['DummyTarget'].get_x_data(0), range(0,3,1),
                         "dd['DummyTarget'].get_x_data(0) is {}".format(dd['DummyTarget'].get_x_data(0)))
        self.assertEqual(dd['DummyTarget'].get_y_data(0), range(3,0,-1),
                         "dd['DummyTarget'].get_y_data(0) is {}".format(dd['DummyTarget'].get_y_data(0)))

    def test_implicit_logged_target(self):
        d = target.TargetFamilyDict()
        d.add_logged_target('st_q')
        self.assertEqual(d['st_q'].name, 'st_q', "d['st_q'].name is {}".format(d['st_q'].name))
        self.assertTrue('st_q' in d['st_q'].depends, "d['st_q'].depends is {}".format(d['st_q'].depends))

    def test_implicit_logged_target2(self):
        d = target.TargetFamilyDict()
        self.assertEqual(d['st_q'].name, 'st_q', "d['st_q'].name is {}".format(d['st_q'].name))
        self.assertTrue('st_q' in d['st_q'].depends, "d['st_q'].depends is {}".format(d['st_q'].depends))


    def test_timed_target(self):
        def test(index, target_dict, *args, **kwargs):
            return index, target_dict, args, kwargs
        dd = target.TargetFamilyDict()
        dd.add_timed_target(name="foo", depends=['st_q'], func=test)
        self.assertEqual(dd['foo'].name, "foo", "dd['foo'].name is {}".format(dd['foo'].name))
        index, target_dict, args, kwargs= dd['foo'].get_y_data(0)
        self.assertEqual(index, 0, "index is {}".format(index))
        self.assertEqual(args, (), "args is {}".format(args))
        self.assertEqual(kwargs, {}, "kwargs is {}".format(kwargs))

    def test_timed_target_with_decorator(self):
        @target.TimedTarget.from_func(name='bar', depends={'log1','log2'})
        def target_with_log12(index, target_dict, *args, **kwargs):
            return 1
        d = target.TargetFamilyDict()
        self.assertEqual('bar', d['bar'].name, "d['bar'].name is {}".format(d['bar'].depends))
        self.assertTrue('log1' in d['bar'].depends, "d['bar'].depends is {}".format(d['bar'].depends))
        self.assertTrue('log2' in d['bar'].depends, "d['bar'].depends is {}".format(d['bar'].depends))
        self.assertEqual(1, d['bar'].get_y_data(0), "d['bar'].get_y_data(0) is {}".format(d['bar'].get_y_data(0)))

if __name__ == '__main__':
    unittest.main(verbosity=2)
