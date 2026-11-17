# gc_content.py 사용법 및 설명서

- 위치: `lab11/src/gc_content.py`
- 목적: FASTQ 또는 FASTA 파일에 있는 서열들의 **GC 함량(GC 비율)**을 계산하고, 서열별 GC 비율의 분포를 보여 준다. FastQC의 "%GC" 값과 "Per sequence GC content" 그래프를 직접 만들어 보는 프로그램이다.
- 필요한 것: Python 3 (표준 라이브러리 `os`, `sys`만 사용, 추가 설치 없음)
- 함께 쓰는 파일: `lab07/src/fasta.py`의 `read_fasta()`, `gc_content()`

---

## 1. 빠른 사용법

`lab11` 폴더에서 다음과 같이 실행한다.

```bash
python3 src/gc_content.py data/SRR1553607_1.fastq
```

형식:

```bash
python3 src/gc_content.py <FASTQ 또는 FASTA 파일 경로>
```

파일 형식은 **파일의 첫 글자**를 보고 자동으로 정한다.

| 첫 글자 | 판단 |
|---|---|
| `@` | FASTQ |
| `>` | FASTA |
| 그 밖 | 오류 메시지를 출력하고 종료 |

FASTA 파일도 그대로 넣을 수 있다.

```bash
python3 src/gc_content.py ../lab10/data/rbcL_all.fasta
```

### 실행 결과 예시

```
파일 형식: FASTQ
서열 수: 203445
전체 염기 수: 20547945
전체 GC 비율: 58.84%
서열별 GC 평균: 58.84%
서열별 GC 최소: 12.87%
서열별 GC 최대: 98.02%

GC 구간	서열 수	비율
  0-10%	0	  0.0%
 10-20%	54	  0.0%
 20-30%	1559	  0.8%
 30-40%	8998	  4.4% **
 40-50%	27096	 13.3% *******
 50-60%	61447	 30.2% ***************
 60-70%	79766	 39.2% ********************
 70-80%	23491	 11.5% ******
 80-90%	1007	  0.5%
 90-100%	27	  0.0%
```

| 출력 항목 | 의미 |
|---|---|
| 파일 형식 | FASTQ 또는 FASTA |
| 서열 수 | read(또는 FASTA 서열)의 개수 |
| 전체 염기 수 | 모든 서열 길이의 합 |
| 전체 GC 비율 | 모든 염기 중 G와 C의 비율 (= G+C 개수 ÷ 전체 염기 수) |
| 서열별 GC 평균 | 서열마다 구한 GC 비율을 평균 낸 값 |
| 서열별 GC 최소/최대 | GC 비율이 가장 낮은/높은 서열의 값 |
| GC 구간 표 | 서열을 GC 비율 10% 단위 구간으로 나눈 개수와 비율. `*` 하나는 약 2% |

---

## 2. 테스트 결과

### 2-1. 손으로 계산할 수 있는 FASTQ 예제

| read | 서열 | G+C / 길이 | GC 비율 |
|---|---|---|---|
| a | `GGCC` | 4 / 4 | 100% |
| b | `ATAT` | 0 / 4 | 0% |
| c | `acgtGC` (소문자 섞임) | 4 / 6 | 66.67% |
| d | `GCGCGCGCGC` | 10 / 10 | 100% |

| 항목 | 손 계산 | 프로그램 출력 |
|---|---|---|
| 전체 GC 비율 | (4+0+4+10) / 24 = 75.00% | 75.00% |
| 서열별 GC 평균 | (100+0+66.67+100) / 4 = 66.67% | 66.67% |
| 최소 / 최대 | 0% / 100% | 0.00% / 100.00% |
| 구간 | 0-10%: 1, 60-70%: 1, 90-100%: 2 | 같음 |

소문자 서열(`acgt`)도 대문자로 바꿔서 올바르게 셌다. GC 100%인 read도 마지막 구간(90-100%)에 들어갔다.

### 2-2. 손으로 계산할 수 있는 FASTA 예제

```
>s1
ATGC
AT
>s2
ggcc
```

여러 줄로 나뉜 `s1`은 `ATGCAT`로 합쳐져 2/6 = 33.33%, `s2`는 100%가 나왔다. 전체 GC 비율은 6/10 = **60.00%**로 기대값과 같았다.

### 2-3. 오류 상황

| 상황 | 결과 |
|---|---|
| 파일 이름 없이 실행 | `사용법: ...` 출력 후 종료 (종료 코드 1) |
| 빈 파일 | `FASTQ/FASTA 서열이 없습니다: ...` 출력 후 종료 (종료 코드 1) |
| FASTQ/FASTA가 아닌 파일 | 위와 같은 메시지 출력 후 종료 (종료 코드 1) |
| 다른 폴더에서 실행 | 저장소 맨 위 폴더에서 `python3 lab11/src/gc_content.py ...`로 실행해도 `fasta.py`를 정상적으로 찾음 |

### 2-4. 수업 데이터 (실행 시간 각 1초 미만)

