---
title: Full Instructions
layout: page
nav_order: 2
parent: v1.0
permalink: /docs/v1.0/pages/fullinstructions/
---

# {{ page.title }}
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 1. Required Inputs

BigBacter requires the following inputs:

1. Sample name
2. Sample taxonomy (species or closer)
3. Sample assembly
4. Sample reads (Illumina paired-end)
5. Species-specific PopPUNK database (a list of pre-made databases can be found [here](https://www.bacpop.org/poppunk/))

{: .highlight }
> BigBacter is designed to be run following general bacterial analysis. Try one of these (in no specific order): [PHoeNIx](https://github.com/CDCgov/phoenix), [Bactopia](https://github.com/bactopia/bactopia), or [TheiaProk](https://github.com/theiagen/public_health_bioinformatics).

## 2. Installing Dependencies

BigBacter requires [Nextflow](https://www.nextflow.io/docs/latest/install.html) and at least one of the following container engines: [Docker](https://docs.docker.com/engine/install/), [Podman](https://podman.io/docs/installation), [Apptainer](https://apptainer.org/docs/admin/main/installation.html), [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html). The examples below use Docker (i.e., `-profile docker`). You can replace this with whichever container engine you decide to use (e.g., `-profile podman`).

{: .note }
> Nextflow versions ≥ 23.10 require that you run `export NXF_SINGULARITY_HOME_MOUNT=true` when running with `-profile singularity` or Gubbins will fail ([issue 7](https://github.com/DOH-JDJ0303/bigbacter-nf/issues/7)).

## 3. Preparing PopPUNK Databases

Performed once per species.
{: .fs-5 .fw-300 }

BigBacter requires a PopPUNK database for each species you plan to analyze. There are several pre-made [databases](https://www.bacpop.org/poppunk/) and instructions for how to create databases on the [PopPUNK webpage](https://poppunk.readthedocs.io/en/latest/index.html).

{: .highlight }
> It is recommended that you configure all PopPUNK databases to a common directory (specified with `--db`). This will allow you to include multiple species on a single run.

### 3.1 Configuring Pre-Made Databases

Below is an example of how to download the pre-made *Escherichia coli* PopPUNK database. You can replace `escherichia_coli_db` with any of the profiles listed [here](https://github.com/DOH-JDJ0303/bigbacter-nf/blob/main/docs/db_profiles.md).

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker,escherichia_coli_db \
    -entry PREPARE_DB \
    --db $PWD/db
```

{: .warning }
> The `all_dbs` profile downloads all available PopPUNK databases (~ 22 GB).

### 3.2 Configuring Custom Databases

Custom databases are added using the `PREPARE_DB` workflow. Below is an example of the samplesheet and command used to configure a custom database. As shown, databases can be supplied as tar.gz, tar.bz, or uncompressed directories.

`custom-dbs_samplesheet.csv`:

```csv
taxa,pp_db
Acinetobacter_baumannii,abaumannii_db.tar.gz
Escherichia_coli,ecoli_db.tar.bz2
Staphylococcus_aureus,staph_db/
Klebsiella_pneumoniae,https://ftp.ebi.ac.uk/pub/databases/pp_dbs/Klebsiella_pneumoniae_v3_refs.tar.bz2
```

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
   -r main \
   -profile docker \
   -entry PREPARE_DB \
   --input custom-dbs_samplesheet.csv \
   --db $PWD/db \
   --max_cpus 4 \
   --max_memory 8.GB
```

## 4. Preparing Your Samplesheet(s)

Performed each time.
{: .fs-5 .fw-300 }

BigBacter accepts assembly and read files in two formats (`--input` and `--ncbi`). Below are examples of both.

### 4.1 Standard Input (`--input`)

The standard input supplies assemblies and reads as file paths.

{: .note }
> Nextflow requires the use of absolute file paths.

`standard-input.csv`:

```csv
sample,taxa,assembly,fastq_1,fastq_2
sample1,Acinetobacter_baumannii,sample1.fasta,sample1_R1.fastq.gz,sample1_R2.fastq.gz
sample2,Escherichia_coli,sample2.fasta,sample2_R1.fastq.gz,sample2_R2.fastq.gz
sample3,Staphylococcus_aureus,sample3.fasta,sample3_R1.fastq.gz,sample3_R2.fastq.gz
```

### 4.2 NCBI Input (`--ncbi`)

Assembly and read files can also be supplied via GenBank and SRA accessions.

`ncbi-input.csv`:

```csv
sample,taxa,assembly,sra
SAMN12769618,Acinetobacter_baumannii,GCF_008632635.1,SRR11176973
```

{: .warning }
> We have observed poor performance when using GenBank assemblies (SKESA) for references, resulting in multiple samples failing QC due to low genome fraction.

## 5. Running the Main BigBacter Workflow

You are now ready to run BigBacter using the samplesheet(s) you prepared above. This is performed in two steps.

### 5.1 Main Analysis

The first step is to perform the main analysis. Below is an example of the command:

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker \
    --input $PWD/standard-input.csv \
    --ncbi $PWD/ncbi.csv \
    --outdir $PWD/results \
    --db $PWD/db
```

### 5.2 Pushing Results

Once your run is complete, the next step is to check the results and make sure everything looks ok. Once you are happy with your results, you can push the new files to your BigBacter database using the command below:

{: .note }
> The only difference between the commands in steps 5.1 and 5.2 is the addition of the `--push true` and `-resume` parameters.

```bash
nextflow run DOH-JDJ0303/bigbacter-nf \
    -r main \
    -profile docker \
    --input $PWD/standard-input.csv \
    --ncbi $PWD/ncbi.csv \
    --outdir $PWD/results \
    --db $PWD/db \
    --push true \
    -resume
```

## 6. Monitoring Your Database

{: .warning }
> Under construction.