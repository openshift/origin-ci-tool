#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

oct_root="$( realpath "$( dirname "${BASH_SOURCE[0]}" )/../.." )"

pushd "${oct_root}" >/dev/null 2>&1

for source_file in $( find oct/ -not -path 'oct/ansible/openshift-ansible/*' -not -path 'oct/ansible/oct/roles/aws-up/files/ec2.py' -name '*.py' ); do
    echo "Updating ${source_file} for code formatting compliance..."
    yapf --in-place "${source_file}"
done

popd  >/dev/null 2>&1