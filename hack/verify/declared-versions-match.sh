#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

oct_root="$( realpath "$( dirname "${BASH_SOURCE[0]}" )/../.." )"

pushd "${oct_root}" >/dev/null 2>&1

declare setup_version cli_version
if ! setup_version="$( grep -Po "(?<=version=').*(?=',)" setup.py )"; then
    echo "No version declaration found in setup.py!"
    exit 1
fi

if ! cli_version="$( grep -Po "(?<=^VERSION = ').*(?='$)" oct/cli/version.py )"; then
    echo "No version declaration found in oct/cli/version.py!"
    exit 1
fi

if [[ "${setup_version}" != "${cli_version}" ]]; then
    echo "Version mismatch! Found ${setup_version} in setup.py and ${cli_version} in oct/cli/version.py!"
    exit 1
fi

echo "Versions match!"

popd  >/dev/null 2>&1