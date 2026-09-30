---
title: Reports & Summaries
layout: page
nav_order: 1
grandparent: v2.0
parent: Outputs
permalink: /docs/v2.0/pages/outputs/results
---

# {{ page.title }}
{: .no_toc}

1. TOC
{:toc}

{: .note}
This page describes results saved to `--outdir`. Files written to the BigBacter database (`--db`) are described on the [BigBacter Database](../bigbacter_database/) page.

# Overview
All outputs intended for routine interpretation and reporting are organized under a run-specific subdirectory named by Unix timestamp (`${timestamp}`). This allows results from multiple runs to be saved to a common `--outdir` without overwriting previous results and also provides baked-in tracibility 🥖.

Below is an overview of the standard outputs produced by BigBacter.
```bash
${outdir}/
├── ${timestamp}
│   ├── ${sample}
│   │   ├── asm
│   │   │   └── ${sample}.fa.gz
│   │   ├── taxa
│   │   │   └── ${sample}_gambit.csv
│   │   └── reads
│   │       ├── ${sra}_1.fastq.gz
│   │       └── ${sra}_2.fastq.gz
│   ├── ${taxa}
│   │   ├── ${cluster}
│   │   │   ├── aln
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.aln
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_full.aln
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_full.csv
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.masked.aln
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_full.masked.aln
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}_full.masked.csv
│   │   │   ├── dist
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_db-dist.csv
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_snp-dist.csv
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_db-dist.masked.csv
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}_snp-dist.masked.csv
│   │   │   ├── qc
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_cg-plot.html
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}_cg-plot.masked.html
│   │   │   ├── recomb
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.vcf
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.bed
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}.per_branch_statistics.csv
│   │   │   ├── report
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.microreact
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}.masked.microreact
│   │   │   ├── summary
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}_summary.csv
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}_summary.masked.csv
│   │   │   ├── tree
│   │   │   │   ├── ${timestamp}-${taxa}-${cluster}.nwk
│   │   │   │   └── ${timestamp}-${taxa}-${cluster}.masked.nwk
│   │   │   └── var
│   │   │       └── ${sample}.tar.gz
│   │   └── cluster
│   │       ├── clusters.csv
│   │       └── global_containment.csv
│   ├── multiqc
│   │   └── multiqc_report.html
│   ├── ${timestamp}.csv
│   └── ${timestamp}.masked.csv
└── pipeline_info
    └── ...
```

# Sample Reads, Assemblies, & Taxonomy
Raw reads from NCBI SRA, de novo genome assemblies from GenBank or created via Shovill, and taxonomic classifications determined via GAMBIT are published in sample-specific subdirectories.
```bash
│   ├── ${sample}
│   │   ├── asm
│   │   │   └── ${sample}.fa.gz
│   │   ├── taxa
│   │   │   └── ${sample}_gambit.csv
│   │   └── reads
│   │       ├── ${sra}_1.fastq.gz
│   │       └── ${sra}_2.fastq.gz
```

| File | Description |
|------|-------------|
| `${sample}.fa.gz` | Compressed genome assembly in FASTA format |
| `${sample}_gambit.csv` | GAMBIT taxonomic classification results |
| `${sra}_1.fastq.gz` | Forward reads downloaded from NCBI SRA |
| `${sra}_2.fastq.gz` | Reverse reads downloaded from NCBI SRA |

# Cluster Assignments
Samples are assigned to clusters within each taxon using MinHash-based dissimilarity. Cluster assignments and global containment scores are published at the taxon level.
```bash
│   └── cluster
│       ├── clusters.csv
│       └── global_containment.csv
```

| File | Description |
|------|-------------|
| `clusters.csv` | Per-sample cluster assignments for the current run |
| `global_containment.csv` | Per sample MinHash global containment scores of nearest matching cluster |

# Core Genome Alignments
Core genome SNP alignments produced by Polycore are published per cluster. Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.
```bash
│   └── aln
│       ├── ${timestamp}-${taxa}-${cluster}.aln
│       ├── ${timestamp}-${taxa}-${cluster}_full.aln
│       ├── ${timestamp}-${taxa}-${cluster}_full.csv
│       ├── ${timestamp}-${taxa}-${cluster}.masked.aln
│       ├── ${timestamp}-${taxa}-${cluster}_full.masked.aln
│       └── ${timestamp}-${taxa}-${cluster}_full.masked.csv
```

| File | Description |
|------|-------------|
| `*.aln` | Core genome SNP alignment in FASTA format |
| `*_full.aln` | Full core genome alignment including invariant sites |
| `*_full.csv` | Per-site summary of the full alignment |

# Recombination
Recombinant regions identified by Gubbins are published per cluster. Only produced when recombination masking is enabled and the cluster has sufficient samples.
```bash
│   └── recomb
│       ├── ${timestamp}-${taxa}-${cluster}.vcf
│       ├── ${timestamp}-${taxa}-${cluster}.bed
│       └── ${timestamp}-${taxa}-${cluster}.per_branch_statistics.csv
```

| File | Description |
|------|-------------|
| `*.vcf` | Recombinant SNPs identified by Gubbins in VCF format |
| `*.bed` | Recombinant regions in BED format |
| `*.per_branch_statistics.csv` | Per-branch recombination statistics |

# SNP Variants
Per-sample Snippy output tarballs are published per cluster. These files are also published to the BigBacter database (`--db`) when using `--push true`.
```bash
│   └── var
│       └── ${sample}.tar.gz
```

| File | Description |
|------|-------------|
| `${sample}.tar.gz` | Compressed Snippy output directory for each sample |

