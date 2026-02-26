#!/bin/bash
# Get script file dir
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
buildfile="$script_dir/pypi/build.sh"

source "$buildfile"
