import os
import sys

# lab07/src 폴더를 모듈 검색 경로에 추가해서 기존 fasta.py 의 함수를 가져온다.
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "lab07", "src"))
from fasta import reverse_complement

STOPS = ["TAA", "TAG", "TGA"]
 
def find_orfs(seq, frame):
    orfs = []
    start = None
 
    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i + 3]
 
        if codon == "ATG" and start is None:
            start = i
        elif codon in STOPS and start is not None:
            orfs.append((start, i + 3))
            start = None
 
    return orfs
 
seq = sys.argv[1].upper()
rc = reverse_complement(seq)  # 역상보 서열

# 정방향(+) 가닥과 역상보(-) 가닥을 차례로 검사한다.
for strand, s_seq in [("+", seq), ("-", rc)]:
    for frame in [0, 1, 2]:
        orfs = find_orfs(s_seq, frame)
        print("가닥", strand, "틀", frame + 1, ":", orfs)
        for s, e in orfs:
            print("   ", s_seq[s:e], "길이", e - s)
