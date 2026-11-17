# qual_by_position.py 사용법 및 설명서

- 위치: `lab11/src/qual_by_position.py`
- 목적: FASTQ 파일의 모든 read를 모아 **위치(사이클)별 평균 품질 점수**를 계산한다. FastQC의 "Per base sequence quality" 그래프를 숫자 표로 직접 만들어 보는 프로그램이다.
- 필요한 것: Python 3 (표준 라이브러리 `sys`만 사용, 추가 설치 없음)

---

## 1. 빠른 사용법

`lab11` 폴더에서 다음과 같이 실행한다.

```bash
python3 src/qual_by_position.py data/SRR1553607_1.fastq
```

형식:

```bash
python3 src/qual_by_position.py <FASTQ 파일 경로>
```

결과를 파일로 저장하려면 `>`(출력 방향 바꾸기)를 쓴다. 탭으로 구분된 표라서 엑셀이나 pandas로 바로 열 수 있다.

```bash
python3 src/qual_by_position.py data/SRR1553607_1.fastq > qual_pos_1.tsv
```

### 실행 결과 예시 (일부)

```
위치	read수	평균품질	판정
1	203445	32.04
2	203445	32.17
3	203445	32.28
4	203445	35.85
...
99	203445	29.03
100	203445	28.93
101	203445	28.25
# 전체 염기 평균 품질: 33.45
```

| 출력 열 | 의미 |
|---|---|
| 위치 | read 안에서 몇 번째 염기인지 (1부터 센다) |
| read수 | 그 위치까지 길이가 닿는 read의 수 |
| 평균품질 | 그 위치에 있는 모든 염기의 평균 Phred 점수 |
| 판정 | 평균이 **Q20 미만**이면 `LOW` 표시, 아니면 빈칸 |
| 마지막 줄 | 파일 전체 염기의 평균 품질 |

---

## 2. 테스트 결과

### 2-1. 손으로 계산할 수 있는 예제

품질 문자열 `IIIIIIII#####IIIIIIIIII` 하나만 있는 FASTQ로 시험했다.

```
@r1
ACGTACGTAGCTACGTACGTACG
+
IIIIIIII#####IIIIIIIIII
```

| 위치 | 글자 | 계산 | 결과 |
|---|---|---|---|
| 1–8 | `I` | 73 - 33 | 40.00 |
| 9–13 | `#` | 35 - 33 | 2.00 `LOW` |
| 14–23 | `I` | 73 - 33 | 40.00 |
| 전체 | | (40×18 + 2×5) / 23 | **31.74** |

프로그램 출력이 손 계산과 정확히 일치했다.

### 2-2. 길이가 다른 read

read `a`(품질 `IIII`, 길이 4)와 read `b`(품질 `##`, 길이 2)를 넣었다.

| 위치 | read수 | 평균품질 | 계산 |
|---|---|---|---|
| 1 | 2 | 21.00 | (40 + 2) / 2 |
| 2 | 2 | 21.00 | (40 + 2) / 2 |
| 3 | 1 | 40.00 | read `a`만 있음 |
| 4 | 1 | 40.00 | read `a`만 있음 |

전체 평균은 (40×4 + 2×2) / 6 = **27.33**으로 기대값과 같았다. 트리밍 후처럼 read 길이가 제각각이어도 올바르게 계산된다.

### 2-3. 오류 상황

| 상황 | 결과 |
|---|---|
| 파일 이름 없이 실행 | `사용법: ...` 메시지 출력 후 종료 (종료 코드 1) |
| 빈 파일 | `read가 없습니다: ...` 출력 후 종료 (종료 코드 1) |

### 2-4. 수업 데이터 (실행 시간 약 3초)

| 파일 | read 수 | 1번 위치 | 101번 위치 | 전체 평균 | LOW 위치 |
|---|---|---|---|---|---|
| `SRR1553607_1.fastq` | 203,445 | 32.04 | 28.25 | 33.45 | 없음 |
| `SRR1553607_2.fastq` | 203,445 | 30.03 | 25.78 | 30.83 | 없음 |
| `trimmed.fastq` | 188,357 | 32.28 | 30.17 | 34.91 | 없음 |