# Quality Control
A per-cluster core genome plot is produced by Polycore and a MultiQC report aggregating per-sample QC metrics is produced at the run level. Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.
```bash
│   ├── qc
│   │   ├── ${timestamp}-${taxa}-${cluster}_cg-plot.html
│   │   └── ${timestamp}-${taxa}-${cluster}_cg-plot.masked.html
└── multiqc
    └── multiqc_report.html
```

| File | Description |
|------|-------------|
| `*_cg-plot.html` | Interactive plot of core genome size and SNP density per cluster |
| `multiqc_report.html` | Aggregated QC report including FastQC and fastp metrics for all samples |

# Distances
Pairwise MinHash and core SNP distance matrices are published per cluster. Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.
```bash
│   └── dist
│       ├── ${timestamp}-${taxa}-${cluster}_db-dist.csv
│       ├── ${timestamp}-${taxa}-${cluster}_snp-dist.csv
│       ├── ${timestamp}-${taxa}-${cluster}_db-dist.masked.csv
│       └── ${timestamp}-${taxa}-${cluster}_snp-dist.masked.csv
```

| File | Description |
|------|-------------|
| `*_db-dist.csv` | Pairwise MinHash distances computed by Floc during clustering |
| `*_snp-dist.csv` | Pairwise core SNP distances |

# Summary
Summary tables combining cluster assignments, QC metrics, and SNP distances are produced at two levels: per cluster and per run. Both levels share the same columns (see [Summary Columns](#summary-columns)). Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.

## Cluster Summary
A per-cluster summary table is published within each cluster subdirectory.
```bash
│   └── summary
│       ├── ${timestamp}-${taxa}-${cluster}_summary.csv
│       └── ${timestamp}-${taxa}-${cluster}_summary.masked.csv
```

| File | Description |
|------|-------------|
| `*_summary.csv` | Per-sample summary for all samples in a single cluster, **without** recombination masked |
| `*_summary.masked.csv` | Per-sample summary for all samples in a single cluster, **with** recombination masked |


## Run Summary
A run-level summary table is published at the top of the run directory. It combines the cluster summaries from every taxon and cluster included in the run.
```bash
│   ├── ${timestamp}.csv
│   └── ${timestamp}.masked.csv
```

| File | Description |
|------|-------------|
| `${timestamp}.csv` | Per-sample summary for all taxa and clusters included in the run, **without** recombination masked |
| `${timestamp}.masked.csv` | Per-sample summary for all taxa and clusters included in the run, **with** recombination masked |

## Summary Columns
The cluster-level and run-level summary files contain the following columns.

| Column | Description |
|--------|-------------|
| `id` | Sample identifier (same as supplied in samplesheet) |
| `run` | Run timestamp (Unix time) associated with the sample |
| `status` | Whether the sample was added in the current run (`new`) or already existed in the BigBacter database (`old`) |
| `included` | Whether the sample was included in the cluster analysis (`TRUE`/`FALSE`). Samples are excluded if their genome fraction falls below [`min_genome_fraction`](../inputs/#--min_genome_fraction).|
| `taxa` | Taxon assigned to the sample (from samplesheet or `GAMBIT`) |
| `cluster` | Cluster assigned to the sample within its taxon (from samplesheet or `floc`) |
| `strong_links` | Samples genetically linked to this sample within the cluster, listed as colon-separated sample pairs. Linkages based on [`strong_link_threshold`](../inputs/#--strong_linkage_threshold). |
| `inter_links` | Samples linked to this sample from other clusters, listed as colon-separated sample pairs. Linkages based on [`inter_link_threshold`](../inputs/#--inter_linkage_threshold) |
| `genome_fraction` | Fraction of the reference genome length with called bases, calculated as (`length` − `missing`) / `length` |
| `core_fraction` | Fraction of the core genome that remains after this sample is added to the analysis. This value is used to create the "progressive core genome" plot |
| `length` | Length of the reference genome in base pairs. Will be the same for all samples in a cluster. |
| `masked` | Number of sites masked in the sample |
| `missing` | Number of sites with no base call (e.g., insufficient coverage) |
| `mixed` | Number of sites with mixed or heterozygous base calls |
| `variants` | Number of variant sites relative to the reference |
| `recomb_masked` | Whether recombination masking with Gubbins was applied (`TRUE`/`FALSE`) |
| `partition` | Partition assigned to the sample within the cluster. _NOTE: Unlike clusters, which are stable between runs, partitions are subject to change depending on which samples are included in the analysis!_|

# Phylogeny
A maximum likelihood phylogenetic tree is produced per cluster for clusters with sufficient samples. Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.
```bash
│   └── tree
│       ├── ${timestamp}-${taxa}-${cluster}.nwk
│       └── ${timestamp}-${taxa}-${cluster}.masked.nwk
```

| File | Description |
|------|-------------|
| `*.nwk` | Maximum likelihood phylogenetic tree in Newick format produced by IQ-TREE |

# Reports
A Microreact report is produced per cluster, combining the phylogenetic tree, Floc and SNP distance matrices, per-sample summary, and core genome plot. When recombination masking is enabled, two report are produced — one using the standard outputs and one using the masked outputs.
```bash
│   └── report
│       ├── ${timestamp}-${taxa}-${cluster}.microreact
│       └── ${timestamp}-${taxa}-${cluster}.masked.microreact
```

| File | Description |
|------|-------------|
| `*.microreact` | Microreact project file for interactive visualization at [microreact.org](https://microreact.org) |
