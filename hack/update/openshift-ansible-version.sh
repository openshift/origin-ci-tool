#!/bin/bash

pushd oct/ansible/openshift-ansible 2>&1 >/dev/null
git fetch origin
git rebase origin/master
description="$( git describe )"
sed -i "s/^OPENSHIFT_ANSIBLE_VERSION.*/OPENSHIFT_ANSIBLE_VERSION = '${description}'/" ./../../cli/version.py
hash="$( git log -1 --pretty=format:%H )"
sed -i "s/^OPENSHIFT_ANSIBLE_CHECKOUT.*/OPENSHIFT_ANSIBLE_CHECKOUT = '${hash}'/" ./../../cli/version.py
popd 2>&1 >/dev/null

git add --all oct/ansible/openshift-ansible/
git add oct/cli/version.py
git commit --signoff -S -m "Update openshift-ansible submodule to ${hash}"$'\n\n'"Current HEAD is now at ${description}"
