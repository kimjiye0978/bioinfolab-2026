# paired-end FASTQ 두 파일(_1, _2)이 올바르게 짝을 이루는지 확인하는 스크립트
# 사용법: python src/check_paired.py

file1 = "data/SRR1553607_1.fastq"
file2 = "data/SRR1553607_2.fastq"


# FASTQ 파일을 읽어서 (이름, 서열, 품질) 튜플의 리스트로 돌려준다
# (parse_fastq.py, qual_summary.py 에서 쓴 함수와 같은 방식)
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()

    # FASTQ 는 4줄이 read 하나: 이름 / 서열 / + / 품질
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]   # 맨 앞의 '@' 를 뺀다
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))

    return records


# read 이름에서 mate 표시를 지우고 비교용 기본 이름만 남긴다
# 예) "SRR1553607.1 1 length=101" -> "SRR1553607.1"
#     "SRR1553607.1/1"            -> "SRR1553607.1"
#     "READ7 2:N:0:ACGT"          -> "READ7"
def base_name(name):
    # 공백 뒤(mate 번호, 설명 등)는 버리고 첫 번째 단어만 사용
    words = name.split()
    first = words[0]

    # 끝이 /1 또는 /2 이면 그 두 글자를 잘라낸다
    if first.endswith("/1") or first.endswith("/2"):
        first = first[:-2]

    return first


# 1. 두 파일 읽기
reads1 = read_fastq(file1)
reads2 = read_fastq(file2)

# 2. read 개수 계산
count1 = len(reads1)
count2 = len(reads2)
print(file1, "read 개수:", count1)
print(file2, "read 개수:", count2)

# 3~5. 같은 순서의 read 끼리 이름 비교
# 개수가 다르면 짧은 쪽 길이만큼만 비교할 수 있다
n = min(count1, count2)
mismatch = 0

for i in range(n):
    name1 = reads1[i][0]
    name2 = reads2[i][0]

    if base_name(name1) != base_name(name2):
        mismatch = mismatch + 1
        # 사람이 읽기 쉽게 read 번호는 1부터 센다
        print("이름 불일치 - read", i + 1, ":", name1, "<->", name2)

print("이름이 다른 read 수:", mismatch)

# 6. read 개수가 같은지 확인
if count1 == count2:
    print("read 개수 일치: 예")
else:
    print("read 개수 일치: 아니오 (차이", abs(count1 - count2), "개)")

# 7. 최종 결과
if count1 == count2 and mismatch == 0:
    print("최종 결과: 모든 read 가 같은 순서로 올바르게 짝을 이룹니다.")
else:
    print("최종 결과: 두 파일이 올바르게 짝을 이루지 않습니다.")
