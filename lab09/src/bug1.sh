#!/usr/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

DIR="$1"
ls "$DIR"
