#!/bin/bash

# This script interacts with `fdisk` in order to add a partition that uses up
# all of the free space in the block device updated by `virsh vol-resize`.

fdisk_commands=(
    # first, create a new partition
    'n'  # new partition
    'p'  # primary partition type
    ''   # default partition number
    ''   # default partition beginning
    ''   # default partition ending

    # then, set it to be a Linux LVM
    't'  # change a partition type
    ''   # default partition number
    '8e' # select Linux LVM

    # persist the changes and exit
    'p'  # print the partition table
    'w'  # write the partition table
    'q'  # finish
)

IFS=$'\n'
echo "${fdisk_commands[*]}" | fdisk "$1"