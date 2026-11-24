
def count_kmers(L, k):
    """서열 길이 L에서 k-mer의 개수를 계산한다."""
    if k > L:
        return 0

    return L - k + 1


# 여러 가지 L과 k 조합으로 확인
print("L=10, k=5:", count_kmers(10, 5))
print("L=10, k=3:", count_kmers(10, 3))
print("L=15, k=5:", count_kmers(15, 5))
print("L=20, k=4:", count_kmers(20, 4))
print("L=5, k=8:", count_kmers(5, 8))
