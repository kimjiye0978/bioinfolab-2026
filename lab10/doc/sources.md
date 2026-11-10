# 데이터 출처

| 파일 | VERSION | ORGANISM | 길이 (bp) | 확인 방법 | 문제 |
|---|---|---|---:|---|---|
| rbcL_arabidopsis | OK432498.1 | Arabidopsis thaliana | 1440 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | CDS 주석 없음 |
| rbcL_ginseng | U50250.1 | Panax quinquefolius | 1437 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_fern | MW620303.1 | Adiantum capillus-veneris | 1308 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_ginkgo | KF221173.1 | Ginkgo biloba | 1317 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_liverwort | LC536762.1 | Marchantia polymorpha subsp. ruderalis | 1399 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_maize | Z11973.1 | Zea mays | 1431 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_pine | JQ512595.1 | Pinus thunbergii | 1428 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |
| rbcL_rice | L24073.1 | Oryza sativa | 1355 | `grep "^VERSION"`, `grep "  ORGANISM"`, `python3 src/fasta.py` | 없음 |

## CDS 번역 검사 결과

`src/check_cds.py`를 이용하여 8개 GenBank 파일의 CDS를 추출하고, Biopython의 `translate(table=11, to_stop=True)`로 번역한 결과를 GenBank의 `/translation` 정보와 비교하였다.

| 파일 | CDS 위치 | 번역 일치 여부 |
|---|---|---|
| rbcL_arabidopsis | CDS 없음 | NA |
| rbcL_fern | [<0:>1308](+) | True |
| rbcL_ginkgo | [<0:>1317](+) | True |
| rbcL_ginseng | [<0:1437](+) | True |
| rbcL_liverwort | [<0:1399](+) | True |
| rbcL_maize | [0:1431](+) | True |
| rbcL_pine | [0:1428](+) | True |
| rbcL_rice | [34:1240](+) | True |

## 확인 결과

- `grep "^VERSION"`으로 GenBank 파일의 버전을 확인하였다.
- `grep "  ORGANISM"`으로 생물의 학명을 확인하였다.
- `python3 src/fasta.py`로 FASTA 파일의 서열 길이를 확인하였다.
- `grep -c ">" data/rbcL_*.fa`로 각 FASTA 파일에 서열이 하나씩 있는지 확인하였다.
- 8개 FASTA 파일의 길이가 모두 1,300~1,500 bp 범위에 포함되는 것을 확인하였다.
- CDS 번역 비교 결과 7개 종에서 NCBI의 `/translation`과 직접 번역한 결과가 일치하였다.
- 불일치(False)는 0개였다.
- 애기장대(OK432498.1)는 GenBank 기록에 CDS 주석이 없어 번역 비교를 수행할 수 없었다(NA).

검사 결과는 `doc/cds_check.tsv`에 저장하였다.