| 파일 | 서열 수 | 전체 GC | 최소 | 최대 | 가장 많은 구간 |
|---|---|---|---|---|---|
| `SRR1553607_1.fastq` | 203,445 | 58.84% | 12.87% | 98.02% | 60-70% (39.2%) |
| `SRR1553607_2.fastq` | 203,445 | 59.24% | 10.89% | 99.01% | 60-70% (39.3%) |
| `trimmed.fastq` | 188,357 | 58.95% | 12.87% | 96.43% | 60-70% (40.3%) |
| `lab10/data/rbcL_all.fasta` | 8 | 43.32% | 37.24% | 48.01% | 40-50% (87.5%) |

- FastQC 보고서(`doc/SRR1553607_1_fastqc.html`, `doc/trimmed_fastqc.html`)의 **%GC는 58**이다. FastQC는 소수점 아래를 버리고 정수로 표시하므로 이 프로그램의 58.84%, 58.95%와 맞는다.
- 별도의 짧은 코드로 G, C 개수를 직접 세어 본 값(58.8376%)과도 같았다.
- 분포는 60% 근처에 봉우리가 하나 있는 종 모양이다. 봉우리가 하나뿐이면 다른 생물의 서열이 많이 섞이지 않았다고 볼 수 있다.

---

## 3. 코드 설명

프로그램은 다섯 부분으로 나뉜다.

1. `lab07/src/fasta.py`를 가져오는 부분
2. `read_fastq()`: FASTQ 파일을 읽는다.
3. `read_sequences()`: 첫 글자로 형식을 판단해 서열 리스트를 돌려준다.
4. `gc_histogram()`: GC 비율을 10% 구간으로 센다.
5. 메인 부분: 계산하고 출력한다.

### 3-1. `lab07`의 `fasta.py` 가져오기

저장소 규칙에 따라 FASTA 읽기(`read_fasta`)와 GC 계산(`gc_content`)은 새로 만들지 않고 `lab07/src/fasta.py`의 함수를 그대로 쓴다.

```python
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "lab07", "src"))
from fasta import read_fasta, gc_content
```

`fasta.py`는 `lab11/src`가 아니라 `lab07/src`에 있다. 그래서 그냥 `from fasta import ...`라고 쓰면 파이썬이 파일을 찾지 못한다. 파이썬이 모듈을 찾는 폴더 목록(`sys.path`)에 `lab07/src`를 추가해 주어야 한다.

| 코드 | 설명 |
|---|---|
| `__file__` | 지금 실행 중인 파이썬 파일의 경로 |
| `os.path.abspath(...)` | 상대 경로를 전체(절대) 경로로 바꾼다 |
| `os.path.dirname(...)` | 경로에서 폴더 부분만 꺼낸다 → `.../lab11/src` |
| `os.path.join(here, "..", "..", "lab07", "src")` | 경로 조각을 이어 붙인다. `..`은 "한 단계 위 폴더" → `.../lab11/src/../../lab07/src`, 즉 `.../lab07/src` |
| `sys.path.insert(0, ...)` | 모듈 검색 목록의 맨 앞에 그 폴더를 넣는다 |
| `from fasta import read_fasta, gc_content` | 이제 `lab07/src/fasta.py`에서 두 함수를 가져올 수 있다 |

`__file__`을 기준으로 경로를 만들기 때문에 **어느 폴더에서 실행하든** `fasta.py`를 찾는다. (`lab10`에서는 `fasta.py`를 복사해 왔지만, 이렇게 하면 복사본 없이 원본 하나만 관리하면 된다.)

`fasta.py`의 `gc_content()`는 다음과 같다.

```python
def gc_content(seq):
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다."""
    if len(seq) == 0:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
```

`count()`는 대문자 `"G"`, `"C"`만 센다. 그래서 FASTQ 서열도 읽을 때 `.upper()`로 대문자로 바꾼다. (`read_fasta()`는 이미 안에서 대문자로 바꾼다.)

### 3-2. `read_sequences(filename)` 함수

```python
def read_sequences(filename):
    with open(filename) as f:
        first = f.read(1)
    if first == "@":
        seqs = [seq for name, seq, qual in read_fastq(filename)]
        return "FASTQ", seqs
    if first == ">":
        return "FASTA", list(read_fasta(filename).values())
    return None, []
```

| 코드 | 설명 |
|---|---|
| `f.read(1)` | 파일에서 **한 글자만** 읽는다 |
| `[seq for name, seq, qual in ...]` | **리스트 컴프리헨션**: 튜플마다 `seq`만 골라 새 리스트를 만든다 |
| `read_fasta(filename).values()` | `{이름: 서열}` 딕셔너리에서 서열(값)만 꺼낸다 |
| `list(...)` | 꺼낸 값들을 리스트로 바꾼다 |
| `return "FASTQ", seqs` | 값 두 개를 한꺼번에 돌려준다 (튜플) |
| `return None, []` | 형식을 알 수 없으면 "없음(`None`)"과 빈 리스트를 돌려준다 |

