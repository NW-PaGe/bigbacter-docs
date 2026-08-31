---
title: Quick Start
layout: page
nav_order: 1
parent: v1.0
permalink: /docs/v1.0/pages/quickstart/
---

# {{ page.title }}
{: .no_toc}

{: .important }
> BigBacter requires [Nextflow](https://www.nextflow.io/docs/latest/install.html) and one of the following container engines: [Docker](https://docs.docker.com/engine/install/), [Podman](https://podman.io/docs/installation), [Apptainer](https://apptainer.org/docs/admin/main/installation.html), [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html).

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. Configure your PopPUNK database

Performed once per species.
{: .fs-5 .fw-300 }

{: .note }
> This example shows how to configure the *E. coli* database. You can find a list of available PopPUNK databases [here](https://github.com/DOH-JDJ0303/bigbacter-nf/blob/main/docs/db_profiles.md) and instructions for how to add your own databases in [Full Instructions]({{ site.baseurl }}/docs/v1.0/pages/fullinstructions/#32-configuring-custom-databases).

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker,escherichia_coli_db \
    -entry PREPARE_DB \
    --db $PWD/db
```

## 2. Prepare your samplesheet

Performed each time.
{: .fs-5 .fw-300 }

{: .note }
> Nextflow requires the use of absolute file paths in samplesheets.

`samplesheet.csv`:

```csv
sample,taxa,assembly,fastq_1,fastq_2
sample1,Acinetobacter_baumannii,sample1.fasta,sample1_R1.fastq.gz,sample1_R2.fastq.gz
sample2,Escherichia_coli,sample2.fasta,sample2_R1.fastq.gz,sample2_R2.fastq.gz
sample3,Staphylococcus_aureus,sample3.fasta,sample3_R1.fastq.gz,sample3_R2.fastq.gz
```

## 3. Run BigBacter

Performed each time.
{: .fs-5 .fw-300 }

{: .note }
> Nextflow versions ≥ 23.10 require that you run `export NXF_SINGULARITY_HOME_MOUNT=true` when running with `-profile singularity` or Gubbins will fail ([issue 7](https://github.com/DOH-JDJ0303/bigbacter-nf/issues/7)).

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker \
    --input $PWD/samplesheet.csv \
    --db $PWD/db \
    --outdir $PWD/results \
    --max_cpus 4 \
    --max_memory 8.GB
```

## 4. Add the new samples to your database

Performed each time.
{: .fs-5 .fw-300 }

{: .note }
> This is the same command as step 3, with the addition of `-resume` and `--push true`.

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker \
    --input $PWD/samplesheet.csv \
    --db $PWD/db \
    --outdir $PWD/results \
    --max_cpus 4 \
    --max_memory 8.GB \
    --push true \
    -resume
```