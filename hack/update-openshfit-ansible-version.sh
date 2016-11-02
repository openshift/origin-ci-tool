#!/bin/bash

git submodule update oct/ansible/openshift-ansible

pushd oct/ansible/openshift-ansible 2>&1 >/dev/null
sed -i "s/^OPENSHIFT_ANSIBLE_VERSION.*/OPENSHIFT_ANSIBLE_VERSION = '$( git describe )'/" ./../../cli/version.py
sed -i "s/^OPENSHIFT_ANSIBLE_CHECKOUT.*/OPENSHIFT_ANSIBLE_CHECKOUT = '$( git log -1 --pretty=format:%H )'/" ./../../cli/version.py
popd 2>&1 >/dev/null