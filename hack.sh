#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

oct provision vagrant --stage=bare
oct bootstrap host
oct prepare all