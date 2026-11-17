"""FASTQ 파일에서 위치(사이클)별 평균 품질 점수를 계산한다.

사용법:
    python3 src/qual_by_position.py <FASTQ 파일 경로>
"""
import sys


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 튜플의 리스트로 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def qual_by_position(reads):
    """위치별 품질 점수의 합과 read 수를 모아 위치별 평균 리스트를 돌려준다.

    돌려주는 값: [(위치, read 수, 평균 품질), ...]  (위치는 1부터 센다)
    """
    totals = []  # totals[i] = i번째 위치의 품질 점수 합계
    counts = []  # counts[i] = i번째 위치까지 길이가 닿는 read 수

    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            # 처음 보는 위치라면 리스트를 한 칸 늘린다 (read 길이가 서로 달라도 동작)
            if i == len(totals):
                totals.append(0)
                counts.append(0)
            totals[i] = totals[i] + (ord(ch) - 33)  # Phred+33
            counts[i] = counts[i] + 1

    result = []
    for i in range(len(totals)):
        result.append((i + 1, counts[i], totals[i] / counts[i]))
    return result


if __name__ == "__main__":
    # 파일 이름을 주지 않았으면 사용법을 알려주고 끝낸다
    if len(sys.argv) < 2:
        print("사용법: python3 src/qual_by_position.py <FASTQ 파일>")
        sys.exit(1)

    reads = read_fastq(sys.argv[1])
    if len(reads) == 0:
        print("read가 없습니다:", sys.argv[1])
        sys.exit(1)

    table = qual_by_position(reads)

    # 탭으로 구분한 표 출력 (Q20 미만은 표시)
    print("위치\tread수\t평균품질\t판정")
    for pos, n, mean in table:
        mark = "LOW" if mean < 20 else ""
        print(f"{pos}\t{n}\t{mean:.2f}\t{mark}")

    # 전체 염기 평균 = 모든 점수의 합 / 모든 염기 수
    total_sum = 0
    total_n = 0
    for pos, n, mean in table:
        total_sum = total_sum + mean * n
        total_n = total_n + n
    print(f"# 전체 염기 평균 품질: {total_sum / total_n:.2f}")
