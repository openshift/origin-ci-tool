#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

oct_root="$( dirname "${BASH_SOURCE[0]}" )/../.."

pushd "${oct_root}" >/dev/null 2>&1

for source_file in $( find oct/ -not -path 'oct/ansible/openshift-ansible/*' -not -path 'oct/ansible/oct/roles/aws-up/files/ec2.py' -name '*.py' ); do
    echo "Checking ${source_file} for PEP8 compliance..."
    if ! pycodestyle --show-source --show-pep8 --max-line-length 130 "${source_file}"; then
        failed="true"
    fi
done

popd  >/dev/null 2>&1

if [[ "${failed:-}" == "true" ]]; then
    echo "Source files are not PEP8 compliant!"
    exit 1
else
    echo "Source files are PEP8 compliant!"
    exit 0
fi