- `SRR1553607_1.fastq`의 전체 평균 33.45는 `qual_summary.py`의 결과(33.4497)와 같다. 모든 read 길이가 101이라 "read 평균의 평균"과 "전체 염기 평균"이 같기 때문이다.
- 세 파일 모두 **3′ 끝(뒤쪽 위치)으로 갈수록 품질이 떨어진다**. Illumina 시퀀싱의 전형적인 모습이다.
- `trimmed.fastq`는 101번 위치의 read 수가 171,032개로 줄었다. 트리밍으로 뒤쪽이 잘린 read가 있다는 뜻이다. 품질이 낮은 끝부분이 잘려 나가서 101번 위치 평균도 28.25에서 30.17로 올랐다.

---

## 3. 코드 설명

프로그램은 세 부분으로 나뉜다.

1. `read_fastq()`: 파일을 읽어 read 목록을 만든다. (`qual_summary.py`와 같은 함수)
2. `qual_by_position()`: 위치별 점수 합계와 read 수를 모아 평균을 낸다.
3. 메인 부분(`if __name__ == "__main__":`): 입력을 확인하고 표를 출력한다.

### 3-1. `qual_by_position(reads)` 함수

```python
def qual_by_position(reads):
    totals = []  # totals[i] = i번째 위치의 품질 점수 합계
    counts = []  # counts[i] = i번째 위치까지 길이가 닿는 read 수

    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            if i == len(totals):
                totals.append(0)
                counts.append(0)
            totals[i] = totals[i] + (ord(ch) - 33)  # Phred+33
            counts[i] = counts[i] + 1

    result = []
    for i in range(len(totals)):
        result.append((i + 1, counts[i], totals[i] / counts[i]))
    return result
```

| 코드 | 설명 |
|---|---|
| `totals = []`, `counts = []` | 위치마다 점수 합계와 read 수를 담을 리스트. 인덱스 `i`가 위치를 뜻한다 |
| `for name, seq, qual in reads:` | read를 하나씩 꺼내 세 변수로 나누어 받는다 (**언패킹**) |
| `for i, ch in enumerate(qual):` | 품질 문자열에서 **위치 번호 `i`(0부터)와 글자 `ch`**를 함께 꺼낸다 |
| `if i == len(totals):` | 지금까지 본 read보다 더 긴 위치에 처음 왔다면 |
| `totals.append(0)` | 리스트를 한 칸 늘려 0으로 시작한다 |
| `ord(ch) - 33` | 글자를 Phred+33 규칙으로 품질 점수로 바꾼다 |
| `totals[i] = totals[i] + ...` | 그 위치의 합계에 더한다 |
| `counts[i] = counts[i] + 1` | 그 위치의 read 수를 1 늘린다 |
| `totals[i] / counts[i]` | 합계 ÷ 개수 = 그 위치의 평균 |
| `i + 1` | 사람이 읽기 쉽게 위치를 1부터 센다 |

#### 왜 점수를 리스트에 다 모으지 않고 "합계"만 더하나?

위치별 평균을 내는 데 필요한 것은 **합계와 개수** 두 숫자뿐이다. 20만 개 read의 점수를 위치마다 전부 저장하면 2천만 개가 넘는 숫자를 메모리에 올려야 하지만, 합계만 더하면 위치마다 숫자 두 개(101 × 2개)면 충분하다.

#### `enumerate()` 복습

```python
for i, ch in enumerate("IB#"):
    print(i, ch)
# 0 I
# 1 B
# 2 #
```

`enumerate()`는 반복할 때 **순번과 값을 함께** 준다. 위치 번호가 필요할 때 쓴다.

### 3-2. 메인 부분

```python
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 src/qual_by_position.py <FASTQ 파일>")
        sys.exit(1)

    reads = read_fastq(sys.argv[1])
    if len(reads) == 0:
        print("read가 없습니다:", sys.argv[1])
        sys.exit(1)

    table = qual_by_position(reads)

    print("위치\tread수\t평균품질\t판정")
    for pos, n, mean in table:
        mark = "LOW" if mean < 20 else ""
        print(f"{pos}\t{n}\t{mean:.2f}\t{mark}")
```

