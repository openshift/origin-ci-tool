# coding=utf-8


class Choices(object):
    class Iterator(type):
        def __iter__(self):
            return (v for k, v in vars(self).iteritems() if not k.startswith('_'))
    __metaclass__ = Iterator