리스트 컴프리헨션은 아래 반복문을 한 줄로 줄인 것이다.

```python
seqs = []
for name, seq, qual in read_fastq(filename):
    seqs.append(seq)
```

### 3-3. `gc_histogram(gc_list)` 함수

```python
def gc_histogram(gc_list):
    bins = [0] * 10
    for gc in gc_list:
        k = int(gc * 10)
        if k == 10:
            k = 9
        bins[k] = bins[k] + 1
    return bins
```

| 코드 | 설명 |
|---|---|
| `[0] * 10` | 0이 10개 든 리스트 `[0, 0, ..., 0]`. 구간 10개의 개수를 담는다 |
| `int(gc * 10)` | GC 비율(0~1)에 10을 곱한 뒤 소수점을 버려 구간 번호를 구한다. 예: 0.588 → 5.88 → **5** (50-60% 구간) |
| `if k == 10: k = 9` | GC가 정확히 100%(1.0)이면 10이 나오므로 마지막 구간(9)에 넣는다 |

### 3-4. 메인 부분: 두 가지 평균

```python
for seq in seqs:
    gc = gc_content(seq)
    gc_list.append(gc)
    total_gc = total_gc + gc * len(seq)
    total_len = total_len + len(seq)
```

| 코드 | 설명 |
|---|---|
| `gc * len(seq)` | GC 비율 × 길이 = 그 서열의 G+C 개수 |
| `total_gc / total_len` | **전체 GC 비율**: 모든 G+C 개수 ÷ 모든 염기 수 |
| `sum(gc_list) / len(gc_list)` | **서열별 GC 평균**: 서열마다 구한 비율의 평균 |

두 값은 서열 길이가 모두 같으면 같고, 길이가 다르면 달라진다. 수업 데이터 원본은 길이가 모두 101이라 두 값이 같다(58.84%). `trimmed.fastq`는 길이가 제각각이라 조금 다르다(58.95% / 58.85%). FastQC의 %GC는 **전체 GC 비율**에 해당한다.

### 3-5. 분포 출력

```python
bar = "*" * round(ratio * 50)
print(f"{k * 10:>3}-{k * 10 + 10}%\t{bins[k]}\t{ratio * 100:5.1f}% {bar}")
```

| 코드 | 설명 |
|---|---|
| `"*" * n` | 문자열을 n번 반복한다. 예: `"*" * 3` → `"***"` |
| `round(ratio * 50)` | 비율 100%를 별 50개로 바꾼다 (별 1개 ≈ 2%) |
| `{k * 10:>3}` | 오른쪽 정렬로 3칸을 차지하게 출력한다 |
| `{ratio * 100:5.1f}` | 전체 5칸, 소수점 아래 1자리로 출력한다 |

---

## 4. 결과 해석하기

- **GC 함량은 생물마다 거의 일정하다.** 예를 들어 사람 게놈은 약 41%, 대장균은 약 51%다. read의 GC 비율이 그 생물의 값과 많이 다르면 오염을 의심한다.
- **분포 모양이 중요하다.**
  - 봉우리 하나(종 모양): 정상
  - 봉우리 두 개 이상: 다른 생물의 서열이 섞였을 가능성 (오염)
  - 아주 뾰족한 봉우리: 어댑터 dimer나 같은 서열이 많이 반복되는 경우
- `rbcL_all.fasta`(엽록체 유전자)의 GC는 약 43%로, SRR1553607 read(약 59%)와 다른 범위다. 서로 다른 생물이나 유전자의 GC 함량이 다를 수 있다는 것을 보여 준다.

---

## 5. 주의할 점과 한계

1. **`N`도 길이에 포함된다**:
   `gc_content()`는 G+C 개수를 서열 **전체 길이**로 나눈다. `N`(모르는 염기)이 많은 read는 GC 비율이 실제보다 낮게 나온다.
2. **첫 글자로만 형식을 판단**:
   파일 맨 앞에 빈 줄이나 공백이 있으면 형식을 알 수 없다고 판단한다.
3. **줄 수가 4의 배수가 아니면 오류**:
   잘린 FASTQ 파일이면 `lines[i + 3]`이 없어 `IndexError`가 날 수 있다.
4. **FASTA에서 이름이 같은 서열**:
   `read_fasta()`는 딕셔너리를 쓰므로 이름이 같은 서열이 있으면 마지막 것만 남는다.
5. **메모리 사용**:
   `readlines()`가 파일 전체를 메모리에 올린다. 수 GB 크기의 FASTQ에서는 메모리가 부족할 수 있다.
6. **`lab07/src/fasta.py`가 필요**:
   폴더 구조를 바꾸거나 `fasta.py`를 옮기면 `ModuleNotFoundError`가 난다.

---

## 6. 수업 데이터 실행 명령

```bash
python3 src/gc_content.py data/SRR1553607_1.fastq
python3 src/gc_content.py data/SRR1553607_2.fastq
python3 src/gc_content.py data/trimmed.fastq
python3 src/gc_content.py ../lab10/data/rbcL_all.fasta
```
