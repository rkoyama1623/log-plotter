# -*- coding: utf-8 -*-

import numpy

class SparseMatrixForIndex(object):
    def __init__(self):
        self._data = dict()

    def __getitem__(self, indices):
        if type(indices) is int:
            ret = self._data.get(indices)
            if ret is None:
                raise IndexError
            return ret
        elif type(indices) is slice:
            if not indices.stop:
                indices = self._data.keys()
                indices.sort()
            elif not indices.start:
                indices = range(indices.stop)
            elif not indices.step:
                indices = range(indices.start, indices.stop)
            else:
                indices = range(indices.start, indices.stop, indices.step)
        columns = [self._data.get(index) for index in indices]
        for index, col in enumerate(columns):
            if col is None:
                raise IndexError, "index {} is not set".format(index)
        return numpy.c_[columns].T

    def __setitem__(self, indices, column):
        if type(indices) is int:
            self._set_item_for_index(indices, column)
            return
        elif type(indices) is slice:
            if not indices.start:
                indices = range(indices.stop)
            elif not indices.step:
                indices = range(indices.start, indices.stop)
            else:
                indices = range(indices.start, indices.stop, indices.step)
        [self._set_item_for_index(index, column[index]) for index in indices]

    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default
            
    def _set_item_for_index(self, index, column):
        assert len(column.shape) == 1
        self._data[index] = column

    def __repr__(self):
        return self[:].__repr__().replace('array', 'log_plotter.sparse_matrix')

class LazyDataGenerator(object):
    def __init__(self, data_dict=None, name=None,
                 func = None, args=None, kwargs=None,
                 max_index = 0, target_indices= None,
                 depends=[]):
        '''
        :param dict data_dict: dict holding all data
        :param str name: key to find this LazyDataGenerator in data_dict
        :param function func: function(index, data_server, *args, **kwargs)
        :param list args: args for func
        :param dict kwargs: keyword args for func
        :param int max_index: maximum index for this data generator
        :param int/slice/None target_indices: target indices to plot
        :param list depends: list of data_dict's key used when calculate data
        '''
        assert(data_dict is not None), "data_dict is not set"
        assert(name is not None), "name is not set"
        self.name = name
        self.data_dict = data_dict
        self.data_dict[self.name] = self
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._data = SparseMatrixForIndex()
        self._indices = target_indices
        self._max_index = max_index
        self.depends=depends

    def toarray(self, indices=None):
        '''
        :param int/slice indices: column indices for generated data
        '''
        if indices is None:
            indices = slice(self._max_index)
        if type(indices) is int:
            indices = [indices]
        elif type(indices) is slice:
            if indices.start is None:
                indices = range(indices.stop)
            elif indices.step is None:
                indices = range(indices.start, indices.stop)
            else:
                indices = range(indices.start, indices.stop, indices.step)
        for index in indices:
            if self._data.get(index) is None:
                array = self._func(index, self.data_dict)
                self._data[index] = array
        return self._data[indices]

    def __getitem__(self, indices):
        self._indices = indices
        return self

    @property
    def data(self):
        ret = self.toarray(self._indices if self._indices is not None else range(self._max_index))
        return ret
