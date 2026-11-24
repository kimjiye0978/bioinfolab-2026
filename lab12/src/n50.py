import sys
import os

# 저장소 규칙: FASTA 는 lab07/src/fasta.py 의 read_fasta 로 읽는다.
# 이 파일(lab12/src/n50.py) 위치에서 ../../lab07/src 폴더를 찾아 import 경로에 추가한다.
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "lab07", "src"))
from fasta import read_fasta


def n50(lengths):
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    half = total / 2

    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length


seqs = read_fasta(sys.argv[1])
lengths = []
for name in seqs:
    lengths.append(len(seqs[name]))

print("contig 개수:", len(lengths))
print("전체 길이:", sum(lengths))
print("가장 긴 contig:", max(lengths))
print("N50:", n50(lengths))

# 모든 contig 길이를 내림차순(긴 것부터)으로 정렬해 한 줄에 하나씩 저장한다.
out_file = os.path.join(here, "..", "doc", "contig_lengths.txt")
with open(out_file, "w") as out:
    for length in sorted(lengths, reverse=True):
        out.write(str(length) + "\n")
print("저장 완료:", out_file)
