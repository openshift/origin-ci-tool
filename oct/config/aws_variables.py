# coding=utf-8
from __future__ import absolute_import, division, print_function

DEFAULT_IDENTIFYING_TAG_KEY = 'origin_ci_aws_cluster_component'
DEFAULT_MASTER_SUBNET_TAG_VALUE = 'master_subnet'
DEFAULT_ETCD_SECURITY_GROUP_TAG_VALUE = 'etcd_security_group'
DEFAULT_NODE_SECURITY_GROUP_TAG_VALUE = 'node_security_group'
DEFAULT_MASTER_SECURITY_GROUP_TAG_VALUE = 'master_security_group'
DEFAULT_MASTER_EXTERNAL_ELB_SECURITY_GROUP_TAG_VALUE = 'master_external_elb_security_group'
DEFAULT_MASTER_INTERNAL_ELB_SECURITY_GROUP_TAG_VALUE = 'master_internal_elb_security_group'
DEFAULT_ROUTER_SECURITY_GROUP_TAG_VALUE = 'router_security_group'
DEFAULT_ROUTER_ELB_SECURITY_GROUP_TAG_VALUE = 'router_elb_security_group'

DEFAULT_MASTER_INSTANCE_TYPE = 'm4.xlarge'
DEFAULT_REGION = 'us-east-1'
DEFAULT_MASTER_ROOT_VOLUME_SIZE = '75'

_aws_variable_prefix = 'origin_ci_aws_'


class AWSVariables(object):
    """
    This container holds values for defaulting
    the set of variables used in provisioning
    objects in AWS EC2.

    Every member field of this class will be passed
    as a var named 'origin_ci_aws' + field_name.
    """

    def __init__(
            self,
            master_subnet_ids=None,
            etcd_security_group_ids=None,
            node_security_group_ids=None,
            master_security_group_ids=None,
            master_external_elb_security_group_ids=None,
            master_internal_elb_security_group_ids=None,
            router_security_group_ids=None,
            router_elb_security_group_ids=None,
            identifying_tag_key=DEFAULT_IDENTIFYING_TAG_KEY,
            master_subnet_tag_value=DEFAULT_MASTER_SUBNET_TAG_VALUE,
            etcd_security_group_tag_value=DEFAULT_ETCD_SECURITY_GROUP_TAG_VALUE,
            node_security_group_tag_value=DEFAULT_NODE_SECURITY_GROUP_TAG_VALUE,
            master_security_group_tag_value=DEFAULT_MASTER_SECURITY_GROUP_TAG_VALUE,
            master_external_elb_security_group_tag_value=DEFAULT_MASTER_EXTERNAL_ELB_SECURITY_GROUP_TAG_VALUE,
            master_internal_elb_security_group_tag_value=DEFAULT_MASTER_INTERNAL_ELB_SECURITY_GROUP_TAG_VALUE,
            router_security_group_tag_value=DEFAULT_ROUTER_SECURITY_GROUP_TAG_VALUE,
            router_elb_security_group_tag_value=DEFAULT_ROUTER_ELB_SECURITY_GROUP_TAG_VALUE,
            master_instance_type=DEFAULT_MASTER_INSTANCE_TYPE,
            region=DEFAULT_REGION,
            master_root_volume_size=DEFAULT_MASTER_ROOT_VOLUME_SIZE,
    ):
        # literal AWS EC2 object identifiers
        self.master_subnet_ids = master_subnet_ids
        self.etcd_security_group_ids = etcd_security_group_ids
        self.node_security_group_ids = node_security_group_ids
        self.master_security_group_ids = master_security_group_ids
        self.master_external_elb_security_group_ids = master_external_elb_security_group_ids
        self.master_internal_elb_security_group_ids = master_internal_elb_security_group_ids
        self.router_security_group_ids = router_security_group_ids
        self.router_elb_security_group_ids = router_elb_security_group_ids

        # the tag key and tag values for identifying
        # pre-existing EC2 objects for these cluster
        # roles without specifying literal EC2 IDs.
        self.identifying_tag_key = identifying_tag_key
        self.master_subnet_tag_value = master_subnet_tag_value
        self.etcd_security_group_tag_value = etcd_security_group_tag_value
        self.node_security_group_tag_value = node_security_group_tag_value
        self.master_security_group_tag_value = master_security_group_tag_value
        self.master_external_elb_security_group_tag_value = master_external_elb_security_group_tag_value
        self.master_internal_elb_security_group_tag_value = master_internal_elb_security_group_tag_value
        self.router_security_group_tag_value = router_security_group_tag_value
        self.router_elb_security_group_tag_value = router_elb_security_group_tag_value

        # other parameters for setting up the cluster
        self.region = region
        self.master_instance_type = master_instance_type
        self.master_root_volume_size = master_root_volume_size

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

    def default(self, playbook_variables=None):
        """
        Default unset values in the Ansible extra playbook
        variables using values loaded from serialized or
        default configurations.

        Values will have the following precedence:
            - given literal ID
            - recorded literal ID
            - given tag value
            - recorded tag value

        :param playbook_variables: partially-filled variables
        :return: defaulted Ansible extra playbook variables
        """
        if playbook_variables is None:
            playbook_variables = {}

        id_suffix = '_ids'
        tag_value_suffix = '_tag_value'
        for id_field in [key for key in self.__dict__ if key.endswith(id_suffix)]:
            component = id_field[:-len(id_suffix)]
            tag_field = '{}{}'.format(component, tag_value_suffix)
            id_variable = '{}{}'.format(_aws_variable_prefix, id_field)
            tag_variable = '{}{}'.format(_aws_variable_prefix, tag_field)

            if id_variable not in playbook_variables and self.__dict__[id_field] is not None:
                playbook_variables[id_variable] = self.__dict__[id_field]

            if tag_variable not in playbook_variables and self.__dict__[tag_field] is not None:
                playbook_variables[tag_variable] = self.__dict__[tag_field]

        for other_field in [key for key in self.__dict__ if not key.endswith(id_suffix) and not key.endswith(tag_value_suffix)]:
            variable = '{}{}'.format(_aws_variable_prefix, other_field)
            if variable not in playbook_variables:
                playbook_variables[variable] = self.__dict__[other_field]

        return playbook_variables
