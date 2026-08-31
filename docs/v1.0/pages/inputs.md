---
title: Inputs
layout: page
nav_order: 4
parent: v1.0
permalink: /docs/v1.0/pages/inputs/
---

# {{ page.title }}
{: .no_toc}

Below is a summary and description of each input parameter.

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## All Input Options

```groovy
// Input options
input                      = "${projectDir}/assets/samplesheet.csv"
ncbi                       = null
db                         = null
push                       = false

// QC: Reads & Assembly
read_qc                    = true
assembly_qc                = true
min_contig_len             = 300

// QC: Variant Calling
max_depth                  = 100
min_genfrac                = 85
max_lowcov                 = 5
max_het                    = 1

// Tree options
max_ml                     = 500
min_tree                   = 2

// Reporting options
strong_link_cutoff         = 10
inter_link_cutoff          = 50
partition_threshold        = 100
max_static                 = 100

// Other options (caution)
db_info                    = true
resolve_merged             = true
run_id                     = null
```

## `--input`

Path to a comma-separated file containing information about PopPUNK databases or samples. An absolute path to the file should be used.

**PopPUNK database sheet example**

`pp_db_list.csv`:

```csv
taxa,pp_db
Acinetobacter_baumannii,abaumannii_db.tar.gz
Escherichia_coli,ecoli_db.tar.bz2
Staphylococcus_aureus,staph_db/
```

**Samplesheet example**

`samplesheet.csv`:

```csv
sample,taxa,assembly,fastq_1,fastq_2
sample1,Acinetobacter_baumannii,sample1.fasta,sample1_R1.fastq.gz,sample1_R2.fastq.gz
sample2,Escherichia_coli,sample2.fasta,sample2_R1.fastq.gz,sample2_R2.fastq.gz
sample3,Staphylococcus_aureus,sample3.fasta,sample3_R1.fastq.gz,sample3_R2.fastq.gz
```

## `--ncbi`

Path to a comma-separated file containing information for samples that should be pulled from NCBI.

```csv
sample,taxa,assembly,sra
SAMN12769618,Acinetobacter_baumannii,GCF_008632635.1,SRR11176973
```

## `--db`

Path to the BigBacter database. It is recommended that PopPUNK databases be configured to a single common directory (i.e., the BigBacter database). This database can be set up automatically using the `PREPARE_DB` workflow (`-entry PREPARE_DB`).

## `--push`

Tells the pipeline whether you want to save (i.e., "push") new samples to the BigBacter database (default: `false`). It is recommended that you check results prior to pushing files. Once confirmed, files can be pushed using `--push true` and `-resume`.

## `--max_depth`

Maximum read depth per sample (default: `100`). This is used by Snippy to randomly subsample reads.

## `--min_genfrac`

Minimum percent of the reference genome that a sample must contain for it to be included in the core SNP analysis (default: `85`).

## `--max_lowcov`

Maximum percent of low coverage sites allowed for a sample to be included in the core SNP analysis (default: `5`).

## `--max_het`

Maximum percent of heterogeneous sites allowed for a sample to be included in the core SNP analysis (default: `1`). Given that bacteria are haploid, the presence of heterogeneous sites indicates either contamination or unrepresented homologs.

## `--strong_link_cutoff`

SNP distance threshold used to classify strong genomic linkages (default: `10`). This has no impact on core SNP analysis and is only meant to aid interpretation of genetic linkages.

## `--inter_link_cutoff`

SNP distance threshold used to classify intermediate genomic linkages (default: `50`). This has no impact on core SNP analysis and is only meant to aid interpretation of genetic linkages.

## `--partition_threshold`

Number of estimated nucleotide substitutions used to partition samples in maximum likelihood trees using `cutree` and `hclust` (default: `100`).

## `--max_static`

Maximum number of samples included in a static image (i.e., `.jpg`). Static images will not be generated for clusters containing more samples than this value.

## `--max_ml`

Maximum number of samples that a cluster can contain for maximum likelihood tree generation (default: `500`). If the number of samples exceeds this threshold, BigBacter will switch to the neighbor-joining approach.

## `--min_tree`

Minimum number of samples in a cluster for a tree to be produced, excluding the reference genome (default: `2`). This must be greater than 2 or IQTREE will fail.

## `--db_info`

Provides a summary of your BigBacter database (default: `true`). A short summary will be printed to the screen upon completion of the pipeline and a full summary can be found in the run directory (e.g., `${timestamp}-db-info.csv`).

## `--resolve_merged`

Whether merged PopPUNK clusters should be resolved (default: `true`).

{: .warning }
> Only turn this off if you know what you are doing.

## `--run_id`

Will be used in place of the timestamp ID.

{: .warning }
> Misuse could lead to database corruption.