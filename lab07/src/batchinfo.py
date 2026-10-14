import sys
import glob
import os
from fasta import read_fasta, length_stats
from fgc import gc_content


if __name__ == "__main__":
    folder = sys.argv[1]
    output_file = sys.argv[2]

    files = sorted(glob.glob(folder + "/*.fasta"))

    with open(output_file, "w") as out:
        out.write("file\tcount\ttotal_length\tmean_gc\n")

        for filename in files:
            seqs = read_fasta(filename)
            stats = length_stats(seqs)

            if len(seqs) > 0:
                mean_gc = sum(
                    gc_content(seq) for seq in seqs.values()
                ) / len(seqs)
            else:
                mean_gc = 0.0

            out.write(f"{os.path.basename(filename)}\t"f"{stats['count']}\t"f"{stats['total']}\t"f"{mean_gc:.4f}\n")

