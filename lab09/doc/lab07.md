# lab07 요약: 함수와 파일 저장

lab07에서는 반복되는 FASTA 처리 코드를 **함수**로 묶어 `fasta.py` 모듈로 만들고, 다른 스크립트에서 `import`하여 재사용하는 방법을 익혔다. 또한 분석 결과를 FASTA/TSV **파일로 저장**하는 방법을 연습했다.

## 1. 폴더 구성

| 폴더 | 내용 |
|------|------|
| `src/` | Python 스크립트와 함수 모음(`fasta.py`), 설명서(`README.md`) |
| `data/` | 연습용 FASTA 파일 (`seqs.fasta`, `seqs2.fasta`, `lower.fasta`) |
| `doc/` | Bash + Python 치트시트, 결과 파일(`summary.tsv`, `long.fasta`) |
| `result.tsv` | `batchinfo.py`로 만든 파일별 요약 결과 |

## 2. 함수 기초

- **`print` vs `return`** (`fseqlen.py`): `print`만 하는 함수는 값을 돌려주지 않으므로 결과가 `None`이 된다. 값을 다른 곳에서 쓰려면 `return`을 사용해야 한다.
- **함수 정의와 호출** (`fgc.py`): `gc_content(seq)`처럼 입력을 받아 계산 결과를 돌려주는 함수를 만들었다.

```python
def gc_content(seq):
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
```

## 3. FASTA 도구 상자: `fasta.py`

| 함수 | 입력 | 반환 |
|------|------|------|
| `read_fasta(filename)` | FASTA 파일 경로 | `{이름: 서열}` 딕셔너리 (서열은 대문자로 변환) |
| `gc_content(seq)` | 염기서열 | GC 비율 (0~1), 빈 서열이면 `0.0` |
| `reverse_complement(seq)` | 염기서열 | 역상보 서열 |
| `write_fasta(seqs, filename)` | 딕셔너리, 저장할 파일 이름 | 없음 (FASTA 파일로 저장) |
| `length_stats(seqs)` | 딕셔너리 | `count`, `total`, `mean`, `min`, `max` 통계 딕셔너리 |

- `if __name__ == "__main__":` 블록을 사용해, 직접 실행할 때만 테스트 코드가 동작하고 `import`할 때는 함수만 불러오도록 했다.
- `assert reverse_complement(rc) == seq`처럼 `assert`로 간단한 테스트를 작성했다.

## 4. 모듈을 활용한 스크립트

모든 스크립트는 `from fasta import ...`로 함수를 불러와 사용하며, 파일 이름은 `sys.argv`로 명령줄에서 받는다.

| 스크립트 | 사용법 | 기능 |
|----------|--------|------|
| `countseq2.py` | `python3 countseq2.py <FASTA>` | 서열 개수 출력 (인자 개수·파일 존재 여부 검사, `sys.exit`) |
| `seqlen2.py` | `python3 seqlen2.py <FASTA>` | 서열별 이름과 길이 출력 |
| `stats.py` | `python3 stats.py <FASTA>` | 서열 개수, 전체/평균/최소/최대 길이 출력 |
| `filter.py` | `python3 filter.py <FASTA>` | 길이 20~40, GC 0.4~0.6, N 5개 미만인 서열만 출력 |
| `filter_fasta.py` | `python3 filter_fasta.py <입력> <최소길이> <출력>` | 최소 길이 이상인 서열만 새 FASTA 파일로 저장 |
| `summary.py` | `python3 summary.py <입력> <출력.tsv>` | 서열별 이름·길이·GC를 TSV로 저장 |
| `batchinfo.py` | `python3 batchinfo.py <폴더> <출력.tsv>` | 폴더 안 모든 `*.fasta`의 서열 수·총 길이·평균 GC를 TSV로 저장 |

## 5. 파일 저장

`with open(파일, "w") as out:`으로 파일을 열고 `out.write()`로 한 줄씩 기록한다. 줄 끝에는 `"\n"`, TSV 열 구분에는 `"\t"`를 넣는다.

```python
with open(outfile, "w") as out:
    out.write("name\tlength\tgc\n")
    for name in seqs:
        out.write(name + "\t" + str(len(seqs[name])) + "\t" + str(gc) + "\n")
```

여러 파일을 한꺼번에 처리할 때는 `glob.glob(folder + "/*.fasta")`로 파일 목록을 얻고, `os.path.basename()`으로 경로를 뺀 파일 이름만 기록했다.

## 6. 실행 결과

`summary.py data/seqs.fasta doc/summary.tsv`:

```
name    length  gc
GENE1   30      0.5
GENE2   15      0.4667
GENE3   22      0.5455
```

`batchinfo.py data result.tsv`:

```
file         count  total_length  mean_gc
lower.fasta  2      20            0.6500
seqs.fasta   3      67            0.5040
seqs2.fasta  2      16            0.2500
```

`read_fasta`가 서열을 대문자로 바꾸므로 소문자가 섞인 `lower.fasta`도 GC가 올바르게 계산된다. 다만 이름 줄까지 대문자로 바뀌어 `gene1`이 `GENE1`로 저장된다.

## 7. 치트시트 (`doc/python_cheatsheet.md`)

- **Bash 정리:** 변수와 따옴표, 명령줄 인자(`$1`, `$#`), 파일/폴더 검사(`-f`, `-d`), 파이프와 종료 상태(`$?`), `for` 반복문, 스크립트를 만드는 다섯 단계
- **Bash ↔ Python 대응:** `pwd`↔`os.getcwd()`, `ls`↔`os.listdir()`, `cat`↔`open()`, `for F in *.fasta`↔`glob.glob()`, `wc -c`↔`len()`, `grep -o | wc -l`↔`.count()` 등

## 8. 부족한 점과 개선할 점

- A, T, G, C 이외의 문자(N 등)가 들어오면 `reverse_complement`에서 오류가 난다. 입력 검사 함수가 필요하다.
- `filter.py`는 `fasta.py`를 쓰지 않고 FASTA 읽기 코드를 다시 작성했으며, 길이가 0인 서열이면 0으로 나누기 오류가 난다.
- `batchinfo.py`는 `gc_content`를 `fgc.py`에서 불러오는데, `fgc.py`는 불러올 때 예시 출력이 실행되고 빈 서열 처리도 없다. `fasta.py`의 `gc_content`를 쓰는 것이 낫다.
- `countseq2.py` 뒷부분에 `read_fasta`를 쓰는 코드가 중복으로 남아 있어 개수가 두 번 출력된다.
- `read_fasta`가 이름 줄도 대문자로 바꾸므로, 서열 줄만 대문자로 바꾸도록 고치면 원래 이름을 유지할 수 있다.
