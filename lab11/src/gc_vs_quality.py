"""FASTQ 의 각 read 에 대해 GC 비율과 평균 품질을 함께 계산하고,
GC 가 극단적으로 낮은/높은 read 의 품질을 전체 평균과 비교한다.

사용법:
    python3 src/gc_vs_quality.py <FASTQ 파일> [고를 read 수, 기본 10]
"""
import os
import statistics
import sys

# lab07/src 의 fasta.py 에서 gc_content 를 가져온다 (gc_content.py 와 같은 방식)
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "lab07", "src"))
from fasta import gc_content


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


def mean_quality(qual):
    """품질 문자열의 평균 Phred 점수 (Phred+33)."""
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)


def print_group(title, group, overall):
    """고른 read 들을 표로 출력하고 전체 평균과의 차이를 보여 준다."""
    print(f"== {title} ==")
    print("read 이름\t길이\tGC(%)\t평균품질")
    for name, length, gc, q in group:
        print(f"{name}\t{length}\t{gc * 100:.2f}\t{q:.2f}")
    qs = [q for name, length, gc, q in group]
    m = sum(qs) / len(qs)
    print(f"-> 평균 품질 {m:.2f} (전체 {overall:.2f}, 차이 {m - overall:+.2f})")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 src/gc_vs_quality.py <FASTQ 파일> [고를 read 수]")
        sys.exit(1)

    n = 10
    if len(sys.argv) > 2:
        n = int(sys.argv[2])

    # 1) read 마다 (이름, 길이, GC 비율, 평균 품질) 계산
    table = []
    for name, seq, qual in read_fastq(sys.argv[1]):
        if len(seq) == 0:  # 빈 read 는 건너뛴다
            continue
        table.append((name, len(seq), gc_content(seq), mean_quality(qual)))

    if len(table) < n:
        print("read 수가 너무 적습니다:", len(table))
        sys.exit(1)

    # 2) 전체 read 의 평균 품질과 표준편차
    all_q = [q for name, length, gc, q in table]
    overall = statistics.mean(all_q)
    sd = statistics.stdev(all_q)
    print("read 수:", len(table))
    print(f"전체 read 평균 품질: {overall:.2f} (표준편차 {sd:.2f})")
    print()

    # 3) GC 비율(튜플의 세 번째 값) 기준으로 정렬해서 양 끝 n 개를 고른다
    table.sort(key=lambda row: row[2])
    print_group(f"GC 가 가장 낮은 read {n}개", table[:n], overall)
    print_group(f"GC 가 가장 높은 read {n}개", table[-n:], overall)
