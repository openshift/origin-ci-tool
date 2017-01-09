#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

oct_root="$( realpath "$( dirname "${BASH_SOURCE[0]}" )/../.." )"

pushd "${oct_root}" >/dev/null 2>&1

for source_file in $( find oct/ -not -path 'oct/ansible/openshift-ansible/*' -not -path 'oct/ansible/oct/roles/aws-up/files/ec2.py' -name '*.py' ); do
    echo "Checking ${source_file} for code formatting compliance..."
    difference="$( yapf --diff "${source_file}" 2>&1 )"
    if [[ -n "${difference}" ]]; then
        echo "${difference}"
        failed="true"
    fi
done

popd  >/dev/null 2>&1

if [[ "${failed:-}" == "true" ]]; then
    echo "Source files are not code format compliant!"
    exit 1
else
    echo "Source files are code format compliant!"
    exit 0
fi