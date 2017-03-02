# -*- coding: utf-8 -*-

import numpy
import unittest.main
from unittest import TestCase
from log_plotter.lazy_data_generator import LazyDataGenerator

class TestLazyDataGenerator(TestCase):
    def lazy_data_generator_factory(self):
        data_server = dict()
        data_server['a'] = numpy.ones([10,3]) * 2
        data_server['b'] = numpy.ones([10,3]) * 3
        generator = LazyDataGenerator(data_dict = data_server, name = 'c', max_index = 3)
        return generator, data_server
        
    def test_init(self):
        generator, data_server = self.lazy_data_generator_factory()
        generator.depend = set(['a', 'b'])
        self.assertEqual(data_server['c'], generator)

    def test_to_array_with_int(self):
        generator, data_server = self.lazy_data_generator_factory()
        def add_data(index, data_server):
            return data_server['a'][:,index] + data_server['b'][:,index]
        generator._func = add_data
        ret = generator.toarray(0)
        self.assertTrue(numpy.array_equal(ret, numpy.ones([10,1]) * 5),
                        msg='LazyDataGenerator.to_array(0) is {}, though should be numpy.array([5]*10)'.format(ret))

    def test_to_array_with_list(self):
        generator, data_server = self.lazy_data_generator_factory()
        def add_data(index, data_server):
            return data_server['a'][:,index] + data_server['b'][:,index]
        generator._func = add_data
        ret = generator.toarray([0,1])
        self.assertTrue(numpy.array_equal(ret, numpy.ones([10,2]) * 5),
                        msg='LazyDataGenerator.to_array(0) is {}, though should be numpy.array([5]*10)'.format(ret))

    def test_to_array_with_slice(self):
        generator, data_server = self.lazy_data_generator_factory()
        def add_data(index, data_server):
            return data_server['a'][:,index] + data_server['b'][:,index]
        generator._func = add_data
        ret = generator.toarray(slice(0,3,2))
        self.assertTrue(numpy.array_equal(ret, numpy.ones([10,2]) * 5),
                        msg='LazyDataGenerator.to_array(0) is {}, though should be numpy.array([5]*10)'.format(ret))

    def test_to_array_with_None(self):
        generator, data_server = self.lazy_data_generator_factory()
        def add_data(index, data_server):
            return data_server['a'][:,index] + data_server['b'][:,index]
        generator._func = add_data
        ret = generator.toarray()
        self.assertTrue(numpy.array_equal(ret, numpy.ones([10,3]) * 5),
                        msg='LazyDataGenerator.to_array(0) is {}, though should be numpy.array([5]*10)'.format(ret))

    def test_lazy_data(self):
        generator, data_server = self.lazy_data_generator_factory()
        def add_data(index, data_server):
            return data_server['a'][:,index] + data_server['b'][:,index]
        generator._func = add_data
        lazy_data = generator[0]
        # import pdb;pdb.set_trace()
        ret = lazy_data.data
        self.assertTrue(numpy.array_equal(ret, numpy.ones([10,1]) * 5),
                        msg='LazyDataGenerator.to_array(0) is {}, though should be numpy.array([5]*10)'.format(ret))


if __name__ == '__main__':
    unittest.main(verbosity=2)
