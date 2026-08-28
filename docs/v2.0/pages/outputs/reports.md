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
│   └── multiqc
│       └── multiqc_report.html
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
A per-cluster summary table combining cluster assignments, QC metrics, and SNP distances is published per cluster. Files with `.masked` in the filename are produced using the recombination-masked alignment from Gubbins.
```bash
│   └── summary
│       ├── ${timestamp}-${taxa}-${cluster}_summary.csv
│       └── ${timestamp}-${taxa}-${cluster}_summary.masked.csv
```

| File | Description |
|------|-------------|
| `*_summary.csv` | Per-sample summary including cluster assignment, core genome size, and closest neighbor |

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