
import sys
from fasta import read_fasta, length_stats

if __name__ == "__main__":
    seqs = read_fasta(sys.argv[1])
    stats = length_stats(seqs)

    print("서열 개수:", stats["count"])
    print("전체 길이:", stats["total"])
    print("평균 길이:", round(stats["mean"], 2))
    print("가장 짧은 길이:", stats["min"])
    print("가장 긴 길이:", stats["max"])
