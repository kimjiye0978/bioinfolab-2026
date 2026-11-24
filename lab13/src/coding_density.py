import sys
import os

# lab07/src 폴더를 모듈 검색 경로에 추가해서 read_fasta 를 가져온다
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "lab07", "src"))
from fasta import read_fasta
from parse_gff import read_gff

# 사용법: python3 src/coding_density.py data/contigs.fa doc/prokka_out/sample.gff
fasta_file = sys.argv[1]
gff_file = sys.argv[2]

# 1. 전체 유전체 길이 = 모든 contig 길이의 합
seqs = read_fasta(fasta_file)
genome_len = 0
for name in seqs:
    genome_len = genome_len + len(seqs[name])

# 2. CDS 개수와 CDS 길이의 총합
features = read_gff(gff_file)
cds_count = 0
cds_total = 0
for f in features:
    if f["type"] == "CDS":
        cds_count = cds_count + 1
        # GFF 좌표는 1부터 시작하고 양 끝을 포함하므로 1을 더한다
        cds_total = cds_total + (f["end"] - f["start"] + 1)

# 3. 1000 염기(1 kb)당 유전자 수
genes_per_kb = cds_count / genome_len * 1000

# 4. 코딩 밀도 = CDS 길이 총합 / 유전체 길이 * 100
coding_density = cds_total / genome_len * 100

print("전체 유전체 길이:", genome_len, "bp")
print("CDS 개수:", cds_count)
print("1000 염기당 유전자 수:", round(genes_per_kb, 3))
print("CDS 길이 총합:", cds_total, "bp")
print("코딩 밀도:", round(coding_density, 2), "%")
