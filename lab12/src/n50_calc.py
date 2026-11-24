
contigs = [12, 3, 20, 8, 1, 15, 6]

# contig 길이를 큰 순서대로 정렬
contigs.sort(reverse=True)

# 전체 길이와 50% 기준 계산
total_length = sum(contigs)
half_length = total_length / 2

print("정렬된 contig 길이:", contigs)
print("전체 길이:", total_length)
print("50% 기준:", half_length)

# 누적 길이를 계산하여 N50 찾기
cumulative = 0

for length in contigs:
    cumulative += length
    print("누적 길이:", cumulative)

    if cumulative >= half_length:
        n50 = length
        break

print("N50:", n50)
