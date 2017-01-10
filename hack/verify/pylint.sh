#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

oct_root="$( dirname "${BASH_SOURCE[0]}" )/../.."

pushd "${oct_root}" >/dev/null 2>&1

for source_file in $( find oct/ -not -path 'oct/ansible/openshift-ansible/*' -not -path 'oct/ansible/oct/roles/aws-up/files/ec2.py' -name '*.py' ); do
    echo "Checking ${source_file} for PyLint compliance..."
    if ! pylint "${source_file}"; then
        failed="true"
    fi
done

popd  >/dev/null 2>&1

if [[ "${failed:-}" == "true" ]]; then
    echo "Source files are not PyLint compliant!"
    exit 1
else
    echo "Source files are PyLint compliant!"
    exit 0
fi