#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2:
    print("사용법: python3 src/mkproject.py 프로젝트이름")
    sys.exit(1)

name = sys.argv[1]

if os.path.isdir(name):
    print(f"오류: {name} 폴더가 이미 존재합니다.")
    sys.exit(1)

os.makedirs(name)
os.makedirs(name + "/data")
os.makedirs(name + "/doc")
os.makedirs(name + "/src")

print(f"{name} 프로젝트를 만들었습니다.")
