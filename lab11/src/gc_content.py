"""FASTQ 또는 FASTA 파일의 GC 함량(GC 비율)을 계산한다.

사용법:
    python3 src/gc_content.py <FASTQ 또는 FASTA 파일 경로>
"""
import os
import sys

# lab07/src 폴더를 모듈 검색 경로에 추가해서 fasta.py 를 가져온다
# (이 파일 위치: lab11/src → 두 단계 위로 올라가 lab07/src 로 이동)
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "lab07", "src"))
from fasta import read_fasta, gc_content


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 튜플의 리스트로 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip().upper()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def read_sequences(filename):
    """파일 첫 글자로 형식을 판단해 (형식, 서열 리스트)를 돌려준다."""
    with open(filename) as f:
        first = f.read(1)
    if first == "@":
        seqs = [seq for name, seq, qual in read_fastq(filename)]
        return "FASTQ", seqs
    if first == ">":
        return "FASTA", list(read_fasta(filename).values())
    return None, []


def gc_histogram(gc_list):
    """GC 비율(0~1) 리스트를 10% 구간으로 나눠 개수를 센다."""
    bins = [0] * 10  # bins[0] = 0~10%, ..., bins[9] = 90~100%
    for gc in gc_list:
        k = int(gc * 10)
        if k == 10:  # GC 100% 는 마지막 구간에 넣는다
            k = 9
        bins[k] = bins[k] + 1
    return bins


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 src/gc_content.py <FASTQ 또는 FASTA 파일>")
        sys.exit(1)

    kind, seqs = read_sequences(sys.argv[1])
    if kind is None or len(seqs) == 0:
        print("FASTQ/FASTA 서열이 없습니다:", sys.argv[1])
        sys.exit(1)

    # 서열마다 GC 비율 계산 (lab07 의 gc_content 사용)
    gc_list = []
    total_gc = 0
    total_len = 0
    for seq in seqs:
        gc = gc_content(seq)
        gc_list.append(gc)
        total_gc = total_gc + gc * len(seq)  # 비율 × 길이 = G+C 개수
        total_len = total_len + len(seq)

    print("파일 형식:", kind)
    print("서열 수:", len(seqs))
    print("전체 염기 수:", total_len)
    print(f"전체 GC 비율: {total_gc / total_len * 100:.2f}%")
    print(f"서열별 GC 평균: {sum(gc_list) / len(gc_list) * 100:.2f}%")
    print(f"서열별 GC 최소: {min(gc_list) * 100:.2f}%")
    print(f"서열별 GC 최대: {max(gc_list) * 100:.2f}%")

    # GC 분포 (FastQC 의 'Per sequence GC content' 를 글자 막대로)
    print()
    print("GC 구간\t서열 수\t비율")
    bins = gc_histogram(gc_list)
    for k in range(10):
        ratio = bins[k] / len(seqs)
        bar = "*" * round(ratio * 50)
        print(f"{k * 10:>3}-{k * 10 + 10}%\t{bins[k]}\t{ratio * 100:5.1f}% {bar}")
