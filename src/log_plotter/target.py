from abc import ABCMeta, abstractmethod
import numpy
import warnings

class MultipleLogDictBase(dict):
    '''
    Dictionary for targets
    '''
    __metaclass__ =  ABCMeta
    used_path = []

    def __init__(self, data=None):
        dict.__init__(self)

    def __getitem__(self, key):
        '''
        TargetDict['/path/to/log', 'ex']
        '''
        if type(key) is not tuple and len(self.used_path) is 0:
            raise KeyError, 'TargetDict.used_path is not set!'
        if type(key) is not tuple:
            assert(type(key) is str or type(key) is unicode)
            path = self.used_path[0]
            if len(self.used_path) > 1:
                warnings.warn('TargetDict has multiple path candidates, but {} is used'.format(path))
            return dict.__getitem__(self, (path, key))
        else:
            assert len(key) == 2, "length of key must be 2"
            assert type(key[0]) is str or type(key[0]) is unicode, "path/to/log must be str"
            return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if type(key) is not tuple and len(self.used_path) is 0:
            raise KeyError, 'TargetDict.used_path is not set!'
        if type(key) is not tuple:
            assert(type(key) is str or type(key) is unicode)
            path = self.used_path[0]
            if len(self.used_path) > 1:
                warnings.warn('TargetDict has multiple path candidates, but {} is used'.format(path))
            dict.__setitem__(self, (path, key), value)
        else:
            assert len(key) == 2, "length of key must be 2"
            assert type(key[0]) is str or type(key[0]) is unicode, "path/to/log must be str"
            if key[0] not in self.used_path:
                self.used_path.append(key[0])
            dict.__setitem__(self, key, value)


class DataDict(MultipleLogDictBase):
    def __init__(self):
        MultipleLogDictBase.__init__(self)
        self.used_path = []

class TargetDict(MultipleLogDictBase):
    '''
    Dictionary for targets
    '''
    def __init__(self, data=None):
        MultipleLogDictBase.__init__(self)
        self.data = DataDict() if data is None else data

    @property
    def used_path(self):
        return self.data.used_path
        

