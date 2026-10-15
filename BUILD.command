#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if [ "$#" -gt 0 ]; then
  base="$1"
else
  printf 'Path to Japanese ROM (CRC32 CCAA4853): '
  IFS= read -r base
fi
python3 build.py "$base"
python3 -m unittest discover -s tests -v
