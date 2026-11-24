import sys
from parse_gff import read_gff

# GFF 파일을 읽어 모든 주석을 가져온다
features = read_gff(sys.argv[1])

# 1. type이 CDS인 주석만 골라낸다
cds_list = []
for f in features:
    if f["type"] == "CDS":
        cds_list.append(f)

# 2. 각 CDS의 길이를 end - start + 1 로 계산한다
#    (GFF 좌표는 1부터 시작하고 양 끝을 모두 포함하므로 1을 더한다)
lengths = []
for f in cds_list:
    length = f["end"] - f["start"] + 1
    f["length"] = length
    lengths.append(length)

# 3. 개수, 평균, 최소, 최대 길이를 출력한다
n = len(lengths)
mean_len = sum(lengths) / n

print("CDS 개수:", n)
print("평균 길이:", round(mean_len, 1), "bp")
print("최소 길이:", min(lengths), "bp")
print("최대 길이:", max(lengths), "bp")

# 평균 길이를 3으로 나누면 평균 아미노산 개수 (세균은 대략 300 근처)
print("평균 아미노산 개수:", round(mean_len / 3, 1))

# 4. 정방향(+)과 역방향(-)의 개수를 센다
plus = 0
minus = 0
for f in cds_list:
    if f["strand"] == "+":
        plus = plus + 1
    elif f["strand"] == "-":
        minus = minus + 1

print("정방향(+):", plus)
print("역방향(-):", minus)

# 5. 가장 긴 CDS 다섯 개의 좌표와 attributes를 출력한다
#    key=... 로 "length" 값을 기준으로 정렬하고, reverse=True 로 큰 것부터 정렬
longest = sorted(cds_list, key=lambda f: f["length"], reverse=True)

print()
print("가장 긴 CDS 5개:")
for f in longest[:5]:
    print(f["seqid"], f["start"], f["end"], f["strand"], f["length"], sep="\t")
    print("  ", f["attributes"])
