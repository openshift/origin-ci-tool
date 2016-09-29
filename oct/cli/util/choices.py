# coding=utf-8


class Choices(object):
    __metaclass__ = type('anonymous', (type,), dict(
        __iter__=lambda self: (v for k, v in vars(self).iteritems() if not k.startswith('_'))
    ))
