# lab10/data 의 rbcL_*.gb 파일을 읽어서
# 파일 이름, VERSION, ORGANISM, CDS 위치, 번역 결과 일치 여부를 탭으로 구분해 출력한다.
# 사용법: python src/check_cds.py   (lab10 폴더에서 실행)

import glob
import os
from Bio import SeqIO
from Bio.SeqFeature import ExactPosition

# 이 스크립트 위치를 기준으로 data 폴더를 찾는다 (어느 폴더에서 실행해도 동작하도록)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def translate_cds(record, feature):
    """CDS 를 table=11 로 번역한다. codon_start, 불완전(partial) CDS 를 고려한다."""
    seq = feature.extract(record.seq)

    # /codon_start 가 2 나 3 이면 앞의 1~2 염기를 건너뛴다
    codon_start = int(feature.qualifiers.get("codon_start", ["1"])[0])
    seq = seq[codon_start - 1:]

    # 길이가 3의 배수가 아니면 끝의 남는 염기를 잘라 낸다 (부분 서열인 경우)
    seq = seq[: len(seq) // 3 * 3]

    # 시작 위치가 정확(<1 처럼 잘리지 않음)하고 codon_start 가 1 이면 완전한 시작 코돈이 있다.
    # 이때 GTG, TTG 같은 대체 시작 코돈도 M 으로 번역되어야 하므로 첫 아미노산을 M 으로 바꾼다.
    complete_start = isinstance(feature.location.start, ExactPosition) and codon_start == 1
    if feature.location.strand == -1:
        complete_start = isinstance(feature.location.end, ExactPosition) and codon_start == 1

    protein = str(seq.translate(table=11))
    if complete_start and protein:
        protein = "M" + protein[1:]

    # 끝의 종결 코돈(*)은 /translation 에 포함되지 않으므로 제거한다
    return protein.rstrip("*")


# 헤더 출력
print("\t".join(["file", "version", "organism", "cds_location", "translation_match"]))

for path in sorted(glob.glob(os.path.join(DATA_DIR, "rbcL_*.gb"))):
    filename = os.path.basename(path)

    # 파일 하나에 레코드가 여러 개 있을 수도 있으므로 parse 로 모두 읽는다
    for record in SeqIO.parse(path, "genbank"):
        version = record.id                                  # VERSION 줄 (예: OK432498.1)
        organism = record.annotations.get("organism", "NA")  # ORGANISM 줄

        cds_list = [f for f in record.features if f.type == "CDS"]
        if not cds_list:
            # CDS 주석이 없는 레코드도 빠뜨리지 않고 표시한다
            print("\t".join([filename, version, organism, "CDS 없음", "NA"]))
            continue

        for cds in cds_list:
            location = str(cds.location)
            if "translation" not in cds.qualifiers:
                match = "translation 없음"
            else:
                expected = cds.qualifiers["translation"][0]
                match = str(translate_cds(record, cds) == expected)
            print("\t".join([filename, version, organism, location, match]))
