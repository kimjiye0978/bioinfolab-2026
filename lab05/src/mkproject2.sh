#!/usr/bin/bash

# 프로젝트 이름을 받아 프로젝트 폴더를 만드는 스크립트

if [ $# -eq 0 ]
then
    echo "사용법: $0 프로젝트이름"
    exit 1
fi

NAME="$1"

if [ -d "$NAME" ]
then
    echo "오류: $NAME 폴더가 이미 존재합니다."
    exit 1
fi

mkdir "$NAME"
echo "$NAME 폴더를 만들었습니다"
