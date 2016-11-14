#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

providers=(
    libvirt
)

operating_systems=(
    fedora
    centos
)

for provider in "${providers[@]}"; do
    for operating_system in "${operating_systems[@]}"; do
        # to build a `base` image, we start with `bare`
        # and install dependencies
        echo "[INFO] Building \`base\` for ${operating_system} on ${provider}"
        oct provision vagrant --provider "${provider}" --os "${operating_system}" --stage bare
        oct prepare all --for origin/master
        oct package vagrant --upgrade --serve-remote --bump-version minor

        # to build a `install` image, we start with
        # `base` and build/install repositories
        # TODO: build and install everything, not just Origin
        echo "[INFO] Building \`install\` for ${operating_system} on ${provider}"
        oct build origin
        oct install origin
        oct package vagrant --upgrade --serve-remote --bump-version minor
        oct provision vagrant --destroy
    done
done