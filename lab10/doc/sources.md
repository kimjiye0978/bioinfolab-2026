# 데이터 출처

| 파일               | VERSION    | ORGANISM                               | 길이 (bp) | 확인 방법                                                                                                                                     | 문제 |
| ---------------- | ---------- | -------------------------------------- | ------: | ----------------------------------------------------------------------------------------------------------------------------------------- | -- |
| rbcL_arabidopsis | OK432498.1 | Arabidopsis thaliana                   |    1440 | `grep "^VERSION" data/rbcL_arabidopsis.gb`, `grep "  ORGANISM" data/rbcL_arabidopsis.gb`, `python3 src/fasta.py data/rbcL_arabidopsis.fa` | 없음 |
| rbcL_ginseng     | U50250.1   | Panax quinquefolius                    |    1437 | `grep "^VERSION" data/rbcL_ginseng.gb`, `grep "  ORGANISM" data/rbcL_ginseng.gb`, `python3 src/fasta.py data/rbcL_ginseng.fa`             | 없음 |
| rbcL_fern        | MW620303.1 | Adiantum capillus-veneris              |    1308 | `grep "^VERSION" data/rbcL_fern.gb`, `grep "  ORGANISM" data/rbcL_fern.gb`, `python3 src/fasta.py data/rbcL_fern.fa`                      | 없음 |
| rbcL_ginkgo      | KF221173.1 | Ginkgo biloba                          |    1317 | `grep "^VERSION" data/rbcL_ginkgo.gb`, `grep "  ORGANISM" data/rbcL_ginkgo.gb`, `python3 src/fasta.py data/rbcL_ginkgo.fa`                | 없음 |
| rbcL_liverwort   | LC536762.1 | Marchantia polymorpha subsp. ruderalis |    1399 | `grep "^VERSION" data/rbcL_liverwort.gb`, `grep "  ORGANISM" data/rbcL_liverwort.gb`, `python3 src/fasta.py data/rbcL_liverwort.fa`       | 없음 |
| rbcL_maize       | Z11973.1   | Zea mays                               |    1431 | `grep "^VERSION" data/rbcL_maize.gb`, `grep "  ORGANISM" data/rbcL_maize.gb`, `python3 src/fasta.py data/rbcL_maize.fa`                   | 없음 |
| rbcL_pine        | JQ512595.1 | Pinus thunbergii                       |    1428 | `grep "^VERSION" data/rbcL_pine.gb`, `grep "  ORGANISM" data/rbcL_pine.gb`, `python3 src/fasta.py data/rbcL_pine.fa`                      | 없음 |
| rbcL_rice        | L24073.1   | Oryza sativa                           |    1355 | `grep "^VERSION" data/rbcL_rice.gb`, `grep "  ORGANISM" data/rbcL_rice.gb`, `python3 src/fasta.py data/rbcL_rice.fa`                      | 없음 |

## 확인 결과

* `grep "^VERSION"`으로 GenBank 파일의 버전을 확인하였다.
* `grep "  ORGANISM"`으로 생물의 학명을 확인하였다.
* `python3 src/fasta.py`로 FASTA 파일의 서열 길이를 확인하였다.
* `grep -c ">" data/rbcL_*.fa`로 각 FASTA 파일에 서열이 하나씩 있는지 확인하였다.
* 8개 FASTA 파일의 길이가 모두 1,300~1,500 bp 범위에 포함되는 것을 확인하였다.

