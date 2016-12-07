# coding=utf-8
from __future__ import absolute_import, division, print_function


class AWSClientConfiguration(object):
    """
    This container holds configuration options
    for the AWS client and general interaction
    with the AWS EC2 API.
    """

    def __init__(self, keypair_name=None, private_key_path=None):
        # the name of the keypair to use to connect
        # to AWS EC2 instances
        self.keypair_name = keypair_name

        # the path to the private key for the afore-
        # mentioned keypair
        self.private_key_path = private_key_path

    def __iter__(self):
        """
        Return an iterator for contained properties.

        :return: the iterator
        """
        return (x for x in vars(self))

    def __getitem__(self, key):
        """
        Fetch the configuration key.

        :param key: name of the item to fetch
        :return: value of the item
        """
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __setitem__(self, key, value):
        """
        Update the value of the configuration entry.

        :param key: name of the item to update
        :param value: value to update the item to
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError('No such option `{}`.'.format(key))

    def __contains__(self, key):
        """
        Determine if the container in fact
        contain the configuration item.

        :param key: name of the item to search for
        :return: whether or not we contain the item
        """
        return hasattr(self, key)
