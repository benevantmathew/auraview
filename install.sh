#!/bin/bash
# Get script file dir
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pip uninstall -y auraview
pip install "$script_dir"
