# coding=utf-8


def value_for_tag(tags, key):
    """
    Look up the tag matching the provided key

    :param tags: An array of Key/Value pairs as returned by Boto3,
                 like [{'Key': 'k', 'Value': 'v'}]
    :param key: A string representing the desired Key to look up
    """
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
    return ""


def image_info(image):
    """
    Return a formatted string identifying the given image

    :param image: a data structure representing an AWS AMI
    """
    infostr = ""
    name_tag = value_for_tag(image['Tags'], 'Name')
    if name_tag:
        infostr += "{} ".format(name_tag)
    infostr += "({})".format(image['ImageId'])
    return infostr
