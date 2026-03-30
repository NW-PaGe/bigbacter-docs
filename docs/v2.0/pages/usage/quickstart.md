---
title: Quick Start
layout: page
nav_order: 1
grand_parent: v2.0
parent: Usage Guide
permalink: /docs/v2.0/pages/usage/quickstart/
---

# {{ page.title }}
{: .no_toc}

# TODO

{: .important}
BigBacter requires [Nextflow](https://www.nextflow.io/docs/latest/install.html) and <ins>one</ins> of the following container engines: [Docker](https://docs.docker.com/engine/install/), [Podman](https://podman.io/docs/installation), [Apptainer](https://apptainer.org/docs/admin/main/installation.html), [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html).

## 1. Make your samplesheet:

{: .note}
Samplesheets should use absolute file paths to avoid path resolution errors.

`samplesheet.csv`:
```csv
sample,fastq_1,fastq_2
sample1,sample1_R1.fastq.gz,sample1_R2.fastq.gz
sample2,sample2_R1.fastq.gz,sample2_R2.fastq.gz
```

## 2. Run BigBacter:

{: .note}
This uses the **default reference set**, which includes <span id="taxon-count">[loading]</span> viral taxa ([full list](../../ref_search/index.html)). It is also possible to supply your own reference(s) in the samplesheet or via the `--ref_set` and `--ref_file` parameters ([learn more](../overview/#reference-selection)).
```bash
nextflow run doh-jdj0303/BigBacter \
    -r main \
    -profile docker \
    --input $PWD/samplesheet.csv \
    --outdir $PWD/results
```

## 3. Check the results:
Results can be found in `--outdir`. A good place to start is `BigBacter-summary.csv`. Genome assemblies can be found in `${outdir}/${sample}/assembly/` and metagenomic summary in `${outdir}/${sample}/metagenome` ([learn more](../outputs/)).

{: .tip}
🔍 Want to learn more? Check out the [getting started](../getting_started/) and [overview](../overview/) pages.