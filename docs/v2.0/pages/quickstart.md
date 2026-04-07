---
title: Quick Start
layout: page
nav_order: 1
parent: v2.0
permalink: /docs/v2.0/pages/quickstart/
---

# {{ page.title }}
{: .no_toc}

{: .important}
BigBacter requires [Nextflow](https://www.nextflow.io/docs/latest/install.html) and <ins>one</ins> of the following container engines: [Docker](https://docs.docker.com/engine/install/), [Podman](https://podman.io/docs/installation), [Apptainer](https://apptainer.org/docs/admin/main/installation.html), [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html).

---

## 1. Create your samplesheet

{: .note}
The `taxa`, `assembly`, `fastq_1`, and `fastq_2` columns are optional — leave them empty if the data is unavailable.

`samplesheet.csv`:
```csv
sample,fastq_1,fastq_2,taxa,assembly
sample1,sample1_R1.fastq.gz,sample1_R2.fastq.gz,Staphylococcus aureus,sample1.fasta
sample2,sample2_R1.fastq.gz,sample2_R2.fastq.gz,Escherichia coli,sample2.fasta
sample3,,,Klebsiella pneumoniae,sample3.fasta
sample4,sample4_R1.fastq.gz,sample4_R2.fastq.gz,,
sample5,,,,
```

---

## 2. Run BigBacter

{: .note}
It is no longer necessary to configure a species-specific database before running BigBacter.
```bash
nextflow run NW-PaGe/BigBacter \
    -r main \
    -profile docker \
    --input $PWD/samplesheet.csv \
    --outdir $PWD/results
```

---

## 3. Review your results

Results are saved to a timestamped subdirectory within `--outdir` (e.g., `${outdir}/${timestamp}`). See the [outputs](../outputs/) page for details.

---

## 4. Push your results

Once satisfied with your results, push them to your BigBacter database (set with `--db`). This saves the results so they are included in future runs. Use `--resume` to avoid recomputing results from step 2.
```bash
nextflow run NW-PaGe/BigBacter \
    -r main \
    -profile docker \
    --input $PWD/samplesheet.csv \
    --outdir $PWD/results \
    --push true \
    --resume
```

---

{: .tip}
🔍 Want to learn more? Check out the [Getting Started](../getting_started/) and [Overview](../overview/) pages.