#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

providers=(
    libvirt
    virtualbox
)

operating_systems=(
    fedora
    centos
)

for provider in "${providers[@]}"; do

    # we only want to bump the version of the box on the last update,
    # so adding new versions of libvirt and virtualbox doesn't take
    # us from e.g. 1.2.0 to 1.4.0 but instead to 1.3.0
    if [[ "${provider}" == "libvirt" ]]; then
        bump="none"
    elif [[ "${provider}" == "virtualbox" ]]; then
        bump="minor"
    fi

    for operating_system in "${operating_systems[@]}"; do
        # to build a `base` image, we start with `bare`
        # and install dependencies
        echo "[INFO] Building ${operating_system} base stage on ${provider}"
        oct provision vagrant --provider "${provider}" --os "${operating_system}" --stage bare
        oct prepare all --for origin/master


        oct package vagrant --upgrade --serve-remote --bump-version "${bump}"

        # to build a `install` image, we start with
        # `base` and build/install repositories
        # TODO: build and install everything, not just Origin
        echo "[INFO] Building ${operating_system} install stage on ${provider}"
        oct build origin
        oct install origin
        oct package vagrant --upgrade --serve-remote --bump-version "${bump}"
        oct provision vagrant --destroy
    done

    # neither virtualization provider seems to clean up
    # the networking bits they set up for themselves, so
    # we need to do so ourselves
    if [[ "${provider}" == "libvirt" ]]; then
        for network in $( sudo virsh net-list --name ); do
            sudo virsh net-destroy "${network}"
        done
    elif [[ "${provider}" == "virtualbox" ]]; then
        VBoxManage hostonlyif remove vboxnet0
    fi
done