| 코드 | 설명 |
|---|---|
| `if __name__ == "__main__":` | 직접 실행할 때만 아래 코드를 실행한다. 다른 파일에서 `import`하면 함수만 가져다 쓸 수 있다 (`lab07/src/fasta.py`와 같은 방식) |
| `len(sys.argv) < 2` | 파일 이름을 주지 않았는지 확인한다 |
| `sys.exit(1)` | 프로그램을 끝낸다. `1`은 "문제가 있었다"는 뜻의 종료 코드 |
| `"\t"` | 탭 문자. 열을 탭으로 나누면 표 형식(TSV)이 된다 |
| `"LOW" if mean < 20 else ""` | **조건 표현식**: 조건이 참이면 앞 값, 거짓이면 뒤 값 |
| `f"{mean:.2f}"` | f-string 서식. `:.2f`는 소수점 아래 두 자리까지 표시 |

### 3-3. 전체 염기 평균

```python
total_sum = 0
total_n = 0
for pos, n, mean in table:
    total_sum = total_sum + mean * n
    total_n = total_n + n
print(f"# 전체 염기 평균 품질: {total_sum / total_n:.2f}")
```

`평균 × 개수 = 합계`이므로, 위치별 합계를 다시 모아 전체 염기 수로 나눈다. read 길이가 달라도 **모든 염기를 똑같은 무게로** 평균 낸 값이 된다.

---

## 4. 결과 해석하기

| 평균 Q | 염기가 틀렸을 확률 | 판단 |
|---|---|---|
| 30 이상 | 1/1,000 이하 | 좋음 |
| 20 ~ 30 | 1/100 ~ 1/1,000 | 보통 |
| 20 미만 | 1/100 초과 | 나쁨 (`LOW`), 트리밍 대상 |

- **뒤쪽 위치가 점점 떨어지는 경우**: 정상적인 Illumina 패턴이다. 품질이 많이 낮으면 3′ 끝을 트리밍한다.
- **가운데 특정 위치만 떨어지는 경우**: 장비나 flow cell 문제일 수 있다. FastQC의 "Per tile sequence quality"도 함께 확인한다.
- **1~3번 위치가 조금 낮은 경우**: 수업 데이터처럼 처음 몇 사이클은 품질이 약간 낮게 나오는 일이 흔하다.

이 프로그램은 위치별 **평균**만 보여 준다. 평균이 높아도 일부 read는 품질이 나쁠 수 있다. FastQC 상자 그림의 아래쪽 수염(하위 10%)이 그런 read를 보여 준다.

---

## 5. 주의할 점과 한계

1. **Phred+33만 가정**:
   오래된 Illumina 데이터(Phred+64)를 넣으면 점수가 31만큼 높게 계산된다.
2. **줄 수가 4의 배수가 아니면 오류**:
   잘린 파일이면 `lines[i + 3]`이 없어 `IndexError`가 날 수 있다.
3. **메모리 사용**:
   `readlines()`가 파일 전체를 메모리에 올린다. 수업 데이터는 괜찮지만 수 GB 크기의 FASTQ에서는 메모리가 부족할 수 있다.
4. **뒤쪽 위치는 read 수가 적을 수 있다**:
   트리밍한 파일에서는 뒤쪽 위치의 `read수`가 줄어든다. read 수가 아주 적은 위치의 평균은 믿기 어려우므로 `read수` 열을 함께 본다.
5. **`LOW` 기준은 Q20으로 고정**:
   다른 기준을 쓰려면 코드의 `mean < 20`의 숫자를 바꾼다.

---

## 6. 수업 데이터 실행 명령

```bash
python3 src/qual_by_position.py data/SRR1553607_1.fastq
python3 src/qual_by_position.py data/SRR1553607_2.fastq
python3 src/qual_by_position.py data/trimmed.fastq
```
