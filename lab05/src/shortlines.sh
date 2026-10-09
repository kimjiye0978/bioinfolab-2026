#!/usr/bin/bash

if [ $# -ne 2 ]
then
    echo "사용법: $0 <FASTA파일> <최소길이>"
    exit 1
fi

FILE="$1"
MIN="$2"

if [ ! -f "$FILE" ]
then
    echo "파일이 존재하지 않습니다: $FILE"
    exit 1
fi

if [ -z "$(echo "$MIN" | grep '^[0-9][0-9]*$')" ]
then
    echo "두 번째 인자는 숫자여야 합니다."
    exit 1
fi

awk -v min="$MIN" '!/^>/ && length($0) < min {count++} END {print count}' "$FILE"
