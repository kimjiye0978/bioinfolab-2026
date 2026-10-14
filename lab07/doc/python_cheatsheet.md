# 나의 Bash 치트시트

## 1. 변수와 따옴표

변수에 값을 저장할 때 = 양쪽에 공백을 넣지 않는다.

NAME="my project"
echo "$NAME"

파일이나 폴더 이름에 공백이 있을 수 있으면 변수도 따옴표로 감싼다.

mkdir "$NAME"

내가 했던 실수: DIR = $1처럼 = 양쪽에 공백을 넣어서 오류가 났다.

## 2. 명령줄 인자

스크립트를 실행할 때 입력한 값은 $1, $2처럼 사용한다.

FILE="$1"
grep -c ">" "$FILE"

인자의 개수는 $#으로 확인한다.

if [ $# -ne 2 ]
then
    echo "인자가 2개 필요합니다."
    exit 1
fi

내가 헷갈렸던 점: 파일 이름에 공백이 있을 수 있으므로 "$1"처럼 따옴표를 사용한다.

## 3. 파일과 폴더 확인

파일이 있는지 확인할 때 -f, 폴더가 있는지 확인할 때 -d를 사용한다.

if [ ! -f "$FILE" ]
then
    echo "파일이 없습니다."
    exit 1
fi

if [ ! -d "$DIR" ]
then
    echo "폴더가 없습니다."
    exit 1
fi

## 4. 파이프와 종료 상태

|를 사용하면 앞 명령의 결과를 뒤 명령으로 넘길 수 있다.

ls data | wc -l

$?는 바로 앞 명령의 종료 상태를 확인한다.

grep -c ">" data/seqs.fasta
echo $?

내가 헷갈렸던 점: ls nowhere | wc -l처럼 파이프를 사용하면 앞의 ls가 실패해도 기본적으로 마지막 명령인 wc의 종료 상태가 $?에 남는다.

## 5. 반복문

여러 FASTA 파일을 한꺼번에 처리할 때 for를 사용한다.

for F in data/*.fasta
do
    echo "$F"
    grep -c ">" "$F"
done

내가 했던 실수: for F in ../ data/*.fasta처럼 ../을 잘못 넣어서 디렉터리까지 처리하려고 했다.

## 6. 스크립트를 만드는 다섯 단계

1. 먼저 터미널에서 명령어 하나로 원하는 작업을 해 본다.
2. 반복해서 바뀌는 값을 변수로 만든다.
3. 파일 이름 등을 명령줄 인자로 받도록 바꾼다.
4. 파일 존재 여부와 인자 개수 같은 오류를 확인한다.
5. 정상적인 경우와 잘못된 입력을 모두 실행해 테스트한다.

예를 들어 FASTA 서열 개수를 세는 경우:

grep -c ">" data/seqs.fasta

변수 사용:

FILE="data/seqs.fasta"
grep -c ">" "$FILE"

명령줄 인자 사용:

FILE="$1"
grep -c ">" "$FILE"

마지막으로 입력 검사를 추가한다.

## 7. 내가 자주 하는 실수

- DIR = $1처럼 = 양쪽에 공백을 넣지 않는다.
- 변수나 파일 이름에 공백이 있으면 따옴표를 사용한다.
- for문에서 처리할 파일 범위를 정확하게 쓴다.
- 스크립트를 실행할 때 ./스크립트이름 또는 bash 스크립트이름을 사용한다.

# Bash + Python 치트시트

## 1. 현재 위치 확인

Bash:

```bash
pwd
```

Python:

```python
import os
os.getcwd()
```

---

## 2. 파일 목록 보기

Bash:

```bash
ls
```

Python:

```python
import os
os.listdir()
```

---

## 3. 폴더 만들기

Bash:

```bash
mkdir apple
```

Python:

```python
import os
os.makedirs("apple")
```

---

## 4. 파일 읽기

Bash:

```bash
cat data/seqs.fasta
```

Python:

```python
with open("data/seqs.fasta") as f:
    for line in f:
        print(line.rstrip())
```

---

## 5. 파일을 한 줄씩 처리하기

Bash:

```bash
for F in data/*.fasta
do
    ...
done
```

Python:

```python
import glob

for F in glob.glob("data/*.fasta"):
    ...
```

---

## 6. 문자열 길이

Bash:

```bash
echo "$SEQ" | wc -c
```

Python:

```python
len(seq)
```

---

## 7. 문자열에 특정 글자가 몇 개 있는지 세기

Bash:

```bash
grep -o "G" | wc -l
```

Python:

```python
seq.count("G")
```

---

## 8. 조건문

Bash:

```bash
if [ "$N" -gt 10 ]; then
    echo "크다"
fi
```

Python:

```python
if n > 10:
    print("크다")
```

---

## 9. 반복문

Bash:

```bash
for F in data/*.fasta
do
    echo "$F"
done
```

Python:

```python
for F in files:
    print(F)
```

---

## 10. 변수

Bash:

```bash
NAME="gene1"
echo "$NAME"
```

Python:

```python
name = "gene1"
print(name)
```

---

## 11. 명령행 인자

Bash:

```bash
NAME=$1
```

Python:

```python
import sys

name = sys.argv[1]
```

---

## 12. 문자열 앞뒤 처리

Bash:

```bash
echo "$LINE" | tr -d '\n'
```

Python:

```python
line = line.rstrip()
```

---

## 13. FASTA 헤더 확인

Bash:

```bash
grep "^>" file.fasta
```

Python:

```python
if line.startswith(">"):
    print(line)
```

---

## 14. FASTA 헤더에서 이름 가져오기

Bash:

```bash
...
```

Python:

```python
name = line[1:].split()[0]
```

Bash에서 여러 명령어를 조합하는 것보다 Python에서는 문자열 메서드를 이용해 직접 처리할 수 있다.

---

## 15. 딕셔너리로 이름과 값 저장

Bash:

```bash
...
```

Python:

```python
counts = {}
counts["seqs.fasta"] = 3
```

Bash 변수만으로 여러 파일의 이름과 값을 체계적으로 저장하는 것보다 Python의 딕셔너리가 편리하다.

---

## 16. 파일 존재 확인

Bash:

```bash
if [ -d "$NAME" ]; then
    ...
fi
```

Python:

```python
import os

if os.path.isdir(name):
    ...
```

---

## 17. 여러 폴더 만들기

Bash:

```bash
mkdir apple
mkdir apple/data
mkdir apple/doc
mkdir apple/src
```

Python:

```python
import os

os.makedirs("apple")
os.makedirs("apple/data")
os.makedirs("apple/doc")
os.makedirs("apple/src")
```

---

## 18. 종료

Bash:

```bash
exit 1
```

Python:

```python
import sys

sys.exit(1)
```

---

## 19. 실행 권한

Bash:

```bash
chmod +x script.sh
```

Python:

```bash
chmod +x script.py
```

Python 코드가 아니라 **운영체제의 파일 권한 설정**이므로 Python 문법으로 바꾸는 항목이 아니다.

---

## 20. Bash 명령어 자체

Bash:

```bash
pwd
ls
cd
chmod
```

Python:

```text
직접 대응시키지 않음
```

이런 명령어들은 Bash와 운영체제 환경에서 사용하는 명령어이므로 Python 코드로 그대로 옮길 필요가 없다.

7주차 Python 치트시트

1. 함수 만들기: def

def는 함수를 정의할 때 사용한다. 함수는 반복해서 사용할 코드를 하나로 묶은 것이다.

def 함수이름(매개변수):
    실행할 코드
    return 결과

예시:

def double(x):
    return x * 2

print(double(3))  # 6

2. print와 return의 차이

print는 결과를 화면에 보여 준다.

return은 함수의 결과를 돌려주어 다른 코드에서 사용할 수 있게 한다.

3. 모듈에서 함수 가져오기

from 모듈이름 import 함수이름 형식으로 다른 파일에 정의된 함수를 가져온다.

from fasta import read_fasta, gc_content

위 코드는 fasta.py에 있는 read_fasta와 gc_content 함수를 가져온다.

4. if __name__ == "__main__":

Python 파일을 직접 실행할 때만 특정 코드를 실행하고 싶을 때 사용한다. 다른 파일에서 모듈로 가져오면 해당 블록 안의 코드는 실행되지 않는다.

if __name__ == "__main__":
    print("직접 실행했을 때만 출력")

5. 파일 쓰기 모드 "w"와 "a"

"w": 파일에 새로 쓴다. 기존 파일이 있으면 내용이 지워지고 새 내용으로 덮어쓴다.

"a": 기존 내용 뒤에 추가한다. 기존 내용을 지우지 않는다.

Bash에서 "w"는 > 기호, "a"는 >> 기호와 비슷하다.

with open("result.txt", "w") as out:
    out.write("첫 번째 줄\n")

with open("result.txt", "a") as out:
    out.write("두 번째 줄\n")

echo "첫 번째 줄" > result.txt
echo "두 번째 줄" >> result.txt

6. 오늘 겪은 오류 두 가지

오류 1: TypeError

print("길이: " + len(seq))

문자열과 정수를 +로 연결하려고 해서 발생한다. str(len(seq))로 정수를 문자열로 바꾸면 해결할 수 있다.

print("길이: " + str(len(seq)))

오류 2: IndexError

filename = sys.argv[1]

명령줄에서 파일 이름을 전달하지 않으면 발생할 수 있다. 실행할 때 필요한 인자를 함께 입력한다.

python3 src/fasta.py data/seqs.fasta